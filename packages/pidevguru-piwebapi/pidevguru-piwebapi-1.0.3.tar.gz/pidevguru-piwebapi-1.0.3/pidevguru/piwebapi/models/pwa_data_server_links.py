from pprint import pformat
from six import iteritems


class PWADataServerLinks(object):
    swagger_types = {
        'enumeration_sets': 'str',
        'points': 'str',
    }

    attribute_map = {
        'enumeration_sets': 'EnumerationSets',
        'points': 'Points',
    }

    def __init__(self, enumeration_sets=None, points=None):

        self._enumeration_sets = None
        self._points = None

        if enumeration_sets is not None:
            self.enumeration_sets = enumeration_sets
        if points is not None:
            self.points = points

    @property
    def enumeration_sets(self):
        return self._enumeration_sets

    @enumeration_sets.setter
    def enumeration_sets(self, enumeration_sets):
        self._enumeration_sets = enumeration_sets

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = points

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
        if not isinstance(other, PWADataServerLinks):
            return False
        return self.__dict__ == other.__dict__

