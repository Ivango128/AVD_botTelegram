class Users:
    def __init__(self):
        self.users = {}

    def add_user(self, chat_id):
        self.users[chat_id] = {
            'add_work_call' : None,
            'start_resume' : None
        }

