import logging
import os
from pathlib import Path
from pydoc import stripid
import json
import subprocess
import tempfile
import time
import sys
from multiprocessing import cpu_count
from pathlib import Path
import pathlib
import re
from datetime import datetime
from rc.utils.config import ConfigManager
from rc.utils.json_parser import *

from rc.utils.request import get_commit_repo, get_config_value_by_key, get_repo_version

logger = logging.getLogger(__name__)
LOG_FILE = "rc.log"

class RctlValidSubprocessError(Exception):
    def __init__(self, msg, *args):
        assert msg
        self.msg = msg
        super().__init__(msg, *args)

def fix_subparsers(subparsers):
    subparsers.required = True
    subparsers.dest = "cmd"

def get_git_url(repository_name):
    result = subprocess.run('git config --get remote.origin.url', capture_output=True, shell=True, cwd=repository_name)    
    stdout = str(result.stdout, 'UTF-8')
    return stripid(stdout)

def get_repo(cwd = None):
    if cwd:
        owd = os.getcwd()
        os.chdir(f"{owd}/{cwd}") 
        repo_name =  os.path.basename(os.getcwd()) 
        os.chdir(owd)  
    else:
        repo_name =  os.path.basename(os.getcwd())
    return repo_name

def get_current_dir_name():
    return os.path.basename(os.getcwd())

def trim_str_n_t(str):
    return ' '.join(str.split())

