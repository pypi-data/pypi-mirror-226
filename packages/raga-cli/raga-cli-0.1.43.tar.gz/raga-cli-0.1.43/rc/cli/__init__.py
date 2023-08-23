import logging
import os
import subprocess
from rc.cli.utils import RctlValidSubprocessError, log_setup, upload_log
from rc.utils.config import ConfigKeyNotFoundError
from rc.utils.request import RctlValidRequestError, get_config_value_by_key

logger = logging.getLogger(__name__)


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
    for tool in ['gh', 'git']:
        try:
            subprocess.run([tool, '--version'], capture_output=True, text=True, check=True)
        except OSError:
            raise RctlError(f'rc: error: {tool} not found! Please install {tool}')

def main(argv=None):
    try:
        log_setup()
        valid_requirement()
        args = parse_args(argv)
        cmd = args.func(args)
        cmd.do_run()
        upload_log()
    except KeyboardInterrupt as exc:
        logger.debug(exc)
        upload_log()
    except (RctlValidRequestError, RctlValidSubprocessError, RctlError, ValueError, ConfigKeyNotFoundError) as exc:
        print(exc.msg)
        upload_log()
    except Exception as exc:
       logger.exception(exc)
       logger.debug(exc)
       upload_log()
    
