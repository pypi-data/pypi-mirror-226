from pprint import pformat
from six import iteritems


class PWAResponse(object):
    swagger_types = {
        'content': 'object',
        'headers': 'dict(str, str)',
        'status': 'int',
    }

    attribute_map = {
        'content': 'Content',
        'headers': 'Headers',
        'status': 'Status',
    }

    def __init__(self, content=None, headers=None, status=None):

        self._content = None
        self._headers = None
        self._status = None

        if content is not None:
            self.content = content
        if headers is not None:
            self.headers = headers
        if status is not None:
            self.status = status

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, headers):
        self._headers = headers

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

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
        if not isinstance(other, PWAResponse):
            return False
        return self.__dict__ == other.__dict__