def valid_command_response(cmd, compare_str, _return = False, error_message=None):
    logger.debug(f"COMMAND: {cmd}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True, check=True)
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        
        logger.debug(f"STD OUT: {stdout}")
        logger.debug(f"STD ERR: {stderr}")

        if re.search(compare_str, stdout) or re.search(compare_str, stderr):
            if _return:
                return True, "match", stdout, stderr
            print(f"rc: error: {error_message}")
            sys.exit(1)
        else:
            if _return:
                return False, "match", stdout, stderr
            print(f"rc: error: {error_message}")
            sys.exit(1)
    
    except subprocess.CalledProcessError as e:
        logger.debug(f"STD OUT: {e.stdout}")
        logger.debug(f"STD ERR: {e.stderr}")
        stdout = e.stdout
        stderr = e.stderr
        logger.debug(f"Command '{cmd}' failed with return code {e.returncode}")
        if re.search(compare_str, stdout) or re.search(compare_str, stderr):
            if _return:
                return True, "match", stdout, stderr
            print(f"rc: error: {error_message}")
            sys.exit(1)
        else:
            if _return:
                return False, "match", stdout, stderr
            print(f"rc: error: {error_message}")
            sys.exit(1)

def check_git_init():
    return os.path.exists('.git')

def check_dvc_init():
    return os.path.exists('.dvc')

def upload_log():
    logger.debug("ERROR LOG INITIATE")
    CLOUD_STORAGE = get_config_value_by_key('cloud_storage')
    temp_dir = tempfile.gettempdir()
    log_file_path = os.path.join(temp_dir, LOG_FILE)

    CLOUD_STORAGE_BUCKET = get_config_value_by_key('bucket_name')
    CLOUD_STORAGE_DIR = get_config_value_by_key('cloud_storage_dir')
    SECRET = get_config_value_by_key('minio_secret_key') if CLOUD_STORAGE == 'minio' else get_config_value_by_key('s3_storage_secret_key')
    ACCESS = get_config_value_by_key('minio_access_key') if CLOUD_STORAGE == 'minio' else get_config_value_by_key('s3_storage_access_key')
    MINIO_URL = get_config_value_by_key('minio_url')
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"rc_{current_datetime}.log"
    repo = get_repo()
    if repo:
        dest = f"{CLOUD_STORAGE_DIR}/{repo}/logs/{log_filename}"
    else:
        dest = f"{CLOUD_STORAGE_DIR}/logs/{log_filename}"
    import botocore.session   
    # Create a botocore session with the AWS access key and secret key
    session = botocore.session.Session()
    session.set_credentials(ACCESS, SECRET)

    if CLOUD_STORAGE == 'minio':
        s3 = session.create_client('s3', endpoint_url=MINIO_URL)
    else:
        s3 = session.create_client('s3')

    # Upload the file to S3
    with open(log_file_path, 'rb') as file:
        s3.put_object(Bucket=CLOUD_STORAGE_BUCKET, Key=dest, Body=file) 

def print_err_msg(msg=""):
    print(f"rc: error: {msg}")
    sys.exit(1)

def print_success_msg(msg=""):
    print(f"rc: success: {msg}")
    sys.exit(1)

def get_dvc_data_status(path):
    logger.debug("Compare on PATH : {}".format(path))
    result = subprocess.run('dvc status {}'.format(path), capture_output=True, shell=True)    
    stdout = str(result.stdout, 'UTF-8').strip()
    logger.debug(stdout)
    # stdout_line = stdout.splitlines()
    # stdout_line = list(map(trim_str_n_t, stdout_line))
    if stdout.find('modified') != -1:
        return True  
    if stdout.find('Data and pipelines are up to date') != -1:
        return False  
    return False

def get_new_dvc_data_status(path):
    if not get_dvc_data_status(path) and not compare_dot_dvc_file(path):
        return True
    return False



def dataset_current_version(paths, repo):
    current_version = 0 if not get_repo_version(repo) else int(get_repo_version(repo))
    for path in paths:
        if not compare_dot_dvc_file(path):
            return current_version+1
        if get_dvc_data_status(path):
            return current_version+1
    return 1 if not current_version else current_version


def model_current_version(repo):
    current_version = 0 if not get_repo_version(repo) else int(get_repo_version(repo))
    return 1 if not current_version else current_version+1

def server_repo_commit_status(ids):
    elastic_processes = []
    for id in ids:
        elastic_processes.append(get_commit_repo(id)['check_elastic_process'])
    logger.debug("ELASTIC PROCESS {}".format(elastic_processes))
    return all(elastic_processes)

def current_commit_hash(cwd=None):
    if cwd:
        result = subprocess.run('git rev-parse HEAD', capture_output=True, shell=True, cwd=cwd)
    else:
        result = subprocess.run('git rev-parse HEAD', capture_output=True, shell=True)
    stdout = str(result.stdout, 'UTF-8')
    logger.debug(f"COMMIT HASH: {stdout.strip()}")
    return stdout.strip()

def current_branch():
    result = subprocess.run('git rev-parse --abbrev-ref HEAD', capture_output=True, shell=True)    
    stdout = str(result.stdout, 'UTF-8')
    return stdout.strip()

def branch_commit_checkout(branch,commitId):
    result = subprocess.run('git checkout {0} -b {1}'.format(commitId,branch), capture_output=True, shell=True)    
    stdout = str(result.stdout, 'UTF-8')
    return stdout.strip()

def is_repo_exist_in_gh(repo):
    logger.debug("Check existence of repo in GIT HUB : {}".format(repo))
    result = subprocess.run('gh repo view {}'.format(repo), capture_output=True, shell=True)    
    stdout = str(result.stdout, 'UTF-8').strip()
    stderr = str(result.stderr, 'UTF-8').strip()
    logger.debug(f"STD OUT: {stdout}")
    logger.debug(f"STD ERR: {stderr}")
    match = re.search(r'Could not resolve to a Repository with the name', stderr)
    if match:
        logger.debug("Repo not found in GH")
        return False  
    logger.debug("Repo found in GH")
    return True

def check_dvc_add_left():
    logger.debug("Check DVC ADD left")
    result = subprocess.run('dvc status', capture_output=True, shell=True)    
    stdout = str(result.stdout, 'UTF-8').strip()
    stderr = str(result.stderr, 'UTF-8').strip()
    logger.debug(f"STD OUT: {stdout}")
    logger.debug(f"STD ERR: {stderr}")
    if re.search(r'(modified:)', stdout):
        logger.debug("DVC ADD left")
        return True  
    elif re.search(r'(modified:)', stderr):
        logger.debug("DVC ADD left")
        return True  
    logger.debug("Clean DVC ADD")
    return False

def check_dvc_file_deleted():
    logger.debug("Check DVC DELETED file")
    result = subprocess.run('dvc status', capture_output=True, shell=True)    
    stdout = str(result.stdout, 'UTF-8').strip()
    stderr = str(result.stderr, 'UTF-8').strip()
    logger.debug(f"STD OUT: {stdout}")
    logger.debug(f"STD ERR: {stderr}")
    if re.search(r'(deleted:)', stdout):
        logger.debug("DVC DELETED file")
        return True  
    elif re.search(r'(deleted:)', stderr):
        logger.debug("DVC DELETED file")
        return True  
    logger.debug("Clean DVC ADD")
    return False

def check_push_left():
    logger.debug("Check PUSH left")
    result = subprocess.run('git status', capture_output=True, shell=True)    
    stdout = str(result.stdout, 'UTF-8').strip()
    stderr = str(result.stderr, 'UTF-8').strip()
    logger.debug(f"STD OUT: {stdout}")
    logger.debug(f"STD ERR: {stderr}")
    if re.search(r'(use "git push" to publish your local commits)', stdout):
        logger.debug("Push left")
        return True  
    elif re.search(r'(use "git push" to publish your local commits)', stderr):
        logger.debug("Push left")
        return True  
    logger.debug("Clean PUSH")
    return False

def check_git_add_untrack_files():
    logger.debug("Check GIT UNTRACK file")
    result = subprocess.run('git status', capture_output=True, shell=True)    
    stdout = str(result.stdout, 'UTF-8').strip()
    stderr = str(result.stderr, 'UTF-8').strip()
    logger.debug(f"STD OUT: {stdout}")
    logger.debug(f"STD ERR: {stderr}")
    if re.search(r'(Untracked files:)', stdout):
        logger.debug(stdout)
        return True  
    elif re.search(r'(Untracked files:)', stderr):
        logger.debug(stderr)
        return True  
    logger.debug("Clean UNTRACK file")
    return False

def check_git_commit_files():
    logger.debug("Check GIT UNTRACK file")
    result = subprocess.run('git status', capture_output=True, shell=True)    
    stdout = str(result.stdout, 'UTF-8').strip()
    stderr = str(result.stderr, 'UTF-8').strip()
    logger.debug(f"STD OUT: {stdout}")
    logger.debug(f"STD ERR: {stderr}")
    if re.search(r'(Changes to be committed:)', stdout):
        logger.debug(stdout)
        return True  
    elif re.search(r'(Changes to be committed:)', stderr):
        logger.debug(stderr)
        return True  
    logger.debug("Clean UNTRACK file")
    return False

def check_git_deleted_files():
    logger.debug("Check GIT DELETED file")
    result = subprocess.run('git status', capture_output=True, shell=True)    
    stdout = str(result.stdout, 'UTF-8').strip()
    stderr = str(result.stderr, 'UTF-8').strip()
    logger.debug(f"STD OUT: {stdout}")
    logger.debug(f"STD ERR: {stderr}")
    if re.search(r'(Changes not staged for commit:)', stdout):
        logger.debug(stdout)
        return True  
    elif re.search(r'(Changes not staged for commit:)', stderr):
        logger.debug(stderr)
        return True  
    logger.debug("Clean DELETED file")
    return False

def is_current_version_stable():
    from rc.utils.request import get_commit_version, get_repo_version
    repo = get_repo()
    commit_id = current_commit_hash()
    repo_version = get_repo_version(repo)
    commit_version = get_commit_version(commit_id)
    if not commit_version and not repo_version:
        return True

    if commit_version == repo_version:
        return True
    else:
        logger.debug("Local repo version is not stable")
        print("Unable to upload from older version. Please use `rc get` to get the latest version and try again.")
        return False     

def get_dir_file(path):
    dvc_file = Path(f'{path}.dvc')
    if not dvc_file.is_file():
        logger.debug("DVC file not found.")
        print("Something went wrong")
        sys.exit(50)
    dvc_read = open(dvc_file, "r")
    md5_dir = ''
    for line in dvc_read.readlines():
        if line.find('- md5') != -1:
            md5_dir = line.split(":")[-1].strip()
    if not md5_dir:
        logger.error(".dir file not found.")
        sys.exit(50)
    return md5_dir

def get_only_valid_dir(dir):
    if not dir.startswith("."):
        return True
    else:
        return False

def trim_slash(str):
    if str.endswith("/"):
        str = str.rsplit("/", 1)[0] 
    return str

def valid_cwd_rc():
    cwd = os.getcwd()   # get the current working directory
    rc_dir = os.path.join(cwd, ".rc")   # create a path to the .rc directory
    if not os.path.isdir(rc_dir):   # check if the path is a directory
        print("Your current location is not a rc repo directory location.")
        sys.exit()
    return True

def find_dvc_files():
    files = []
    cwd = os.getcwd()   # get the current working directory
    for file in os.listdir(cwd):   # iterate through the files in the current directory
        if file.endswith(".dvc") and not os.path.isdir(os.path.join(cwd, file)):   # check if the file has a .dvc extension and is not a directory
            files.append(os.path.join(cwd, file))
    return files

def match_and_delete_files(dir_list, file_list):
    dir_names = [os.path.basename(d) for d in dir_list]   # get the names of the directories in the first list
    deleted_files = []
    for file in file_list:   # iterate through the files in the second list
        filename = pathlib.Path(file).stem   # get the filename from the full path
        if filename not in dir_names:   # check if the filename is not in the list of directory names
            logger.debug(f"REMOVE DVC FILE : {filename}")
            os.remove(file)   # delete the file if it does not have a matching directory name
            deleted_files.append(file)
    return deleted_files

def check_extensions(extensions=["requirements.txt", ".pth"]):
    found_extensions = set()
    for extension in extensions:
        extension_found = False
        for subdir, dirs, filenames in os.walk("."):
            for filename in filenames:
                if filename.endswith(extension):
                    found_extensions.add(extension)
                    extension_found = True
                    break
            if extension_found:
                break
        if not extension_found:
            print_err_msg(f"{extension} file not found.")
            sys.exit()
    return True

def valid_dot_dvc_with_folder(dirs):
    files = find_dvc_files()
    return match_and_delete_files(dirs, files)
    
def get_all_data_folder():
    directory = os.getcwd()
    dirs = next(os.walk(directory))[1]
    filtered = list(filter(get_only_valid_dir, dirs))
    return filtered

def compare_dot_dvc_file(dir_path):
    dvc_file = Path(f'{dir_path}.dvc')
    if dvc_file.is_file():
        return True
    return False
    
def back_slash_trim(dirs):
    filtered = list(map(trim_slash, dirs))
    return filtered

def run_command_on_subprocess(command, cwd=None, err_skip=False):
    logger.debug(command)
    kwargs = {
        "capture_output": True,
        "shell": True,
        "cwd": cwd
    } if cwd else {
        "capture_output": True,
        "shell": True
    }

    result = subprocess.run(command, **kwargs)
    stderr = result.stderr.decode('utf-8')
    stdout = result.stdout.decode('utf-8')
    
    logger.debug("STD OUT: {}".format(stdout))
    logger.debug("STD ERR: {}".format(stderr))     
                

def repo_name_valid(name):
    for c in name:        
        if c == '_':
            raise RctlValidSubprocessError(f"Error: Bucket name contains invalid (_) characters. Name: {name}")
    if len(name) <3 or len(name)>63:
        raise RctlValidSubprocessError("Error: Bucket names should be between 3 and 63 characters long")   
    
def path_to_dict(path, is_full_path=False):
    if not os.path.exists(path):
        return None

    name = os.path.basename(path)
    if name == ".rc" or name == ".git" or name == ".DS_Store" or name == ".dvc" or name == ".gitignore" or name == ".dvcignore" or name == "model.dvc":
        return None

    d = {'name': name}
    if is_full_path:
        current_path = os.getcwd()
        full_path = os.path.join(current_path, path)
        d['full_path'] = full_path

    if os.path.isdir(path):
        d['type'] = "directory"
        children = []
        for filename in os.listdir(path):
            child_path = os.path.join(path, filename)
            child_dict = path_to_dict(child_path, is_full_path)
            if child_dict is not None:
                children.append(child_dict)
        if children:  # Only add children if there are any non-empty directories or files
            d['children'] = children
        else:
            return None
    else:
        d['type'] = "file"
        d['last_updated'] = datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')

    return d


def upload_model_file_list_json(version, config_manager: ConfigManager, cwd = None):
    if cwd:
        owd = os.getcwd()
        os.chdir(f"{owd}/{cwd}") 
    logger.debug("MODEL FILE UPLOADING")
    model_file_list = json.loads(json.dumps(path_to_dict('.')))
    CLOUD_STORAGE = config_manager.get_config_value('cloud_storage')
    CLOUD_STORAGE_BUCKET = config_manager.get_config_value('bucket_name')
    CLOUD_STORAGE_DIR = config_manager.get_config_value('cloud_storage_dir')

    SECRET = config_manager.get_config_value('minio_secret_key') if CLOUD_STORAGE == 'minio' else config_manager.get_config_value('s3_storage_secret_key')
    ACCESS = config_manager.get_config_value('minio_access_key') if CLOUD_STORAGE == 'minio' else config_manager.get_config_value('s3_storage_access_key')

    MINIO_URL = config_manager.get_config_value('minio_url')
    repo = get_repo()
    dest = f"{CLOUD_STORAGE_DIR}/{repo}/model_files/{version}.json"
    json_file = f'{version}.json'
    with open(json_file, 'w', encoding='utf-8') as cred:    
        json.dump(model_file_list, cred, ensure_ascii=False, indent=4)  

    import botocore.session   

    session = botocore.session.Session()
    session.set_credentials(ACCESS, SECRET)
    
    if CLOUD_STORAGE == 'minio':
        s3 = session.create_client('s3', endpoint_url=MINIO_URL)
    else:
        s3 = session.create_client('s3')

    with open(json_file, 'rb') as file:
        s3.put_object(Bucket=CLOUD_STORAGE_BUCKET, Key=dest, Body=file) 
    
    pathlib.Path(json_file).unlink(missing_ok=True)
    if cwd:
        os.chdir(owd) 
    
def retry(ExceptionToCheck, tries=4, delay=3, backoff=2):
    """
    Retry calling the decorated function using an exponential backoff.

    Args:
        ExceptionToCheck (Exception): the exception to check. When an exception of this type is raised, the function will be retried.
        tries (int): number of times to try before giving up.
        delay (int): initial delay between retries in seconds.
        backoff (int): backoff multiplier (e.g. value of 2 will double the delay each retry).

    Example Usage:
    ```
    @retry(Exception, tries=4, delay=3, backoff=2)
    def test_retry():
        # code to retry
    ```
    """
    logger.debug("RETRYING")
    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    print(f"Got exception '{e}', retrying in {mdelay} seconds...")
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)
        return f_retry
    return deco_retry


