from pprint import pformat
from six import iteritems


class PWASystemLandingLinks(object):
    swagger_types = {
        'cache_instances': 'str',
        'configuration': 'str',
        'status': 'str',
        'user_info': 'str',
        'versions': 'str',
    }

    attribute_map = {
        'cache_instances': 'CacheInstances',
        'configuration': 'Configuration',
        'status': 'Status',
        'user_info': 'UserInfo',
        'versions': 'Versions',
    }

    def __init__(self, cache_instances=None, configuration=None, status=None, user_info=None, versions=None):

        self._cache_instances = None
        self._configuration = None
        self._status = None
        self._user_info = None
        self._versions = None

        if cache_instances is not None:
            self.cache_instances = cache_instances
        if configuration is not None:
            self.configuration = configuration
        if status is not None:
            self.status = status
        if user_info is not None:
            self.user_info = user_info
        if versions is not None:
            self.versions = versions

    @property
    def cache_instances(self):
        return self._cache_instances

    @cache_instances.setter
    def cache_instances(self, cache_instances):
        self._cache_instances = cache_instances

    @property
    def configuration(self):
        return self._configuration

    @configuration.setter
    def configuration(self, configuration):
        self._configuration = configuration

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def user_info(self):
        return self._user_info

    @user_info.setter
    def user_info(self, user_info):
        self._user_info = user_info

    @property
    def versions(self):
        return self._versions

    @versions.setter
    def versions(self, versions):
        self._versions = versions

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
        if not isinstance(other, PWASystemLandingLinks):
            return False
        return self.__dict__ == other.__dict__

