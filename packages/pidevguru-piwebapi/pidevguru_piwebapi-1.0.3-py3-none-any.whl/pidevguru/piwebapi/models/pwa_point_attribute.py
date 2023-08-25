from pprint import pformat
from six import iteritems


class PWAPointAttribute(object):
    swagger_types = {
        'links': 'PWAPointAttributeLinks',
        'name': 'str',
        'value': 'object',
        'web_exception': 'PWAWebException',
    }

    attribute_map = {
        'links': 'Links',
        'name': 'Name',
        'value': 'Value',
        'web_exception': 'WebException',
    }

    def __init__(self, links=None, name=None, value=None, web_exception=None):

        self._links = None
        self._name = None
        self._value = None
        self._web_exception = None

        if links is not None:
            self.links = links
        if name is not None:
            self.name = name
        if value is not None:
            self.value = value
        if web_exception is not None:
            self.web_exception = web_exception

    @property
    def links(self):
        return self._links

    @links.setter
    def links(self, links):
        self._links = links

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

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
        if not isinstance(other, PWAPointAttribute):
            return False
        return self.__dict__ == other.__dict__

