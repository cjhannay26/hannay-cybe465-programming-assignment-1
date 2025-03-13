class PictureManager:
    def __init__(self, filename="pictures.txt"):
        self.pictures = {}
        self.filename = filename
        self.load_from_file()

    def add_picture(self, picture_name, owner):
        if picture_name in self.pictures:
            print(f"Error: Picture '{picture_name}' already exists.")
            return
        self.pictures[picture_name] = {
            'owner': owner,
            'list': 'nil',
            'permissions': {'owner': 'rw', 'list': '--', 'others': '--'},
            'comments': []
        }

    def change_list(self, picture_name, list_name):
        if picture_name not in self.pictures:
            print(f"Error: Picture '{picture_name}' does not exist.")
            return
        self.pictures[picture_name]['list'] = list_name

    def change_permissions(self, picture_name, permissions):
        if picture_name not in self.pictures:
            print(f"Error: Picture '{picture_name}' does not exist.")
            return
        self.pictures[picture_name]['permissions'] = {
            'owner': permissions[0],
            'list': permissions[1],
            'others': permissions[2]
        }

    def change_owner(self, picture_name, new_owner):
        if picture_name not in self.pictures:
            print(f"Error: Picture '{picture_name}' does not exist.")
            return
        self.pictures[picture_name]['owner'] = new_owner

    def read_comments(self, picture_name, viewer, logger, list_manager):
        if picture_name not in self.pictures:
            print(f"Error: Picture '{picture_name}' does not exist.")
            return None
        
        picture = self.pictures[picture_name]

        if viewer == picture['owner'] or picture['permissions']['others'][0] == 'r':
            return "\n".join(picture['comments'])
        
        if picture['list'] in list_manager.lists and list_manager.friend_in_list(viewer, picture['list']):
            if picture['permissions']['list'][0] == 'r':
                return "\n".join(picture['comments'])

        logger.log_action(f"Friend {viewer} denied read access to {picture_name}")
        return None


    def write_comments(self, picture_name, viewer, comment, logger, list_manager):
        if picture_name not in self.pictures:
            print(f"Error: Picture '{picture_name}' does not exist.")
            return
        
        picture = self.pictures[picture_name]
        
        if viewer == picture['owner'] or picture['permissions']['others'][1] == 'w':
            picture['comments'].append(comment)
            return True
        
        if picture['list'] != 'nil' and picture['permissions']['list'][1] == 'w':
            if list_manager.friend_in_list(viewer, picture['list']):
                picture['comments'].append(comment)
                return True

        if picture['permissions']['others'][1] == 'w':
            picture['comments'].append(comment)
            return True
        
        logger.log_action(f"Friend {viewer} denied write access to {picture_name}")
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
                    self.pictures[pic_name] = {'owner': owner, 'list': list_name, 'permissions': permissions, 'comments': []}
        except FileNotFoundError:
            print(f"Warning: {self.filename} not found. Starting with an empty picture list.")

    def save_to_file(self):
        with open("pictures.txt", 'a') as f:
            for pic, data in self.pictures.items():
                f.write(f"{pic}: {data['owner']} {data['list']} {data['permissions']['owner']} {data['permissions']['list']} {data['permissions']['others']}\n")