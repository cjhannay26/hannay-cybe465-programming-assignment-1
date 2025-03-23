class Logger:
    def __init__(self, filename="audit.txt"):
       self.filename = filename
       # Clear audit.txt file each time the program is run
       open(self.filename, 'w').close()

    def log_action(self, action):
        # Log an action (success or error)
        with open(self.filename, 'a') as f:
            f.write(f"{action}\n")