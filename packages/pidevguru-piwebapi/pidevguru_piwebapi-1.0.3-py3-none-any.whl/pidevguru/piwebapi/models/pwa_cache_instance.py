from pprint import pformat
from six import iteritems


class PWACacheInstance(object):
    swagger_types = {
        'id': 'str',
        'last_refresh_time': 'str',
        'scheduled_expiration_time': 'str',
        'user': 'str',
        'web_exception': 'PWAWebException',
        'will_refresh_after': 'str',
    }

    attribute_map = {
        'id': 'Id',
        'last_refresh_time': 'LastRefreshTime',
        'scheduled_expiration_time': 'ScheduledExpirationTime',
        'user': 'User',
        'web_exception': 'WebException',
        'will_refresh_after': 'WillRefreshAfter',
    }

    def __init__(self, id=None, last_refresh_time=None, scheduled_expiration_time=None, user=None, web_exception=None, will_refresh_after=None):

        self._id = None
        self._last_refresh_time = None
        self._scheduled_expiration_time = None
        self._user = None
        self._web_exception = None
        self._will_refresh_after = None

        if id is not None:
            self.id = id
        if last_refresh_time is not None:
            self.last_refresh_time = last_refresh_time
        if scheduled_expiration_time is not None:
            self.scheduled_expiration_time = scheduled_expiration_time
        if user is not None:
            self.user = user
        if web_exception is not None:
            self.web_exception = web_exception
        if will_refresh_after is not None:
            self.will_refresh_after = will_refresh_after

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def last_refresh_time(self):
        return self._last_refresh_time

    @last_refresh_time.setter
    def last_refresh_time(self, last_refresh_time):
        self._last_refresh_time = last_refresh_time

    @property
    def scheduled_expiration_time(self):
        return self._scheduled_expiration_time

    @scheduled_expiration_time.setter
    def scheduled_expiration_time(self, scheduled_expiration_time):
        self._scheduled_expiration_time = scheduled_expiration_time

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    @property
    def web_exception(self):
        return self._web_exception

    @web_exception.setter
    def web_exception(self, web_exception):
        self._web_exception = web_exception

    @property
    def will_refresh_after(self):
        return self._will_refresh_after

    @will_refresh_after.setter
    def will_refresh_after(self, will_refresh_after):
        self._will_refresh_after = will_refresh_after

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
        if not isinstance(other, PWACacheInstance):
            return False
        return self.__dict__ == other.__dict__

