
from dotenv import load_dotenv
import os
load_dotenv()

class _ProcessManager():
    
    def __init__(self):
        self._is_dev = os.getenv('DEV') == 'true'
        return
    
    def is_dev_mode(self):
        return self._is_dev
    

process_manager = _ProcessManager()
