# Saving the settings for the application
class Configuration:
    def __init__(self, animate=True, spacing=2):
        self._animate = animate
        self._spacing = spacing

    def update_layout(self, animate, spacing):
        if spacing < 1:
            raise ValueError('Spacing can not be less than 1')
        self._animate = animate
        self._spacing = spacing

    def get_spacing(self):
        return self._spacing

    def get_animate(self):
        return self._animate
