from dash_bootstrap_components import Alert
from dash_html_components import P


#base alerts
class BaseAlert(Alert):
    def __init__(self, message, color):
        super().__init__(message, color=color, duration=4000, dismissable=True)


# Style for alerts singaling success
class SuccessAlert(BaseAlert):
    def __init__(self, message):
        super().__init__(message=message, color='success')


# Style for alerts singaling error
class ErrorAlert(BaseAlert):
    def __init__(self, message):
        super().__init__(message=message, color='danger')


# Style for alerts singaling error
class WarningAlert(BaseAlert):
    def __init__(self, message):
        super().__init__(message=message, color='warning')


def add_app_success_alert(item):
    return SuccessAlert('Application added')


def load_setup_success_alert(item):
    return SuccessAlert('Setup loaded')


# Alert(s) for tracing
def trace_error_alert(error):
    return Alert([P('There was an error with tracing'), P(error)],
                 color='danger', duration=6000, dismissable=True)


# Alert(s) for static output
def load_output_success_alert():
    return SuccessAlert('Output loaded')


def output_empty_alert():
    return ErrorAlert('Please provide the output of a BCC trace run')


# Alert(s) for configuration
def empty_command_config_alert():
    return ErrorAlert('Please provide a command')


def save_config_success_alert():
    return SuccessAlert('Configuration saved')