from pprint import pformat
from six import iteritems


class PWAPropertyError(object):
    swagger_types = {
        'field_name': 'str',
        'message': 'list[str]',
    }

    attribute_map = {
        'field_name': 'FieldName',
        'message': 'Message',
    }

    def __init__(self, field_name=None, message=None):

        self._field_name = None
        self._message = None

        if field_name is not None:
            self.field_name = field_name
        if message is not None:
            self.message = message

    @property
    def field_name(self):
        return self._field_name

    @field_name.setter
    def field_name(self, field_name):
        self._field_name = field_name

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        self._message = message

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
        if not isinstance(other, PWAPropertyError):
            return False
        return self.__dict__ == other.__dict__

