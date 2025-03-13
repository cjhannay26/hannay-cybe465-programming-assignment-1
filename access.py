import sys
from friend_management import FriendManager
from picture_management import PictureManager
from list_management import ListManager
from log import Logger

class MyFacebook:
    def __init__(self):
        self.profile_owner = None
        self.current_viewer = None
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

        elif instruction == "chmod": self.change_permissions(parts[1], parts[2:5])

        elif instruction == "chown": self.change_owner(parts[1], parts[2])

        elif instruction == "readcomments": self.read_comments(parts[1])
        
        elif instruction == "writecomments": self.write_comments(parts[1], ' '.join(parts[2:]))
        
        elif instruction == "end": self.end()

        else: self.logger.log_error(f"Invalid command: {command}")

    # Command handlers
    def friend_add(self, friend_name):
        if self.profile_owner is None:
            self.profile_owner = friend_name
        self.friends_manager.add_friend(friend_name, self.logger)
        self.logger.log_action(f"Friend {friend_name} added")

    def view_by(self, friend_name):
        # Handle viewing by friend
        if self.current_viewer is not None:
            self.logger.log_action("Login failed: simultaneous login not permitted")
            return
        
        if not self.friends_manager.is_friend(friend_name):
            self.logger.log_action(f"Login failed: invalid friend name")
            return
        
        self.current_viewer = friend_name
        self.logger.log_action(f"Friend {friend_name} views the profile")

    def logout(self):
        if not self.current_viewer:
            print("Error: No one is currently viewing the profile.")
            return
        self.logger.log_action(f"Friend {self.current_viewer} logged out")
        self.current_viewer = None

    def list_add(self, list_name):
        self.list_manager.add_list(list_name, self.logger)
        self.logger.log_action(f"List {list_name} added")

    def friend_list(self, friend_name, list_name):
        self.list_manager.add_friend_to_list(friend_name, list_name)
        self.logger.log_action(f"Friend {friend_name} added to list {list_name}")

    def post_picture(self, picture_name):
        if not self.current_viewer:
            return
        
        self.picture_manager.add_picture(picture_name, self.current_viewer)
        self.logger.log_action(f"Picture {picture_name} with owner {self.current_viewer} and default permissions created")

    def change_list(self, picture_name, list_name):
        self.picture_manager.change_list(picture_name, list_name)
        self.logger.log_action(f"List for {picture_name} set to {list_name} by {self.current_viewer}")

    def change_permissions(self, picture_name, permissions):
        self.picture_manager.change_permissions(picture_name, permissions)
        owner, list, others = permissions[:3]
        self.logger.log_action(f"Permissions for {picture_name} set to {owner} {list} {others} by {self.current_viewer}")

    def change_owner(self, picture_name, new_owner):
        self.picture_manager.change_owner(picture_name, new_owner)
        self.logger.log_action(f"Owner of {picture_name} changed to {new_owner}")

    def read_comments(self, picture_name):
        comment = self.picture_manager.read_comments(picture_name, self.current_viewer, self.logger, self.list_manager)
        if comment is not None:
            self.logger.log_action(f"Friend {self.current_viewer} reads {picture_name} as:\n{comment}")

    def write_comments(self, picture_name, comment_text):
        success = self.picture_manager.write_comments(picture_name, self.current_viewer, comment_text, self.logger, self.list_manager)
        if success:
            self.logger.log_action(f"Friend {self.current_viewer} wrote to {picture_name}: {comment_text}")

    def end(self):
        # Writing all data back to files
        self.friends_manager.save_to_file()
        self.list_manager.save_to_file()
        self.picture_manager.save_to_file()
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python access.py <commands_file>")
        sys.exit(1)

    facebook = MyFacebook()
    facebook.run(sys.argv[1])