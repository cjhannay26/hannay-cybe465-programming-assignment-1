class ListManager:
    def __init__(self, filename="lists.txt"):
        # Initialize ListManager with a file name and an empty dictionary
        self.lists = {}
        self.filename = filename

        # Clear lists.txt file each time the program is run
        open(self.filename, 'w').close()

        # Load lists from the file
        self.load_from_file()

    def add_list(self, list_name):
        # Add a new list to the dictionary of lists with an empty set of friends associated with the list
        self.lists[list_name] = set()

    def add_friend_to_list(self, friend_name, list_name):
        # Add a friend into the set for a specified list
        self.lists[list_name].add(friend_name)

    def friend_in_list(self, friend_name, list_name):
        # Return whether or not a friend is in the list
        return list_name in self.lists and friend_name in self.lists[list_name]

    def load_from_file(self):
        # Load lists from the file
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    # Strip the newline and add each friend to the list
                    parts = line.strip().split()

                    # Extract the list name from the first part
                    list_name = parts[0]

                    # Extract the friends (as a set) from the remaining parts
                    members = set(parts[1:])

                    # Store the lists's data into the the lists dictionary
                    self.lists[list_name] = members
        except FileNotFoundError:
            # Handle the case for if the file does not exist
            print(f"Warning: {self.filename} not found. Starting with empty file {self.filename}")

    def save_to_file(self):
        # Save any created lists to lists.txt
        with open("lists.txt", 'w') as f:
            for list_name, members in self.lists.items():
                # Write each list to a new line in the file with format list_name: friend1 friend2
                f.write(f"{list_name}: {' '.join(members)}\n")