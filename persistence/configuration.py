class Configuration:
    def __init__(
            self, bcc_command='trace-bpfcc',
            animate=True, spacing=2):
        self.bcc_command = bcc_command
        self.animate = animate
        self.spacing = spacing

    def update_command(self, bcc_command):
        self.bcc_command = bcc_command

    def update_layout(self, animate, spacing):
        self.animate = animate
        self.spacing = spacing
