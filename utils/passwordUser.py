from dataclasses import dataclass
from dotenv import load_dotenv
import os
@dataclass
class DataBaseMenu:

    def __post_init__(self):
        try:
            load_dotenv()
            self.passkey=os.getenv("PASS")
        except Exception as e:
            self.passkey=""
        

    
    def check_password(self,password):
        if self.passkey=="":
            return False
            
        if password == self.passkey:
            return True
        else:
            return False