def folder_exists(folder_name):
    current_dir = os.getcwd()
    folder_path = os.path.join(current_dir, folder_name)
    return os.path.exists(folder_path) and os.path.isdir(folder_path)



def calculate_coordinates(bbox, width, height):
    normalized_bbox = [
        bbox[0] / width,   # Normalized x-coordinate (xmin)
        bbox[1] / height,  # Normalized y-coordinate (ymin)
        bbox[2] / width,   # Normalized width
        bbox[3] / height   # Normalized height
    ]
    return normalized_bbox


def datetime_to_units(datetime_str, unit='milliseconds'):
    # Convert datetime string to datetime object
    dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

    # Get the total seconds from the Unix epoch to the given datetime
    total_seconds = (dt - datetime(1970, 1, 1)).total_seconds()

    if unit == 'seconds':
        return int(total_seconds)
    elif unit == 'milliseconds':
        return int(total_seconds * 1000)
    elif unit == 'nanoseconds':
        return int(total_seconds * 1e9)
    else:
        raise ValueError("Invalid unit. Please choose 'seconds', 'milliseconds', or 'nanoseconds'.")
    
def add_tmp(path):
    import random
    import string
    # Generate a random string
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    # Create a temporary file with the random string and .tmp extension
    temp_file_path = os.path.join(path, ".tmp")
    with open(temp_file_path, 'w') as temp_file:
        temp_file.write(random_string)

    return temp_file_path
