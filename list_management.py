class ListManager:
    def __init__(self, filename="lists.txt"):
        self.lists = {}
        self.filename = filename

        # Clear lists.txt file each time the program is run
        open(self.filename, 'w').close()

        self.load_from_file()

    def add_list(self, list_name):
        self.lists[list_name] = set()

    def add_friend_to_list(self, friend_name, list_name):
        self.lists[list_name].add(friend_name)

    # Return whether a friend is in the list
    def friend_in_list(self, friend_name, list_name):
        return list_name in self.lists and friend_name in self.lists[list_name]

    def load_from_file(self):
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    list_name = parts[0]
                    members = set(parts[1:])
                    self.lists[list_name] = members
        except FileNotFoundError:
            print(f"Warning: {self.filename} not found. Starting with empty file {self.filename}")

    # Save any created lists to lists.txt
    def save_to_file(self):
        with open("lists.txt", 'w') as f:
            for list_name, members in self.lists.items():
                f.write(f"{list_name}: {' '.join(members)}\n")