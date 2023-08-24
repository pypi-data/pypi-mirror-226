from pprint import pformat
from six import iteritems


class PWAItemEventFrame(object):
    swagger_types = {
        'exception': 'PWAErrors',
        'identifier': 'str',
        'identifier_type': 'str',
        'object': 'PWAEventFrame',
    }

    attribute_map = {
        'exception': 'Exception',
        'identifier': 'Identifier',
        'identifier_type': 'IdentifierType',
        'object': 'Object',
    }

    def __init__(self, exception=None, identifier=None, identifier_type=None, object=None):

        self._exception = None
        self._identifier = None
        self._identifier_type = None
        self._object = None

        if exception is not None:
            self.exception = exception
        if identifier is not None:
            self.identifier = identifier
        if identifier_type is not None:
            self.identifier_type = identifier_type
        if object is not None:
            self.object = object

    @property
    def exception(self):
        return self._exception

    @exception.setter
    def exception(self, exception):
        self._exception = exception

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        self._identifier = identifier

    @property
    def identifier_type(self):
        return self._identifier_type

    @identifier_type.setter
    def identifier_type(self, identifier_type):
        self._identifier_type = identifier_type

    @property
    def object(self):
        return self._object

    @object.setter
    def object(self, object):
        self._object = object

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
        if not isinstance(other, PWAItemEventFrame):
            return False
        return self.__dict__ == other.__dict__

