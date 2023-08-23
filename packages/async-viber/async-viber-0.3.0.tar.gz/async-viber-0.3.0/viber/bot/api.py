import json
import logging

import aiohttp
from aiogram.utils.helper import Helper, HelperMode, Item

from viber.utils import exceptions

# Main aioviber2 logger
log = logging.getLogger('aioviber2')

VIBER_BOT_API_URL = "https://chatapi.viber.com/pa"


def check_result(method_name: str, content_type: str, request_data: dict, body: str) -> dict:
    """
    Checks whether result is a valid API response.
    A result is considered invalid if:
    - The content of the result is invalid JSON.
    - The method call was unsuccessful (The JSON 'status' field not equals 0)

    :param method_name: The name of the method called
    :param content_type: content type of result
    :param request_data: request_data
    :param body: result body
    :return: The result parsed to a JSON dictionary
    :raises ViberApiError: if one of the above listed cases is applicable
    """
    log.debug('Response for %s: "%r"', method_name, body)

    if content_type != 'application/json':
        raise exceptions.NetworkError(f'Invalid response with content type {content_type}: "{body}"')

    result_json: dict = json.loads(body)

    if (status := result_json['status']) == 0:
        return {k: v for k, v in result_json.items() if k not in ['status', 'status_message']}

    status_message = result_json.get('status_message')
    error = exceptions.ViberApiError(method_name, request_data, status, status_message)
    error.detect()


async def make_request(session, token, method, data=None, **kwargs):
    log.debug('Make request: "%s" with data: "%r"', method, data)

    url = f'{VIBER_BOT_API_URL}/{method}'
    headers = {'X-Viber-Auth-Token': token}

    try:
        async with session.post(url, json=data, headers=headers, **kwargs) as response:
            return check_result(method, response.content_type, data, await response.text())
    except aiohttp.ClientError as e:
        raise exceptions.NetworkError(f"aiohttp client throws an error: {e.__class__.__name__}: {e}")


class Methods(Helper):
    """
    Helper for Viber API Methods listed on https://developers.viber.com/docs/api/rest-bot-api/
    """

    mode = HelperMode.snake_case

    SET_WEBHOOK = Item()
    SEND_MESSAGE = Item()
    BROADCAST_MESSAGE = Item()
    GET_ACCOUNT_INFO = Item()
    GET_USER_DETAILS = Item()
    GET_ONLINE = Item()
