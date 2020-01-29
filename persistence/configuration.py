# Saving the settings for the application
class Configuration:
    def __init__(
            self, bcc_command='trace-bpfcc',
            animate=True, spacing=2):
        self._bcc_command = bcc_command
        self._animate = animate
        self._spacing = spacing

    def update_command(self, bcc_command):
        self._bcc_command = bcc_command

    def update_layout(self, animate, spacing):
        if spacing < 1:
            raise ValueError('Spacing can not be less than 1')
        self._animate = animate
        self._spacing = spacing

    def get_spacing(self):
        return self._spacing

    def get_animate(self):
        return self._animate

    def get_command(self):
        return self._bcc_command
