class PictureManager:
    def __init__(self, filename="pictures.txt"):
        # Initialize PictureManager with a file name and en empty dictionary
        self.pictures = {}
        self.filename = filename

        # Clear pictures.txt file each time the program is run
        open(self.filename, 'w').close()

        # Load pictures from the file
        self.load_from_file()

    def add_picture(self, picture_name, owner):
        # Add/post a picture with the default list ('nil') and default permissions
        self.pictures[picture_name] = {
            'owner': owner,
            'list': 'nil',
            'permissions': {'owner': 'rw', 'list': '--', 'others': '--'},
        }

        # Create a new file for the posted picture with the name of the picture on the first line
        with open(picture_name, 'w') as picture:
            picture.write(f"{picture_name.rsplit(".txt", 1)[0]}\n")

    def change_list(self, picture_name, list_name):
         # Change the list for a given picture
        self.pictures[picture_name]['list'] = list_name

    def change_permissions(self, picture_name, permissions):
        # Change the read/write permissions for owner, list, and others for a given picture
        self.pictures[picture_name]['permissions'] = {
            'owner': permissions[0],
            'list': permissions[1],
            'others': permissions[2]
        }

    def change_owner(self, picture_name, new_owner):
        # Change the owner of a given picture
        self.pictures[picture_name]['owner'] = new_owner

    # Read in any comment(s) that have been written to a picture
    def read_comments(self, picture_name, viewer, list_manager):
        picture = self.pictures[picture_name]

        # Check owner permissions to determine whether to read comments from picture/file
        if viewer == picture['owner'] and picture['permissions']['owner'][0] == 'r':
            with open(picture_name, 'r') as picture:
                # Read the comment from the picture
                return picture.read().strip()
                
        # Check to make sure the associated list is not the default 'nil' and that the friend is in the list
        if picture['list'] != 'nil' and list_manager.friend_in_list(viewer, picture['list']):
            # Check list permissions to determine whether to read comments from picture/file
            if picture['permissions']['list'][0] == 'r':
                with open(picture_name, 'r') as picture:
                    # Read the comment from the picture
                    return picture.read().strip()

        # Check others permissions to determine whether to read comments from picture/file
        if picture['permissions']['others'][0] == 'r':
            with open(picture_name, 'r') as picture:
                # Read the comment from the picture
                return picture.read().strip()

        # Indicate that permission to read is denied
        return None

    # Write new comment(s) to the picture
    def write_comments(self, picture_name, viewer, comment, list_manager):
        picture = self.pictures[picture_name]
        
        # Check owner permissions to determine whether to write comment to picture/file
        if viewer == picture['owner'] and picture['permissions']['owner'][1] == 'w':
            with open(picture_name, 'a') as picture:
                # Append the comment into the picture file
                picture.write(comment + "\n")
            return True
        
        # Check to make sure the associated list is not the default 'nil' and that the friend is in the list
        if picture['list'] != 'nil' and list_manager.friend_in_list(viewer, picture['list']): 
            # Check list permissions to determine whether to write comment to picture/file
            if picture['permissions']['list'][1] == 'w':
                with open(picture_name, 'a') as picture:
                    # Append the comment into the picture file
                    picture.write(comment + "\n")
                return True

        # Check others permissions to determine whether to write comment to picture/file
        if picture['permissions']['others'][1] == 'w':
            with open(picture_name, 'a') as picture:
                # Append the comment into the picture file
                picture.write(comment + "\n")
            return True
        
        # Indicate that permission to write is denied
        return False

    def load_from_file(self):
        # Load pictures from the file
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    # Strip the newline and add each friend to the list
                    parts = line.strip().split()

                    # Extract picture name,  owner, and list from first three parts
                    pic_name = parts[0]
                    owner = parts[1]
                    list_name = parts[2]

                    # Extract permissions for owner, list, and others from remaining parts
                    permissions = {'owner': parts[3], 'list': parts[4], 'others': parts[5]}

                    # Store the picutre's data into the the pictures dictionary
                    self.pictures[pic_name] = {'owner': owner, 'list': list_name, 'permissions': permissions}
        except FileNotFoundError:
            # Handle the case for if the file does not exist
            print(f"Warning: {self.filename} not found. Starting with empty file {self.filename}")

    
    def save_to_file(self):
        # Save any posted/created pictures to pictures.txt
        with open("pictures.txt", 'w') as f:
            for pic, data in self.pictures.items():
                # Write each picture to a new line in the file wiht the format: picture_name: owner list owner_permissions list_permissions others_permissions
                f.write(f"{pic}: {data['owner']} {data['list']} {data['permissions']['owner']} {data['permissions']['list']} {data['permissions']['others']}\n")