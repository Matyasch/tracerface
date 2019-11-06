class Configuration:
    def __init__(
            self,
            bcc_command='trace-bpfcc',
            animate=False):
        self.bcc_command = bcc_command
        self.animate = animate

    def update(self, bcc_command, animate):
        self.bcc_command = bcc_command
        self.animate = animate
