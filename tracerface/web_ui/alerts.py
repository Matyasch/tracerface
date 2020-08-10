from dash_bootstrap_components import Alert
from dash_html_components import P


# Parent class for all kinds of alerts
class BaseAlert(Alert):
    def __init__(self, message, color):
        super().__init__(message, color=color, duration=4000, dismissable=True)


# Style for alerts singaling success
class SuccessAlert(BaseAlert):
    def __init__(self, message):
        super().__init__(message=message, color='success')


# Style for alerts singaling errors
class ErrorAlert(BaseAlert):
    def __init__(self, message):
        super().__init__(message=message, color='danger')


# Style for alerts singaling warnings
class WarningAlert(BaseAlert):
    def __init__(self, message):
        super().__init__(message=message, color='warning')


# Special long error for tracing alerts
class TraceErrorAlert(Alert):
    def __init__(self, error):
        super().__init__(
            [P('There was an error with tracing:'), P(error)],
            color='danger', duration=6000, dismissable=True
        )
