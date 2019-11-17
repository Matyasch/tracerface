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
        if spacing < 1:
            raise ValueError('Spacing can not be less than 1')
        self.animate = animate
        self.spacing = spacing
