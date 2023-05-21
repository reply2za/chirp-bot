
from dotenv import load_dotenv
import os
load_dotenv()

class _ProcessManager():
    
    def __init__(self):
        self._is_dev = os.getenv('DEV') == 'true'
        self._is_active = False
        return
    
    def is_dev_mode(self):
        return self._is_dev
    
    def is_active(self):
        return self._is_active
    
    def set_active(self, is_active: bool):
        self._is_active = is_active
        return
    
    def set_dev_mode(self, is_dev: bool):
        self._is_dev = is_dev
        return
    
    
    
    

process_manager = _ProcessManager()
