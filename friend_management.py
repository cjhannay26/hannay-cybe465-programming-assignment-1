class FriendManager:
    def __init__(self, filename="friends.txt"):
        self.friends = []
        self.filename = filename

        # Clear friends.txt file each time the program is run
        open(self.filename, 'w').close()

        self.load_from_file()

    def add_friend(self, friend_name):
        self.friends.append(friend_name)
    
    def load_from_file(self):
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    self.friends.append(line.strip())
        except FileNotFoundError:
            print(f"Warning: {self.filename} not found. Starting with empty file {self.filename}")

    # Save any added friends to friends.txt
    def save_to_file(self):
        with open("friends.txt", 'w') as f:
            for friend in self.friends:
                f.write(friend + "\n")