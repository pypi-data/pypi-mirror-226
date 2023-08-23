import datetime
import json
import secrets

from babel.support import LazyProxy

from viber import types
import re

DEFAULT_FILTER = ['self', 'cls']


def generate_payload(exclude=None, **kwargs):
    """
    Generate payload

    Usage: payload = generate_payload(**locals(), exclude=['foo'])

    :param exclude:
    :param kwargs:
    :return: dict
    """
    if exclude is None:
        exclude = []
    return {key: value for key, value in kwargs.items() if
            key not in exclude + DEFAULT_FILTER
            and value is not None
            and not key.startswith('_')}


def _normalize(obj):
    """
    Normalize dicts and lists

    :param obj:
    :return: normalized object
    """
    if isinstance(obj, list):
        return [_normalize(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: _normalize(v) for k, v in obj.items() if v is not None}
    elif hasattr(obj, 'to_python'):
        return obj.to_python()
    return obj


def prepare_arg(value):
    """
    Stringify dicts/lists and convert datetime/timedelta to unix-time

    :param value:
    :return:
    """
    if value is None:
        return value
    if isinstance(value, (list, dict)) or hasattr(value, 'to_python'):
        return json.dumps(_normalize(value))
    if isinstance(value, datetime.timedelta):
        now = datetime.datetime.now()
        return int((now + value).timestamp())
    if isinstance(value, datetime.datetime):
        return round(value.timestamp())
    if isinstance(value, LazyProxy):
        return str(value)
    return value


def prepare_file(payload, files, key, file):
    if isinstance(file, str):
        payload[key] = file
    elif file is not None:
        files[key] = file


def prepare_attachment(payload, files, key, file):
    if isinstance(file, str):
        payload[key] = file
    elif isinstance(file, types.InputFile):
        payload[key] = file.attach
        files[file.attachment_key] = file.file
    elif file is not None:
        file_attach_name = secrets.token_urlsafe(16)
        payload[key] = "attach://" + file_attach_name
        files[file_attach_name] = file


def html_to_md(html_text: str):
    html_text = re.sub(r'<b>(.*?)</b>', r'*\1*', html_text)
    html_text = re.sub(r'<i>(.*?)</i>', r'_\1_', html_text)
    html_text = re.sub(r'<s>(.*?)</s>', r'~\1~', html_text)
    html_text = re.sub(r'<pre>(.*?)</pre>', r'```\1```', html_text)
    html_text = re.sub(r'\*:', r'* :', html_text)
    html_text = re.sub(r':\*', r': *', html_text)

    return html_text


def get_md_text(text: str, parse_mode: str = None):
    if parse_mode == types.ParseMode.HTML:
        text = html_to_md(text)
    return text
