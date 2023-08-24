from pprint import pformat
from six import iteritems


class PWAAssetServer(object):
    swagger_types = {
        'description': 'str',
        'extended_properties': 'dict(str, PWAValue)',
        'id': 'str',
        'is_connected': 'bool',
        'links': 'PWAAssetServerLinks',
        'name': 'str',
        'path': 'str',
        'server_time': 'str',
        'server_version': 'str',
        'web_exception': 'PWAWebException',
        'web_id': 'str',
    }

    attribute_map = {
        'description': 'Description',
        'extended_properties': 'ExtendedProperties',
        'id': 'Id',
        'is_connected': 'IsConnected',
        'links': 'Links',
        'name': 'Name',
        'path': 'Path',
        'server_time': 'ServerTime',
        'server_version': 'ServerVersion',
        'web_exception': 'WebException',
        'web_id': 'WebId',
    }

    def __init__(self, description=None, extended_properties=None, id=None, is_connected=None, links=None, name=None, path=None, server_time=None, server_version=None, web_exception=None, web_id=None):

        self._description = None
        self._extended_properties = None
        self._id = None
        self._is_connected = None
        self._links = None
        self._name = None
        self._path = None
        self._server_time = None
        self._server_version = None
        self._web_exception = None
        self._web_id = None

        if description is not None:
            self.description = description
        if extended_properties is not None:
            self.extended_properties = extended_properties
        if id is not None:
            self.id = id
        if is_connected is not None:
            self.is_connected = is_connected
        if links is not None:
            self.links = links
        if name is not None:
            self.name = name
        if path is not None:
            self.path = path
        if server_time is not None:
            self.server_time = server_time
        if server_version is not None:
            self.server_version = server_version
        if web_exception is not None:
            self.web_exception = web_exception
        if web_id is not None:
            self.web_id = web_id

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def extended_properties(self):
        return self._extended_properties

    @extended_properties.setter
    def extended_properties(self, extended_properties):
        self._extended_properties = extended_properties

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def is_connected(self):
        return self._is_connected

    @is_connected.setter
    def is_connected(self, is_connected):
        self._is_connected = is_connected

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
    def server_time(self):
        return self._server_time

    @server_time.setter
    def server_time(self, server_time):
        self._server_time = server_time

    @property
    def server_version(self):
        return self._server_version

    @server_version.setter
    def server_version(self, server_version):
        self._server_version = server_version

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
        if not isinstance(other, PWAAssetServer):
            return False
        return self.__dict__ == other.__dict__

