import base64
from datetime import datetime
from django.contrib import messages
from django.utils.translation import ugettext


def base64_encode_time_now(string: str = None):
    time = datetime.timestamp(datetime.now())
    bytes_result = (string + str(time)).encode('ascii') if string is not None else str(time).encode('ascii')
    base64_bytes = base64.b64encode(bytes_result)
    return base64_bytes.decode('ascii')


def throw_form_errors_as_message(request, form):
    for field in form:
        for error in field.errors:
            messages.error(request, ugettext(field.label) + ': ' + error.lower())
