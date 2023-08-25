from pprint import pformat
from six import iteritems


class PWAWebException(object):
    swagger_types = {
        'errors': 'list[str]',
        'status_code': 'int',
    }

    attribute_map = {
        'errors': 'Errors',
        'status_code': 'StatusCode',
    }

    def __init__(self, errors=None, status_code=None):

        self._errors = None
        self._status_code = None

        if errors is not None:
            self.errors = errors
        if status_code is not None:
            self.status_code = status_code

    @property
    def errors(self):
        return self._errors

    @errors.setter
    def errors(self, errors):
        self._errors = errors

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, status_code):
        self._status_code = status_code

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
        if not isinstance(other, PWAWebException):
            return False
        return self.__dict__ == other.__dict__

