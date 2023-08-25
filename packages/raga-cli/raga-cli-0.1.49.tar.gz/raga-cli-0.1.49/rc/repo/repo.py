import argparse
import json
import logging
import os
from datetime import timedelta
import sys 
from timeit import default_timer as timer
import os, pwd

from rc.cli.command import CmdBase
from rc.cli.utils import check_dvc_init, check_git_init, current_commit_hash, folder_exists, is_repo_exist_in_gh, print_err_msg, print_success_msg, run_command_on_subprocess, get_git_url, upload_model_file_list_json, valid_command_response
from rc.utils.config import ConfigManager
from rc.utils.request import create_repository, create_repo_lock, get_repo_commit, get_repository, insert_repo_commit

logger = logging.getLogger(__name__)
class RepoMain():
    def __init__(self, config_manager:ConfigManager) -> None:
        self.config_manager = config_manager
        self.CLOUD_STORAGE = self.config_manager.get_config_value('cloud_storage')
        self.CLOUD_STORAGE_BUCKET = self.config_manager.get_config_value('bucket_name')
        self.CLOUD_STORAGE_DIR = self.config_manager.get_config_value('cloud_storage_dir')
        self.CLOUD_STORAGE_LOCATION = f"s3://{self.CLOUD_STORAGE_BUCKET}/{self.CLOUD_STORAGE_DIR}"
        self.MINIO_URL = self.config_manager.get_config_value('minio_url') if self.CLOUD_STORAGE == 'minio' else ""
        self.INITIAL_COMMIT = self.config_manager.get_config_value('git_initial_commit')
        self.GIT_BRANCH = self.config_manager.get_config_value('git_initial_branch')
        self.GIT_ORG = self.config_manager.get_config_value('git_org')
        self.GH_TOKEN = self.config_manager.get_config_value('gh_token')
        self.TAGS = {"dataset", "model"}
        self.created_by = pwd.getpwuid(os.getuid()).pw_name 
        self.common_repo_name = self.config_manager.get_config_value('repo_name')
        self.secret_key = self.config_manager.get_config_value('minio_secret_key') if self.CLOUD_STORAGE == 'minio' else self.config_manager.get_config_value('s3_storage_secret_key')
        self.access_key = self.config_manager.get_config_value('minio_access_key') if self.CLOUD_STORAGE == 'minio' else self.config_manager.get_config_value('s3_storage_access_key')
    
    def validation(self, repository_name, repository_tag):
        if folder_exists(repository_name):
            print_err_msg("The repository creation process could not be completed due to the presence of the directory in the current location.")
        if check_git_init():
            print_err_msg("The repository creation process could not be completed as the current directory already contains a Git repository.")
        repo_name, tag = get_repository(repository_name)
        if repo_name:
            print_err_msg("The repo creating process could not be completed because the repo already exists. Please rename repo and try again.")
        if repository_tag not in self.TAGS:
            print_err_msg("'{0}' tag is not available. Please select from {1}".format(repository_tag, self.TAGS))

    def run_git_commands(self, repository_name):   
        run_command_on_subprocess("git commit -m '{0}' -a".format(self.INITIAL_COMMIT), repository_name)    
        run_command_on_subprocess("git branch -M {0}".format(repository_name), repository_name)    
        run_command_on_subprocess("git push --set-upstream origin {0}".format(repository_name), repository_name)

    def run_repo_create_subprocesses(self,repo_name, repo_tag):    
        logger.debug(f"Repository Name: {repo_name}") #name is equivalent of git branch name
        run_command_on_subprocess(f"mkdir {repo_name}") 
        run_command_on_subprocess(f"git clone https://{self.GH_TOKEN}@github.com/{self.GIT_ORG}/{self.common_repo_name}.git .", repo_name, True)
        run_command_on_subprocess(f"git checkout -b {repo_name}", repo_name)

        run_command_on_subprocess("dvc init", repo_name)    
        run_command_on_subprocess("dvc remote add -d {0} {1}/{2} -f".format(self.CLOUD_STORAGE_BUCKET, self.CLOUD_STORAGE_LOCATION, repo_name), repo_name)   
        if self.CLOUD_STORAGE == 'minio':        
            run_command_on_subprocess("dvc remote modify {0} endpointurl {1}".format(self.CLOUD_STORAGE_BUCKET, self.MINIO_URL, repo_name), repo_name)           
        run_command_on_subprocess("dvc remote modify {0} secret_access_key {1}".format(self.CLOUD_STORAGE_BUCKET,self.secret_key ), repo_name)         
        run_command_on_subprocess("dvc remote modify {0} access_key_id {1}".format(self.CLOUD_STORAGE_BUCKET, self.access_key), repo_name)        
        run_command_on_subprocess("dvc config core.autostage true", repo_name)
                        
        if repo_tag == "model": 
            gitignored_extensions = self.config_manager.get_config_value('gitignored_extensions').split(",")
            for extension in gitignored_extensions:
                run_command_on_subprocess(f"echo *{extension} >> .gitignore", repo_name)
            run_command_on_subprocess(f"mkdir model", repo_name) 
            run_command_on_subprocess(f"echo /model >> .gitignore", repo_name) 
            run_command_on_subprocess("touch README.md", repo_name)      
            run_command_on_subprocess("git add README.md", repo_name)
            run_command_on_subprocess("git add .gitignore", repo_name)

    
    def create_repo(self, args):
        repository_name = getattr(args, "name", None) #name is equivalent of git branch name
        repository_tag = getattr(args, "tag", None)
        self.validation(repository_name, repository_tag)

        self.run_repo_create_subprocesses(repository_name, repository_tag)
        git_repo = get_git_url(repository_name)
        
        if repository_tag == "dataset":

            s3_repo = "{1}/{2}".format(self.CLOUD_STORAGE_BUCKET, self.CLOUD_STORAGE_LOCATION, repository_name)  

            req_body = json.dumps({
                "repo_name":repository_name,
                "tag":repository_tag,
                "created_by":self.created_by,
                "git_repo":git_repo.replace('\n', ''),
                "remote_storage_url":s3_repo,
            })

            logger.debug(req_body)

        if repository_tag == "model":
            req_body = json.dumps({
                "repo_name":repository_name,
                "tag":repository_tag,
                "created_by":self.created_by,
                "git_repo":git_repo.replace('\n', ''),
            })
            logger.debug(req_body)

        create_repository(req_body)
        
        if repository_tag == "dataset":
            self.run_git_commands(repository_name)

        if repository_tag == "model":
            self.run_git_commands(repository_name)
            commit_hash = current_commit_hash(repository_name)
            request_payload = {
                    "commit_message" : "Initial commit",
                    "repo" : repository_name,
                    "commit_id":commit_hash,
                    "version":0,
                    "branch":"master"
                }  
            insert_repo_commit(json.dumps(request_payload))
            upload_model_file_list_json(commit_hash, self.config_manager, repository_name)

        create_repo_lock(json.dumps({"repo_name":repository_name, "user_name":self.created_by, "locked":False}))
        print("Repository has been created. `cd {}`".format(repository_name))    

        logger.debug(f"END CREATE REPO COMMAND")

    def clone_repo(self, args):
        if check_git_init():
            print_err_msg("The repo cloning process inside the repository is not possible.")
        start = timer()
        repository_name = getattr(args, "name", None) #name is equivalent of git branch name

        if folder_exists(repository_name):
            print_err_msg("The repository cloning process could not be completed due to the presence of the directory in the current location.")
        print('Cloning...')
        repo_name, tag = get_repository(repository_name)
        repo_commit = get_repo_commit(repository_name)
        if not repo_name:
            print_err_msg("Repo not found")
        run_command_on_subprocess(f"mkdir {repository_name}") 
        run_command_on_subprocess(f"git clone https://{self.GH_TOKEN}@github.com/{self.GIT_ORG}/{self.common_repo_name}.git .", repo_name, True) 
        run_command_on_subprocess(f"git checkout {repo_name}", repository_name)
        run_command_on_subprocess('git reset --hard', repository_name)
        run_command_on_subprocess('git reset --hard {0}'.format(repo_commit['commit_id']), repository_name)
        run_command_on_subprocess('git clean -fd', repository_name)
        run_command_on_subprocess('dvc pull -f', repository_name)
        print("Repository cloned successfully")
        end = timer()
        logger.debug('CLONE TIME {0}'.format(timedelta(seconds=end-start))) 