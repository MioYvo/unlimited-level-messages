"""
flaskr.utils.check_input
~~~~~~~~~~~~~~~~~~~~~~~~
Utilities for checking input data.
"""
import re

email_pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
username_pattern = re.compile(r"^[a-zA-Z\d]{5,20}$")
password_pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,20}")


def check_input(target: str, pattern):
    if re.match(pattern, target):
        return target
    else:
        return False
