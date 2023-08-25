import logging
import os
import subprocess
from rc.cli.utils import RctlValidSubprocessError, upload_log
from rc.utils.config import ConfigKeyNotFoundError
from rc.utils.request import RctlValidRequestError, get_config_value_by_key
from rc.utils import DEBUG
import tempfile

logger = logging.getLogger(__name__)
LOG_FILE = "rc.log"

def log_setup(args = None):
    if DEBUG:
        level = logging.DEBUG
        logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')     
    elif args:
        if args.output:
            level = logging.DEBUG
            logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S') 
    else:
        # Get the temporary directory path
        temp_dir = tempfile.gettempdir()
        logger.setLevel(logging.DEBUG)
        # Create a file handler and set the logging level
        log_file_path = os.path.join(temp_dir, LOG_FILE)
        file_handler = logging.FileHandler(log_file_path, mode='w')
        file_handler.setLevel(logging.DEBUG)
        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Add the formatter to the file handler
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)

log_setup()
class RctlParserError(Exception):
    """Base class for CLI parser errors."""
    def __init__(self):
        logger.error("Parser error")
        super().__init__("Parser error")

class RctlError(Exception):
    def __init__(self, msg, *args):
        assert msg
        self.msg = msg
        logger.error(msg)
        super().__init__(msg, *args)

def parse_args(argv=None):
    from .parser import get_main_parser
    try:
        parser = get_main_parser()
        args = parser.parse_args(argv)
        args.parser = parser
        return args
    except RctlParserError as exc:
        pass

def valid_requirement():
    for tool in ['git']:
        try:
            subprocess.run([tool, '--version'], capture_output=True, text=True, check=True)
        except OSError:
            raise RctlError(f'rc: error: {tool} not found! Please install {tool}')

def main(argv=None):
    try:
        valid_requirement()
        args = parse_args(argv)
        cmd = args.func(args)
        cmd.do_run()
        upload_log()
    except KeyboardInterrupt as exc:
        logger.debug(exc)
        upload_log()
    except (RctlValidRequestError, RctlValidSubprocessError, RctlError, ConfigKeyNotFoundError) as exc:
        print(exc.msg)
        upload_log()
    except ValueError as exc:
        print(exc)
        upload_log()
    except Exception as exc:
       logger.exception(exc)
       logger.debug(exc)
       upload_log()
    
