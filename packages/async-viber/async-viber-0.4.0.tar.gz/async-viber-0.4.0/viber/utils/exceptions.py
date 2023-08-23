class AiogramViberioError(Exception):
    pass


class AiogramViberioWarning(Warning):
    pass


class TimeoutWarning(AiogramViberioWarning):
    pass


class FSMStorageWarning(AiogramViberioWarning):
    pass


class ValidationError(AiogramViberioError):
    pass


# class Throttled(AiogramViberioError):
#     def __init__(self, **kwargs):
#         from ..dispatcher.storage import DELTA, EXCEEDED_COUNT, KEY, LAST_CALL, RATE_LIMIT, RESULT
#         self.key = kwargs.pop(KEY, '<None>')
#         self.called_at = kwargs.pop(LAST_CALL, time.time())
#         self.rate = kwargs.pop(RATE_LIMIT, None)
#         self.result = kwargs.pop(RESULT, False)
#         self.exceeded_count = kwargs.pop(EXCEEDED_COUNT, 0)
#         self.delta = kwargs.pop(DELTA, 0)
#         self.user = kwargs.pop('user', None)
#         self.chat = kwargs.pop('chat', None)
#
#     def __str__(self):
#         return f"Rate limit exceeded! (Limit: {self.rate} s, " \
#                f"exceeded: {self.exceeded_count}, " \
#                f"time delta: {round(self.delta, 3)} s)"


# === ===

class NetworkError(Exception):
    pass


class ViberApiError(Exception):
    def __init__(self, method: str, payload: dict, status, status_message: str):
        self.method = method
        self.payload = payload
        self.status = status
        self.status_message = status_message or 'Unknown error'

    def __str__(self):
        return f'Failed request "{self.method}" with body: {self.payload} ' \
               f'[status: {self.status}, description: {self.status_message}]'

    def detect(self):
        for exc in ViberApiError.__subclasses__():
            if self.status == getattr(exc, 'status', None):
                raise exc(self.method, self.payload, self.status, self.status_message)
        else:
            raise GeneralError(self.method, self.payload, self.status, self.status_message)


class InvalidUrl(ViberApiError):
    status = 1


class InvalidAuthToken(ViberApiError):
    status = 2


class BadData(ViberApiError):
    status = 3


class MissingData(ViberApiError):
    status = 4


class ReceiverNotRegistered(ViberApiError):
    status = 5


class ReceiverNotSubscribed(ViberApiError):
    status = 6


class PublicAccountBlocked(ViberApiError):
    status = 7


class PublicAccountNotFound(ViberApiError):
    status = 8


class PublicAccountSuspended(ViberApiError):
    status = 9


class WebhookNotSet(ViberApiError):
    status = 10


class ReceiverNoSuitableDevice(ViberApiError):
    status = 11


class TooManyRequests(ViberApiError):
    status = 12


class ApiVersionNotSupported(ViberApiError):
    status = 13


class IncompatibleWithVersion(ViberApiError):
    status = 14


class PublicAccountNotAuthorized(ViberApiError):
    status = 15


class InchatReplyMessageNotAllowed(ViberApiError):
    status = 16


class PublicAccountIsNotInline(ViberApiError):
    status = 17


class NoPublicChat(ViberApiError):
    status = 18


class CannotSendBroadcast(ViberApiError):
    status = 19


class BroadcastNotAllowed(ViberApiError):
    status = 20


class GeneralError(ViberApiError):
    status = 'other'
