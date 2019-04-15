class InvalidMail(Exception):
    
    def __init__(self):
        super().__init__()
        self.message = 'Invalid mail. It should be like name@example.com'
