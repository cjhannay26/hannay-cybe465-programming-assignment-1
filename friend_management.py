class FriendManager:
    def __init__(self, filename="friends.txt"):
        self.friends = set()
        self.filename = filename
        self.load_from_file()

    def add_friend(self, friend_name):
        self.friends.add(friend_name)
       
    def is_friend(self, friend_name):
        return friend_name in self.friends
    
    def load_from_file(self):
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    self.friends.add(line.strip())
        except FileNotFoundError:
            print(f"Warning: {self.filename} not found. Starting with an empty friend list.")

    def save_to_file(self):
        with open("friends.txt", 'a') as f:
            for friend in self.friends:
                f.write(friend + "\n")