class ListManager:
    def __init__(self, filename="lists.txt"):
        self.lists = {}
        self.filename = filename
        self.load_from_file()

    def add_list(self, list_name):
        if list_name in self.lists or list_name == 'nil':
            print(f"Error: List '{list_name}' already exists or is reserved.")
            return
        self.lists[list_name] = set()

    def add_friend_to_list(self, friend_name, list_name):
        if list_name not in self.lists:
            print(f"Error: List '{list_name}' does not exist.")
            return
        if not friend_name in self.lists:
            print(f"Error: Friend '{friend_name}' does not exist.")
            return
        self.lists[list_name].add(friend_name)

    def load_from_file(self):
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    list_name = parts[0]
                    members = set(parts[1:])
                    self.lists[list_name] = members
        except FileNotFoundError:
            print(f"Warning: {self.filename} not found. Starting with an empty list.")

    def save_to_file(self):
        with open("lists.txt", 'a') as f:
            for list_name, members in self.lists.items():
                f.write(f"{list_name} {' '.join(members)}\n")