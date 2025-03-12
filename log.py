class Logger:
    def __init__(self):
        self.audit_log = "audit.txt"

    def log_action(self, action):
        with open(self.audit_log, 'a') as f:
            f.write(f"{action}\n")

    def log_error(self, error):
        with open(self.audit_log, 'a') as f:
            f.write(f"{error}\n")