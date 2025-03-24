class PictureManager:
    def __init__(self, filename="pictures.txt"):
        self.pictures = {}
        self.filename = filename
        self.load_from_file()

    # Add/post a picture with the default list ('nil') and default permissions
    def add_picture(self, picture_name, owner):
        self.pictures[picture_name] = {
            'owner': owner,
            'list': 'nil',
            'permissions': {'owner': 'rw', 'list': '--', 'others': '--'},
        }

        with open(picture_name, 'w') as picture:
            picture.write(f"{picture_name.rsplit(".txt", 1)[0]}\n")

    # Change the list for a given picture
    def change_list(self, picture_name, list_name):
        self.pictures[picture_name]['list'] = list_name

    # Change the read/write permissions for owner, list, and others for a given picture
    def change_permissions(self, picture_name, permissions):
        self.pictures[picture_name]['permissions'] = {
            'owner': permissions[0],
            'list': permissions[1],
            'others': permissions[2]
        }

    # Change the owner of a given picture
    def change_owner(self, picture_name, new_owner):
        self.pictures[picture_name]['owner'] = new_owner

    # Read in any comment(s) that have been written to a picture
    def read_comments(self, picture_name, viewer, list_manager):
        picture = self.pictures[picture_name]

        # Check owner permissions to determine whether to read comment from picture/file
        if viewer == picture['owner'] and picture['permissions']['owner'][0] == 'r':
            with open(picture_name, 'r') as picture:
                return picture.read().strip()
                
        # Check list permissions to determine whether to read comment from picture/file
        if picture['list'] != 'nil' and list_manager.friend_in_list(viewer, picture['list']):
            if picture['permissions']['list'][0] == 'r':
                with open(picture_name, 'r') as picture:
                    return picture.read().strip()

        # Check others permissions to determine whether to read comment from picture/file
        if picture['permissions']['others'][0] == 'r':
            with open(picture_name, 'r') as picture:
                return picture.read().strip()

        return None

    # Write new comment(s) to the picture
    def write_comments(self, picture_name, viewer, comment, list_manager):
        picture = self.pictures[picture_name]
        
        # Check owner permissions to determine whether to write comment to picture/file
        if viewer == picture['owner'] and picture['permissions']['owner'][1] == 'w':
            with open(picture_name, 'a') as picture:
                picture.write(comment + "\n")
            return True
        
        # Check lists permissions to determine whether to write comment to picture/file
        if picture['list'] != 'nil' and list_manager.friend_in_list(viewer, picture['list']): 
            if picture['permissions']['list'][1] == 'w':
                with open(picture_name, 'a') as picture:
                    picture.write(comment + "\n")
                return True

        # Check others permissions to determine whether to write comment to picture/file
        if picture['permissions']['others'][1] == 'w':
            with open(picture_name, 'a') as picture:
                picture.write(comment + "\n")
            return True
        
        # Indicate that permission to write is denied
        return False

    def load_from_file(self):
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    pic_name = parts[0]
                    owner = parts[1]
                    list_name = parts[2]
                    permissions = {'owner': parts[3], 'list': parts[4], 'others': parts[5]}
                    self.pictures[pic_name] = {'owner': owner, 'list': list_name, 'permissions': permissions}
        except FileNotFoundError:
            print(f"Warning: {self.filename} not found. Starting with empty file {self.filename}")

    # Save any posted/created pictures to pictures.txt
    def save_to_file(self):
        with open("pictures.txt", 'a') as f:
            for pic, data in self.pictures.items():
                f.write(f"{pic}: {data['owner']} {data['list']} {data['permissions']['owner']} {data['permissions']['list']} {data['permissions']['others']}\n")
            f.close()