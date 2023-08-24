from pprint import pformat
from six import iteritems


class PWAItemsstring(object):
    swagger_types = {
        'items': 'list[str]',
    }

    attribute_map = {
        'items': 'Items',
    }

    def __init__(self, items=None):

        self._items = None

        if items is not None:
            self.items = items

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, items):
        self._items = items

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
        if not isinstance(other, PWAItemsstring):
            return False
        return self.__dict__ == other.__dict__

