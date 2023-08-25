from pprint import pformat
from six import iteritems


class PWASubstatus(object):
    swagger_types = {
        'message': 'str',
        'substatus': 'int',
        'web_exception': 'PWAWebException',
    }

    attribute_map = {
        'message': 'Message',
        'substatus': 'Substatus',
        'web_exception': 'WebException',
    }

    def __init__(self, message=None, substatus=None, web_exception=None):

        self._message = None
        self._substatus = None
        self._web_exception = None

        if message is not None:
            self.message = message
        if substatus is not None:
            self.substatus = substatus
        if web_exception is not None:
            self.web_exception = web_exception

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        self._message = message

    @property
    def substatus(self):
        return self._substatus

    @substatus.setter
    def substatus(self, substatus):
        self._substatus = substatus

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
        if not isinstance(other, PWASubstatus):
            return False
        return self.__dict__ == other.__dict__

