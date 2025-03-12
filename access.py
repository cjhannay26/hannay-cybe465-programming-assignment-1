import sys
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

    # Command handlers
    def friend_add(self, friend_name):
        if not self.profile_owner:
            print("Error: Profile owner must be created first.")
            self.logger.log_error("Error: Profile owner must be created first.")
            return
        self.friends_manager.add_friend(friend_name)
        print(f"Friend '{friend_name}' added.")
        self.logger.log_action(f"Friend '{friend_name}' added.")

    def view_by(self, friend_name):
        # Handle viewing by friend
        if self.current_viewer:
            print(f"Error: {self.current_viewer} is already viewing the profile.")
            return
        if not self.friends_manager.is_friend(friend_name):
            print(f"Error: {friend_name} is not a friend.")
            return
        self.current_viewer = friend_name
        print(f"{friend_name} is now viewing the profile.")
        self.logger.log_action(f"{friend_name} is now viewing the profile.")

    def logout(self):
        if not self.current_viewer:
            print("Error: No one is currently viewing the profile.")
            return
        print(f"{self.current_viewer} has logged out.")
        self.logger.log_action(f"{self.current_viewer} has logged out.")
        self.current_viewer = None

    def list_add(self, list_name):
        self.list_manager.add_list(list_name)
        print(f"List '{list_name}' added.")
        self.logger.log_action(f"List '{list_name}' added.")

    def friend_list(self, friend_name, list_name):
        self.list_manager.add_friend_to_list(friend_name, list_name)
        print(f"Added {friend_name} to list '{list_name}'.")
        self.logger.log_action(f"Added {friend_name} to list '{list_name}'.")

    def post_picture(self, picture_name):
        if not self.current_viewer:
            print("Error: No one is viewing the profile.")
            return
        self.picture_manager.add_picture(picture_name, self.current_viewer)
        print(f"Picture '{picture_name}' posted by {self.current_viewer}.")
        self.logger.log_action(f"Picture '{picture_name}' posted by {self.current_viewer}.")

    def change_list(self, picture_name, list_name):
        self.picture_manager.change_list(picture_name, list_name)
        print(f"List of picture '{picture_name}' changed to '{list_name}'.")
        self.logger.log_action(f"List of picture '{picture_name}' changed to '{list_name}'.")

    def change_permissions(self, picture_name, permissions):
        self.picture_manager.change_permissions(picture_name, permissions)
        print(f"Permissions for picture '{picture_name}' changed.")
        self.logger.log_action(f"Permissions for picture '{picture_name}' changed.")

    def change_owner(self, picture_name, new_owner):
        self.picture_manager.change_owner(picture_name, new_owner)
        print(f"Owner of picture '{picture_name}' changed to {new_owner}.")
        self.logger.log_action(f"Owner of picture '{picture_name}' changed to {new_owner}.")

    def read_comments(self, picture_name):
        comments = self.picture_manager.read_comments(picture_name)
        print(f"Comments for picture '{picture_name}':\n{comments}")
        self.logger.log_action(f"Read comments for picture '{picture_name}'.")

    def write_comments(self, picture_name, comment_text):
        self.picture_manager.write_comment(picture_name, comment_text)
        print(f"Comment added to picture '{picture_name}': {comment_text}")
        self.logger.log_action(f"Comment added to picture '{picture_name}': {comment_text}.")

    def end(self):
        # Writing all data back to files
        self.friends_manager.save_to_file()
        self.list_manager.save_to_file()
        self.picture_manager.save_to_file()
        print("End of commands. Data saved.")
        self.logger.log_action("End of commands. Data saved.")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python access.py <commands_file>")
        sys.exit(1)

    facebook = MyFacebook()
    facebook.run(sys.argv[1])