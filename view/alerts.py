from dash_bootstrap_components import Alert
from dash_html_components import P


#base alerts
class BaseAlert(Alert):
    def __init__(self, message, color):
        super().__init__(message, color=color, duration=4000, dismissable=True)

class SuccessAlert(BaseAlert):
    def __init__(self, message):
        super().__init__(message=message, color='success')

class ErrorAlert(BaseAlert):
    def __init__(self, message):
        super().__init__(message=message, color='danger')

#application add alerts
def app_already_added_alert():
    return ErrorAlert('Application already added')

def add_app_success_alert(app):
    return Alert('{} was added successfully'.format(app), color='success', duration=4000, dismissable=True)

def empty_app_name_alert():
    return ErrorAlert('Please provide an application name')

#manage app alerts
def no_app_selected_alert():
    return ErrorAlert('Please select an application first')

#add function alerts
def empty_function_name_alert():
    return ErrorAlert('Please provide a function name')

def function_already_added_alert():
    return ErrorAlert('Function already added to this application')

def func_add_success_alert():
    return SuccessAlert('Function successfully added')

#manage function alert
def no_func_selected_alert():
    return ErrorAlert('Please select a function first')

#add parameter alerts
def no_param_type_alert():
    return ErrorAlert('Please provide the type of the parameter')

def no_param_index_alert():
    return ErrorAlert('Please provide the position of the parameter')

def param_already_added_alert():
    return ErrorAlert('Parameter already added to this position')

def param_add_success_alert():
    return SuccessAlert('Parameter successfully added')

#manage parameter alerts:
def no_param_selected_alert():
    return ErrorAlert('Please select a parameter first')

#trace alerts
def trace_error_alert(error):
    return Alert([P('There was an error with tracing'), P(error)], color='danger', duration=6000, dismissable=True)

#load output alerts
def load_output_success_alert():
    return SuccessAlert('Output loaded')

def output_empty_alert():
    return ErrorAlert('Please provide the output of a BCC trace run')

#configuration save alerts
def empty_command_config_alert():
    return ErrorAlert('Please provide a command')

def save_config_success_alert():
    return SuccessAlert('Configuration saved!')