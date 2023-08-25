from pprint import pformat
from six import iteritems


class PWASecurityEntry(object):
    swagger_types = {
        'allow_rights': 'list[str]',
        'deny_rights': 'list[str]',
        'links': 'PWASecurityEntryLinks',
        'name': 'str',
        'security_identity_name': 'str',
        'web_exception': 'PWAWebException',
    }

    attribute_map = {
        'allow_rights': 'AllowRights',
        'deny_rights': 'DenyRights',
        'links': 'Links',
        'name': 'Name',
        'security_identity_name': 'SecurityIdentityName',
        'web_exception': 'WebException',
    }

    def __init__(self, allow_rights=None, deny_rights=None, links=None, name=None, security_identity_name=None, web_exception=None):

        self._allow_rights = None
        self._deny_rights = None
        self._links = None
        self._name = None
        self._security_identity_name = None
        self._web_exception = None

        if allow_rights is not None:
            self.allow_rights = allow_rights
        if deny_rights is not None:
            self.deny_rights = deny_rights
        if links is not None:
            self.links = links
        if name is not None:
            self.name = name
        if security_identity_name is not None:
            self.security_identity_name = security_identity_name
        if web_exception is not None:
            self.web_exception = web_exception

    @property
    def allow_rights(self):
        return self._allow_rights

    @allow_rights.setter
    def allow_rights(self, allow_rights):
        self._allow_rights = allow_rights

    @property
    def deny_rights(self):
        return self._deny_rights

    @deny_rights.setter
    def deny_rights(self, deny_rights):
        self._deny_rights = deny_rights

    @property
    def links(self):
        return self._links

    @links.setter
    def links(self, links):
        self._links = links

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def security_identity_name(self):
        return self._security_identity_name

    @security_identity_name.setter
    def security_identity_name(self, security_identity_name):
        self._security_identity_name = security_identity_name

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
        if not isinstance(other, PWASecurityEntry):
            return False
        return self.__dict__ == other.__dict__

