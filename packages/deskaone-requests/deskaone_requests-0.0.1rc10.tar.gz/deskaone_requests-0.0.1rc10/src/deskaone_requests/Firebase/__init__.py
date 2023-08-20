from pyrebase.pyrebase import Firebase as FB

class Firebase(FB):
    
    def __init__(self, config: dict):
        super().__init__(config)