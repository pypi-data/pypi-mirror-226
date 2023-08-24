from pprint import pformat
from six import iteritems


class PWASecurityMapping(object):
    swagger_types = {
        'account': 'str',
        'description': 'str',
        'id': 'str',
        'links': 'PWASecurityMappingLinks',
        'name': 'str',
        'path': 'str',
        'security_identity_web_id': 'str',
        'web_exception': 'PWAWebException',
        'web_id': 'str',
    }

    attribute_map = {
        'account': 'Account',
        'description': 'Description',
        'id': 'Id',
        'links': 'Links',
        'name': 'Name',
        'path': 'Path',
        'security_identity_web_id': 'SecurityIdentityWebId',
        'web_exception': 'WebException',
        'web_id': 'WebId',
    }

    def __init__(self, account=None, description=None, id=None, links=None, name=None, path=None, security_identity_web_id=None, web_exception=None, web_id=None):

        self._account = None
        self._description = None
        self._id = None
        self._links = None
        self._name = None
        self._path = None
        self._security_identity_web_id = None
        self._web_exception = None
        self._web_id = None

        if account is not None:
            self.account = account
        if description is not None:
            self.description = description
        if id is not None:
            self.id = id
        if links is not None:
            self.links = links
        if name is not None:
            self.name = name
        if path is not None:
            self.path = path
        if security_identity_web_id is not None:
            self.security_identity_web_id = security_identity_web_id
        if web_exception is not None:
            self.web_exception = web_exception
        if web_id is not None:
            self.web_id = web_id

    @property
    def account(self):
        return self._account

    @account.setter
    def account(self, account):
        self._account = account

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

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
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def security_identity_web_id(self):
        return self._security_identity_web_id

    @security_identity_web_id.setter
    def security_identity_web_id(self, security_identity_web_id):
        self._security_identity_web_id = security_identity_web_id

    @property
    def web_exception(self):
        return self._web_exception

    @web_exception.setter
    def web_exception(self, web_exception):
        self._web_exception = web_exception

    @property
    def web_id(self):
        return self._web_id

    @web_id.setter
    def web_id(self, web_id):
        self._web_id = web_id

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
        if not isinstance(other, PWASecurityMapping):
            return False
        return self.__dict__ == other.__dict__

