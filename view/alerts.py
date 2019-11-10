from dash_bootstrap_components import Alert

#base alerts
def base_success_alert(message):
    return Alert(message, color='success', duration=4000, dismissable=True)

def base_error_alert(message):
    return Alert(message, color='danger', duration=4000, dismissable=True)

#application add alerts
def empty_app_name_alert():
    return base_error_alert('Please provide an application name')

def app_already_added_alert():
    return base_error_alert('Application already added')

def add_app_success_alert(app):
    return Alert('{} was added successfully'.format(app), color='success', duration=4000, dismissable=True)

#manage app alerts
def no_app_selected_alert():
    return base_error_alert('Please select an application first')

#add function alerts
def empty_function_name_alert():
    return base_error_alert('Please provide a function name')

def function_already_added_alert():
    return base_error_alert('Function already added to this application')

def func_add_success_alert():
    return base_success_alert('Function successfully added')

#manage function alert
def no_func_selected_alert():
    return base_error_alert('Please select a function first')

#add parameter alerts
def no_param_type_alert():
    return base_error_alert('Please provide the type of the parameter')

def no_param_index_alert():
    return base_error_alert('Please provide the position of the parameter')

def param_already_added_alert():
    return base_error_alert('Parameter already added to this position')

def param_add_success_alert():
    return base_success_alert('Parameter successfully added')

#manage parameter alerts:
def no_param_selected_alert():
    return base_error_alert('Please select a parameter first')

#trace alerts
def trace_error_alert(error):
    return Alert([html.P('There was an error with tracing'), html.P(error)], color='danger', duration=6000, dismissable=True)

#load output alerts
def load_output_success_alert():
    return base_success_alert('Output loaded')

def output_empty_alert():
    return base_error_alert('Please provide the output of a BCC trace run')

#configuration save alerts
def save_config_success_alert():
    return base_success_alert('Configuration saved!')

def empty_command_config_alert():
    return base_success_alert('Please provide a command')