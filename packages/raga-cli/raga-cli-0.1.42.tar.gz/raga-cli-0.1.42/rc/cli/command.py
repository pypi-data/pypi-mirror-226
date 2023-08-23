import logging
import os
from abc import ABC, abstractmethod

from rc.utils.config import ConfigManager
from rc.utils.request import get_all_config

logger = logging.getLogger(__name__)


class CmdBase(ABC):
    def __init__(self, args):
        self.args = args
        self.config = ConfigManager(get_all_config())
    def do_run(self):
        return self.run()
            
    @abstractmethod
    def run(self):
        pass


