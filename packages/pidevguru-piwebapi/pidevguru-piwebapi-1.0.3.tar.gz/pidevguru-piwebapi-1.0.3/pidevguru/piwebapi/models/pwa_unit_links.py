from pprint import pformat
from six import iteritems


class PWAUnitLinks(object):
    swagger_types = {
        'reference_unit': 'str',
    }

    attribute_map = {
        'reference_unit': 'ReferenceUnit',
    }

    def __init__(self, reference_unit=None):

        self._reference_unit = None

        if reference_unit is not None:
            self.reference_unit = reference_unit

    @property
    def reference_unit(self):
        return self._reference_unit

    @reference_unit.setter
    def reference_unit(self, reference_unit):
        self._reference_unit = reference_unit

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
        if not isinstance(other, PWAUnitLinks):
            return False
        return self.__dict__ == other.__dict__

