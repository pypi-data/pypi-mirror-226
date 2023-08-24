from pprint import pformat
from six import iteritems


class PWAEnumerationSetLinks(object):
    swagger_types = {
        'data_server': 'str',
        'database': 'str',
        'security': 'str',
        'security_entries': 'str',
        'values': 'str',
    }

    attribute_map = {
        'data_server': 'DataServer',
        'database': 'Database',
        'security': 'Security',
        'security_entries': 'SecurityEntries',
        'values': 'Values',
    }

    def __init__(self, data_server=None, database=None, security=None, security_entries=None, values=None):

        self._data_server = None
        self._database = None
        self._security = None
        self._security_entries = None
        self._values = None

        if data_server is not None:
            self.data_server = data_server
        if database is not None:
            self.database = database
        if security is not None:
            self.security = security
        if security_entries is not None:
            self.security_entries = security_entries
        if values is not None:
            self.values = values

    @property
    def data_server(self):
        return self._data_server

    @data_server.setter
    def data_server(self, data_server):
        self._data_server = data_server

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database):
        self._database = database

    @property
    def security(self):
        return self._security

    @security.setter
    def security(self, security):
        self._security = security

    @property
    def security_entries(self):
        return self._security_entries

    @security_entries.setter
    def security_entries(self, security_entries):
        self._security_entries = security_entries

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, values):
        self._values = values

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
        if not isinstance(other, PWAEnumerationSetLinks):
            return False
        return self.__dict__ == other.__dict__

