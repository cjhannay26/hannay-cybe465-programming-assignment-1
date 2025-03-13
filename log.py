class Logger:
    def __init__(self):
        # Initialize the log file path to "audit.txt"
        self.audit_log = "audit.txt"

    def log_action(self, action):
        # Log an action (success or error)
        with open(self.audit_log, 'a') as f:
            f.write(f"{action}\n")