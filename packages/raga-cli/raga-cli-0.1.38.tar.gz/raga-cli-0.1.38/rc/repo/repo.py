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
from rc.utils.request import create_repository, create_repo_lock, get_repository, insert_repo_commit

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
        self.AUTH_TOKEN = self.config_manager.get_config_value('auth_token')
        self.TAGS = {"dataset", "model"}
        self.created_by = pwd.getpwuid(os.getuid()).pw_name 
        self.common_repo_name = self.config_manager.get_config_value('repo_name')
        self.secret_key = self.config_manager.get_config_value('minio_secret_key') if self.CLOUD_STORAGE == 'minio' else self.config_manager.get_config_value('s3_storage_secret_key')
        self.access_key = self.config_manager.get_config_value('minio_access_key') if self.CLOUD_STORAGE == 'minio' else self.config_manager.get_config_value('s3_storage_access_key')
        self.pre_validation()

    def pre_validation(self):
        if not check_git_init():
            print_err_msg("The repo creating process could not be completed because the directory does not contain git repo.")
    
    def validation(self, repository_name, repository_tag, git_protocol):
        if git_protocol == "ssh":
            success, match, out, err = valid_command_response("ssh -T git@github.com", "You've successfully authenticated", True)
            if not success:
                print_err_msg("git@github.com: Permission denied (publickey)")
            success, match, out, err = valid_command_response(f"git branch", repository_name, True)
        if success:
            print_err_msg("The repo creating process could not be completed because the repo already exists. Please rename repo and try again.")
        if repository_tag not in self.TAGS:
            print_err_msg("'{0}' tag is not available. Please select from {1}".format(repository_tag, self.TAGS))
        if check_dvc_init():
            print_err_msg("The repo creating process could not be completed because current dir contains .dvc. Please remove .dvc dir and try again.")

    def run_git_commands(self, repository_name):   
        run_command_on_subprocess("git commit -m '{0}' -a".format(self.INITIAL_COMMIT))    
        run_command_on_subprocess("git branch -M {0}".format(repository_name))    
        run_command_on_subprocess("git push --set-upstream origin {0}".format(repository_name))

    def run_repo_create_subprocesses(self,repo_name, repo_tag, git_protocol):    
        logger.debug(f"Repository Name: {repo_name}") #name is equivalent of git branch name
        run_command_on_subprocess(f"gh config set git_protocol {git_protocol}")
        if repo_tag =="dataset":
            run_command_on_subprocess(f"git checkout -b {repo_name}")
            run_command_on_subprocess("dvc init -f")    
            run_command_on_subprocess("dvc remote add -d {0} {1}/{2} -f".format(self.CLOUD_STORAGE_BUCKET, self.CLOUD_STORAGE_LOCATION, repo_name))   
            if self.CLOUD_STORAGE == 'minio':        
                run_command_on_subprocess("dvc remote modify {0} endpointurl {1}".format(self.CLOUD_STORAGE_BUCKET, self.MINIO_URL, repo_name))           
            run_command_on_subprocess("dvc remote modify {0} secret_access_key {1}".format(self.CLOUD_STORAGE_BUCKET,self.secret_key ))         
            run_command_on_subprocess("dvc remote modify {0} access_key_id {1}".format(self.CLOUD_STORAGE_BUCKET, self.access_key))        
            run_command_on_subprocess("dvc config core.autostage true")            
        if repo_tag == "model": 
            run_command_on_subprocess(f"git checkout -b {repo_name}")
            run_command_on_subprocess("touch README.md")      
            run_command_on_subprocess("git add README.md")

    
    def create_repo(self, args):
        repository_name = getattr(args, "name", None) #name is equivalent of git branch name
        repository_tag = getattr(args, "tag", None)
        git_protocol = getattr(args, "git_protocol", None)
        self.validation(repository_name, repository_tag, git_protocol)

        self.run_repo_create_subprocesses(repository_name, repository_tag, git_protocol)
        git_repo = get_git_url()
        
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
            commit_hash = current_commit_hash()
            request_payload = {
                    "commit_message" : "Initial commit",
                    "repo" : repository_name,
                    "commit_id":commit_hash,
                    "version":0,
                    "branch":"master"
                }  
            insert_repo_commit(json.dumps(request_payload))
            upload_model_file_list_json(commit_hash)

        create_repo_lock(json.dumps({"repo_name":repository_name, "user_name":self.created_by, "locked":False}))
        print_success_msg("Repository has been created.")  

        logger.debug(f"END CREATE REPO COMMAND")

    def clone_repo(self, args):
        if self.check_git_init():
            print("The repo cloning process inside the repository is not possible.")
            sys.exit(50)
        start = timer()
        repository_name = args.name  

        if folder_exists(repository_name):
            print("The repo cloning process could not be completed because the directory already exists.")
            sys.exit(50)

        print('Cloning...')
        run_command_on_subprocess("git clone git@github.com:{0}/{1}.git".format(self.GIT_ORG, repository_name), None, True)    
        tag = get_repository(repository_name)
        if tag == "dataset":
            run_command_on_subprocess("dvc pull", repository_name, True) 
        print("Repository cloned successfully")
        end = timer()
        logger.debug('CLONE TIME {0}'.format(timedelta(seconds=end-start))) 