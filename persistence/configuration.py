class Configuration:
    def __init__(
            self, bcc_command='trace-bpfcc',
            animate=False, spacing=2):
        self.bcc_command = bcc_command
        self.animate = animate
        self.spacing = spacing

    def update(self, bcc_command, animate, spacing):
        self.bcc_command = bcc_command
        self.animate = animate
        self.spacing = spacing
