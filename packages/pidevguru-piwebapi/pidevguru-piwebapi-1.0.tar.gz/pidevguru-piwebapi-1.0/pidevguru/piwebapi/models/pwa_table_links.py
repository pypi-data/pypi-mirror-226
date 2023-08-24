from pprint import pformat
from six import iteritems


class PWATableLinks(object):
    swagger_types = {
        'categories': 'str',
        'data': 'str',
        'database': 'str',
        'security': 'str',
        'security_entries': 'str',
    }

    attribute_map = {
        'categories': 'Categories',
        'data': 'Data',
        'database': 'Database',
        'security': 'Security',
        'security_entries': 'SecurityEntries',
    }

    def __init__(self, categories=None, data=None, database=None, security=None, security_entries=None):

        self._categories = None
        self._data = None
        self._database = None
        self._security = None
        self._security_entries = None

        if categories is not None:
            self.categories = categories
        if data is not None:
            self.data = data
        if database is not None:
            self.database = database
        if security is not None:
            self.security = security
        if security_entries is not None:
            self.security_entries = security_entries

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, categories):
        self._categories = categories

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

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
        if not isinstance(other, PWATableLinks):
            return False
        return self.__dict__ == other.__dict__

