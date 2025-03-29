class FriendManager:
    def __init__(self, filename="friends.txt"):
        # Initialize FriendManager with a file name and an empty friend list
        self.friends = []
        self.filename = filename

        # Clear friends.txt file each time the program is run
        open(self.filename, 'w').close()

        # Load friends from the file
        self.load_from_file()

    def add_friend(self, friend_name):
        # Add a new friend to the list of friends
        self.friends.append(friend_name)
    
    def load_from_file(self):
        # Load friends from the file (one per line)
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    # Strip the newline and add each friend to the list
                    self.friends.append(line.strip())
        except FileNotFoundError:
            # Handle the case for if the file does not exist
            print(f"Warning: {self.filename} not found. Starting with empty file {self.filename}")

    def save_to_file(self):
        # Save any added friends to friends.txt
        with open("friends.txt", 'w') as f:
            for friend in self.friends:
                # Write each friend to a newline in the file
                f.write(friend + "\n")