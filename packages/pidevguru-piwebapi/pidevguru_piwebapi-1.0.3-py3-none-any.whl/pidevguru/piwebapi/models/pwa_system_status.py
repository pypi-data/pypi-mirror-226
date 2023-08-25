from pprint import pformat
from six import iteritems


class PWASystemStatus(object):
    swagger_types = {
        'cache_instances': 'int',
        'server_time': 'str',
        'state': 'str',
        'up_time_in_minutes': 'float',
        'web_exception': 'PWAWebException',
    }

    attribute_map = {
        'cache_instances': 'CacheInstances',
        'server_time': 'ServerTime',
        'state': 'State',
        'up_time_in_minutes': 'UpTimeInMinutes',
        'web_exception': 'WebException',
    }

    def __init__(self, cache_instances=None, server_time=None, state=None, up_time_in_minutes=None, web_exception=None):

        self._cache_instances = None
        self._server_time = None
        self._state = None
        self._up_time_in_minutes = None
        self._web_exception = None

        if cache_instances is not None:
            self.cache_instances = cache_instances
        if server_time is not None:
            self.server_time = server_time
        if state is not None:
            self.state = state
        if up_time_in_minutes is not None:
            self.up_time_in_minutes = up_time_in_minutes
        if web_exception is not None:
            self.web_exception = web_exception

    @property
    def cache_instances(self):
        return self._cache_instances

    @cache_instances.setter
    def cache_instances(self, cache_instances):
        self._cache_instances = cache_instances

    @property
    def server_time(self):
        return self._server_time

    @server_time.setter
    def server_time(self, server_time):
        self._server_time = server_time

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    @property
    def up_time_in_minutes(self):
        return self._up_time_in_minutes

    @up_time_in_minutes.setter
    def up_time_in_minutes(self, up_time_in_minutes):
        self._up_time_in_minutes = up_time_in_minutes

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
        if not isinstance(other, PWASystemStatus):
            return False
        return self.__dict__ == other.__dict__

