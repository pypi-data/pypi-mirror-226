from pprint import pformat
from six import iteritems


class PWAUserInfo(object):
    swagger_types = {
        'identity_type': 'str',
        'impersonation_level': 'str',
        'is_authenticated': 'bool',
        'name': 'str',
        's_i_d': 'str',
        'web_exception': 'PWAWebException',
    }

    attribute_map = {
        'identity_type': 'IdentityType',
        'impersonation_level': 'ImpersonationLevel',
        'is_authenticated': 'IsAuthenticated',
        'name': 'Name',
        's_i_d': 'SID',
        'web_exception': 'WebException',
    }

    def __init__(self, identity_type=None, impersonation_level=None, is_authenticated=None, name=None, s_i_d=None, web_exception=None):

        self._identity_type = None
        self._impersonation_level = None
        self._is_authenticated = None
        self._name = None
        self._s_i_d = None
        self._web_exception = None

        if identity_type is not None:
            self.identity_type = identity_type
        if impersonation_level is not None:
            self.impersonation_level = impersonation_level
        if is_authenticated is not None:
            self.is_authenticated = is_authenticated
        if name is not None:
            self.name = name
        if s_i_d is not None:
            self.s_i_d = s_i_d
        if web_exception is not None:
            self.web_exception = web_exception

    @property
    def identity_type(self):
        return self._identity_type

    @identity_type.setter
    def identity_type(self, identity_type):
        self._identity_type = identity_type

    @property
    def impersonation_level(self):
        return self._impersonation_level

    @impersonation_level.setter
    def impersonation_level(self, impersonation_level):
        self._impersonation_level = impersonation_level

    @property
    def is_authenticated(self):
        return self._is_authenticated

    @is_authenticated.setter
    def is_authenticated(self, is_authenticated):
        self._is_authenticated = is_authenticated

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def s_i_d(self):
        return self._s_i_d

    @s_i_d.setter
    def s_i_d(self, s_i_d):
        self._s_i_d = s_i_d

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
        if not isinstance(other, PWAUserInfo):
            return False
        return self.__dict__ == other.__dict__

