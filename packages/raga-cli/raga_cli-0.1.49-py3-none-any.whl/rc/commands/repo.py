import argparse
import logging
from rc.cli import log_setup

from rc.cli.command import CmdBase
from rc.cli.utils import print_success_msg, repo_name_valid
from rc.repo.repo import RepoMain
from rc.utils.config import ConfigManager
from rc.utils.request import RctlValidRequestError, get_all_config

logger = logging.getLogger(__name__)
   
 

"""
----------------------------
***Bucket Name Validation***
----------------------------
Bucket names should not contain upper-case letters
Bucket names should not contain underscores (_)
Bucket names should not end with a dash
Bucket names should be between 3 and 63 characters long
Bucket names cannot contain dashes next to periods (e.g., my-.bucket.com and my.-bucket are invalid)
Bucket names cannot contain periods - Due to our S3 client utilizing SSL/HTTPS, Amazon documentation indicates that a bucket name cannot contain a period, otherwise you will not be able to upload files from our S3 browser in the dashboard.
"""   


class CmdRepo(CmdBase):
    def __init__(self, args): 
        super().__init__(args)
        log_setup(self.args)  
        self.repo = RepoMain(self.config)    
        repo_name = getattr(self.args, "name", None) #name is equivalent of git branch name
        if repo_name: 
            repo_name = repo_name.lower()
            setattr(self.args, "name", repo_name)            
            repo_name_valid(repo_name) #name is equivalent of git branch name
        else:
            raise RctlValidRequestError("Error: Please provide a valid name, -n")
                
class CmdRepoCreate(CmdRepo):
    def run(self):         
        if self.args.create:
            logger.debug(f"START CREATE REPO COMMAND")
            print("Repo creating...")
            self.repo.create_repo(self.args)
        if self.args.clone:
            self.repo.clone_repo(self.args)                                    
        return 0


def add_parser(subparsers, parent_parser):
    REPO_HELP = "Create a new repository."
    REPO_DESCRIPTION = (
        "Create a new repository."
    )

    repo_parser = subparsers.add_parser(
        "repo",
        parents=[parent_parser],
        description=REPO_DESCRIPTION,
        help=REPO_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    repo_parser.add_argument(
        "-create",
        "--create",
        action="store_true",
        default=False,
        help="Create new repo",
    )

    repo_parser.add_argument(
        "-clone",
        "--clone",
        action="store_true",
        default=False,
        help="Clone new repo",
    )

    repo_parser.add_argument(
        "-n", 
        "--name", 
        nargs="?", 
        help="Name of the repo",
    )


    repo_parser.add_argument(
        "-tag", 
        "--tag", 
        nargs="?", 
        help="Tag of the repo",
    )

    repo_parser.add_argument(
        "-o", 
        "--output", 
        type=bool, 
        nargs='?',
        const=True, 
        default=False,
        help="Output debug",
    )
    
    repo_parser.set_defaults(func=CmdRepoCreate)
