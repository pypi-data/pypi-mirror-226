from pprint import pformat
from six import iteritems


class PWAChannelInstance(object):
    swagger_types = {
        'id': 'str',
        'last_message_sent_time': 'str',
        'sent_message_count': 'int',
        'start_time': 'str',
        'web_exception': 'PWAWebException',
    }

    attribute_map = {
        'id': 'Id',
        'last_message_sent_time': 'LastMessageSentTime',
        'sent_message_count': 'SentMessageCount',
        'start_time': 'StartTime',
        'web_exception': 'WebException',
    }

    def __init__(self, id=None, last_message_sent_time=None, sent_message_count=None, start_time=None, web_exception=None):

        self._id = None
        self._last_message_sent_time = None
        self._sent_message_count = None
        self._start_time = None
        self._web_exception = None

        if id is not None:
            self.id = id
        if last_message_sent_time is not None:
            self.last_message_sent_time = last_message_sent_time
        if sent_message_count is not None:
            self.sent_message_count = sent_message_count
        if start_time is not None:
            self.start_time = start_time
        if web_exception is not None:
            self.web_exception = web_exception

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def last_message_sent_time(self):
        return self._last_message_sent_time

    @last_message_sent_time.setter
    def last_message_sent_time(self, last_message_sent_time):
        self._last_message_sent_time = last_message_sent_time

    @property
    def sent_message_count(self):
        return self._sent_message_count

    @sent_message_count.setter
    def sent_message_count(self, sent_message_count):
        self._sent_message_count = sent_message_count

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time

    @property
    def web_exception(self):
        return self._web_exception

    @web_exception.setter
    def web_exception(self, web_exception):
        self._web_exception = web_exception

    def to_dict(self):
        result = {}
        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        return result

    def to_str(self):
        return pformat(self.to_dict())

    def __repr__(self):
        return self.to_str()

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        if not isinstance(other, PWAChannelInstance):
            return False
        return self.__dict__ == other.__dict__

