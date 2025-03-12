from friend_management import FriendManager
from picture_management import PictureManager
from list_management import ListManager
from log import Logger

class MyFacebook:
    def __init__(self):
        self.profile_owner = None
        self.current_user = None
        self.friends_manager = FriendManager("friends.txt")
        self.picture_manager = PictureManager("pictures.txt")
        self.list_manager = ListManager("list.txt")
        self.logger = Logger()

    def run(self, filename):
        try:
            with open(filename, 'r') as file:
                commands = file.readlines()
                for command in commands:
                    self.execute_command(command.strip())

        except FileNotFoundError:
            self.logger.log_error(f"File {filename} not found")

        except Exception as e:
            self.logger.log_error(f"Unexpected error: {e}")

    def execute_command(self, command):
        parts = command.split()
        instruction = parts[0]

        if instruction == "friendadd": self.friend_add(parts[1])

        elif instruction == "viewby": self.view_by(parts[1])

        elif instruction == "logout": self.logout()
        
        elif instruction == "listadd": self.list_add(parts[1])
        
        elif instruction == "friendlist": self.friend_list(parts[1], parts[2])

        elif instruction == "postpicture": self.post_picture(parts[1])
        
        elif instruction == "chlst": self.change_list(parts[1], parts[2])

        elif instruction == "chmod": self.change_permissions(parts[1], parts[2:])

        elif instruction == "chown": self.change_owner(parts[1], parts[2])

        elif instruction == "readcomments": self.read_comments(parts[1])
        
        elif instruction == "writecomments": self.write_comments(parts[1], ''.join(parts[2:]))
        
        elif instruction == "end": self.end()

        else: self.logger.log_error(f"Invalid command: {command}")
