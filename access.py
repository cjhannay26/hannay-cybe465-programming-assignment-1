import sys
from friend_management import FriendManager
from picture_management import PictureManager
from list_management import ListManager
from log import Logger

class MyFacebook:
    def __init__(self):
        self.profile_owner = None
        self.current_viewer = None

        # Flag to keep track whether or not profile owner has viewed the profile
        self.profile_owner_has_viewed = False

        self.friends_manager = FriendManager("friends.txt")
        self.picture_manager = PictureManager("pictures.txt")
        self.list_manager = ListManager("lists.txt")
        self.logger = Logger()

    def run(self, filename):
        try:
            with open(filename, 'r') as file:
                commands = file.readlines()
                for command in commands:
                    self.execute_command(command.strip())

        except FileNotFoundError:
            self.logger.log_action(f"File {filename} not found")
            print(f"File {filename} not found")

        except Exception as e:
            self.logger.log_action(f"Unexpected error: {e}")
            print(f"Unexpected error: {e}")

    def execute_command(self, command):
        # Split each instruction/command into parts based on the space between command and arugments
        parts = command.split()

        # Set the actual instruction/command to be the first part
        instruction = parts[0]

        # Perform several checks to see which instruction should be executed
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

        else: 
            self.logger.log_action(f"Invalid command: {command}")
            print(f"Invalid command: {command}")

    def friend_add(self, friend_name):
        # Check whether the current viewer is the profile owner
        if self.current_viewer != self.profile_owner:
            self.logger.log_action(f"Error: only {self.profile_owner} may issue friendadd command")
            print(f"Error: only {self.profile_owner} may issue friendadd command")
            return
        
        # If there is no profile owner, set it to the first added friend
        if self.profile_owner is None:
            self.profile_owner = friend_name

        # Check to see if the friend already exists
        if friend_name in self.friends_manager.friends:
            self.logger.log_action(f"Error: Friend {friend_name} already exists")
            print(f"Error: Friend {friend_name} already exists")
            return

        # Add the friend and log the action
        self.friends_manager.add_friend(friend_name)
        self.logger.log_action(f"Friend {friend_name} added")
        print(f"Friend {friend_name} added")
        
    def view_by(self, friend_name):
        # Check to make sure the profile owner views first
        if not self.profile_owner_has_viewed and friend_name != self.profile_owner:
            self.logger.log_action(f"Error with viewby: profile owner must view profile first")
            print(f"Error with viewby: profile owner must view profile first")
            return

        # Check if there is already someone viewing profile to prevent simultaneous login
        if self.current_viewer is not None:
            self.logger.log_action("Login failed: simultaneous login not permitted")
            print("Login failed: simultaneous login not permitted")
            return
        
        # Check if the friend has been added
        if friend_name not in self.friends_manager.friends:
            self.logger.log_action(f"Login failed: invalid friend name")
            print(f"Login failed: invalid friend name")
            return
        
        # Indicate that the profile owner has viewed first/at least once
        if friend_name == self.profile_owner:
            self.profile_owner_has_viewed = True
            
        # Set the current viewer and log the action
        self.current_viewer = friend_name
        self.logger.log_action(f"Friend {friend_name} views the profile")
        print(f"Friend {friend_name} views the profile")

    def logout(self):
        # If no one is viewing the profile, log an error
        if not self.current_viewer:
            self.logger.log_action("Error: no one is currently viewing profile")
            print("Error: no one is currently viewing profile")
            return
        
        # Log the friend out (no viewer) and log the action
        self.logger.log_action(f"Friend {self.current_viewer} logged out")
        print(f"Friend {self.current_viewer} logged out")
        self.current_viewer = None

    def list_add(self, list_name):
        # If no one is viewing the profile, log an error
        if not self.current_viewer:
            self.logger.log_action("Error with listadd: no one is currently viewing profile")
            print("Error with listadd: no one is currently viewing profile")
            return
        
        # Check whether the current viewer is the profile owner
        if self.current_viewer != self.profile_owner:
            self.logger.log_action(f"Error: only {self.profile_owner} may issue listadd command")
            print(f"Error: only {self.profile_owner} may issue listadd command")
            return
        
        # Check to see if the list already exists (or it is 'nil')
        if list_name in self.list_manager.lists or list_name == 'nil':
            self.logger.log_action(f"Error: List {list_name} already exists")
            print(f"Error: List {list_name} already exists")
            return
        
        # Add the list and log the action
        self.list_manager.add_list(list_name)
        self.logger.log_action(f"List {list_name} added")
        print(f"List {list_name} added")

    def friend_list(self, friend_name, list_name):
        # If no one is viewing the profile, log an error
        if not self.current_viewer:
            self.logger.log_action("Error with friendlist: no one is currently viewing profile")
            print("Error with friendlist: no one is currently viewing profile")
            return
        
        # Check whether the current viewer is the profile owner
        if self.current_viewer != self.profile_owner:
            self.logger.log_action(f"Error: only {self.profile_owner} may issue friendlist command")
            print(f"Error: only {self.profile_owner} may issue friendlist command")
            return
        
        # Check to see if the list exists
        if list_name not in self.list_manager.lists:
            self.logger.log_action(f"Error with friendlist: list {list_name} not found")
            print(f"Error with friendlist: list {list_name} not found")
            return
        
        # Check to see if the friend exists
        if friend_name not in self.friends_manager.friends:
            self.logger.log_action(f"Error with friendlist: friend {friend_name} not found")
            print(f"Error with friendlist: friend {friend_name} not found")
            return
        
        # Add the friend to the list and log the action
        self.list_manager.add_friend_to_list(friend_name, list_name)
        self.logger.log_action(f"Friend {friend_name} added to list {list_name}")
        print(f"Friend {friend_name} added to list {list_name}")

    def post_picture(self, picture_name):
        # If no one is viewing the profile, log an error
        if not self.current_viewer:
            self.logger.log_action("Error: no one is currently viewing profile")
            print("Error: no one is currently viewing profile")
            return
        
        reserved_names = {"audit.txt", "friends.txt", "lists.txt", "pictures.txt"}

        if picture_name in reserved_names:
            self.logger.log_action(f"Error: invalid filename {picture_name}")
            print(f"Error: invalid filename {picture_name}")
            return
        
        # Check to see if the picture already exists
        if picture_name in self.picture_manager.pictures:
            self.logger.log_action(f"Error: picture {picture_name} already exists")
            print(f"Error: picture {picture_name} already exists")
            return
        
        # Post the picutre and log the action (including owner and default permissions)
        self.picture_manager.add_picture(picture_name, self.current_viewer)
        self.logger.log_action(f"Picture {picture_name} with owner {self.current_viewer} and default permissions created")
        print(f"Picture {picture_name} with owner {self.current_viewer} and default permissions created")

    def change_list(self, picture_name, list_name):
        # If no one is viewing the profile, log an error
        if not self.current_viewer:
            self.logger.log_action("Error with chlist: no one is currently viewing profile")
            print("Error with chlist: no one is currently viewing profile")
            return
        
        picture_owner = self.picture_manager.pictures[picture_name]['owner']

        # Check to make sure current viewer is profile owner or picture owner to determine if they can change list
        if self.current_viewer != self.profile_owner and self.current_viewer != picture_owner:
            self.logger.log_action("Error with chlist: only profile owner or picture owner can change the list")
            print("Error with chlist: only profile owner or picture owner can change the list")
            return
        
        # Check to see if the friend is in the list and if they are the profile owner
        if not self.list_manager.friend_in_list(self.current_viewer, list_name) and self.current_viewer != self.profile_owner:
            self.logger.log_action(f"Error with chlist: Friend {self.current_viewer} is not a member of list {list_name}")
            print(f"Error with chlist: Friend {self.current_viewer} is not a member of list {list_name}")
            return
        
        # If current viewer is not profile owner, they can only set list to "nil" or a list they belong to
        if self.current_viewer != self.profile_owner and list_name != "nil":
            if not self.list_manager.friend_in_list(self.current_viewer, list_name):
                self.logger.log_action(f"Error with chlish: friend {self.current_viewer} is not a member of list {list_name}")
                print(f"Error with chlish: friend {self.current_viewer} is not a member of list {list_name}")
                return
        
        # Check to see if the picture exists
        if picture_name not in self.picture_manager.pictures:
            self.logger.log_action(f"Error with chlist: picture {picture_name} not found")
            print(f"Error with chlist: picture {picture_name} not found")
            return
        
        # Check to see if the list exists
        if list_name not in self.list_manager.lists:
            self.logger.log_action(f"Error with chlist: list {list_name} not found")
            print(f"Error with chlist: list {list_name} not found")
            return
        
        self.picture_manager.change_list(picture_name, list_name)
        self.logger.log_action(f"List for {picture_name} set to {list_name} by {self.current_viewer}")
        print(f"List for {picture_name} set to {list_name} by {self.current_viewer}")

    def change_permissions(self, picture_name, permissions):
        # If no one is viewing the profile, log an error
        if not self.current_viewer:
            self.logger.log_action("Error with chmod: no one is currently viewing profile")
            print("Error with chmod: no one is currently viewing profile")
            return
        
        picture_owner = self.picture_manager.pictures[picture_name]['owner']

        # Check to make sure current viewer is profile owner or picture owner to determine if they can change list
        if self.current_viewer != self.profile_owner and self.current_viewer != picture_owner:
            self.logger.log_action("Error with chmod: only profile owner or picture owner can change permissions")
            print("Error with chmod: only profile owner or picture owner can change permissions")
            return
        
        # Check to see if the picture exists
        if picture_name not in self.picture_manager.pictures:
            self.logger.log_action(f"Error with chmod: picture {picture_name} not found")
            print(f"Error with chmod: picture {picture_name} not found")
            return
        
        self.picture_manager.change_permissions(picture_name, permissions)
        owner, list, others = permissions[:3]
        self.logger.log_action(f"Permissions for {picture_name} set to {owner} {list} {others} by {self.current_viewer}")
        print(f"Permissions for {picture_name} set to {owner} {list} {others} by {self.current_viewer}")

    def change_owner(self, picture_name, new_owner):
        # If no one is viewing the profile, log an error
        if not self.current_viewer:
            self.logger.log_action("Error with chown: no one is currently viewing profile")
            print("Error with chown: no one is currently viewing profile")
            return
        
        # Check whether the current viewer is the profile owner
        if self.current_viewer != self.profile_owner:
            self.logger.log_action(f"Error: only {self.profile_owner} may issue chown command")
            print(f"Error: only {self.profile_owner} may issue chown command")
            return
        
        # Check to see if the new owner exists as a friend
        if new_owner not in self.friends_manager.friends:
            self.logger.log_action(f"Error with chown: friend {new_owner} not found")
            print(f"Error with chown: friend {new_owner} not found")
            return
        
        # Check to see if the picture exists
        if picture_name not in self.picture_manager.pictures:
            self.logger.log_action(f"Error with chown: picture {picture_name} not found")
            print(f"Error with chown: picture {picture_name} not found")
            return
        
        self.picture_manager.change_owner(picture_name, new_owner)
        self.logger.log_action(f"Owner of {picture_name} changed to {new_owner}")
        print(f"Owner of {picture_name} changed to {new_owner}")

    def read_comments(self, picture_name):
        # If no one is viewing the profile, log an error
        if not self.current_viewer:
            self.logger.log_action("Error with readcomments: no one is currently viewing profile")
            print("Error with readcomments: no one is currently viewing profile")
            return
        
        # Check to see if the picture exists
        if picture_name not in self.picture_manager.pictures:
            self.logger.log_action(f"Error with readcomments: picture {picture_name} not found")
            print(f"Error with readcomments: picture {picture_name} not found")
            return
        
        comment = self.picture_manager.read_comments(picture_name, self.current_viewer, self.list_manager)

        if comment is not None:
            self.logger.log_action(f"Friend {self.current_viewer} reads {picture_name} as:\n{comment}")
            print(f"Friend {self.current_viewer} reads {picture_name} as:\n{comment}")
        else:
            self.logger.log_action(f"Friend {self.current_viewer} denied read access to {picture_name}")
            print(f"Friend {self.current_viewer} denied read access to {picture_name}")


    def write_comments(self, picture_name, comment_text):
        # If no one is viewing the profile, log an error
        if not self.current_viewer:
            self.logger.log_action("Error with writecomments: no one is currently viewing profile")
            print("Error with writecomments: no one is currently viewing profile")
            return
        
        # Check to see if the picture exists
        if picture_name not in self.picture_manager.pictures:
            self.logger.log_action(f"Error with writecomments: picture {picture_name} not found")
            print(f"Error with writecomments: picture {picture_name} not found")
            return
        
        success = self.picture_manager.write_comments(picture_name, self.current_viewer, comment_text, self.list_manager)
        
        if success:
            self.logger.log_action(f"Friend {self.current_viewer} wrote to {picture_name}: {comment_text}")
            print(f"Friend {self.current_viewer} wrote to {picture_name}: {comment_text}")
        else:
            self.logger.log_action(f"Friend {self.current_viewer} denied write access to {picture_name}")
            print(f"Friend {self.current_viewer} denied write access to {picture_name}")

    def end(self):
        # If no one is viewing the profile, log an error
        if not self.current_viewer:
            self.logger.log_action("Error with end: no one is currently viewing profile")
            print("Error with end: no one is currently viewing profile")
            return
        
        # Writing all data back to files
        self.friends_manager.save_to_file()
        self.list_manager.save_to_file()
        self.picture_manager.save_to_file()

        # Terminate the program
        sys.exit(0)

if __name__ == "__main__":
    # Check to see if script is being run properly and if the correct number of arguments are provided
    if len(sys.argv) != 2:
        # Print usage instructions if the number of arguments is not correct
        print("Usage Instruction: python access.py <commands_file>")
        sys.exit(1)

    # Create an instance of the MyFacebook class
    facebook = MyFacebook()

    # Run the instructions/commands by passing the provided command file as an argument
    facebook.run(sys.argv[1])