from pprint import pformat
from six import iteritems


class PWAAnalysisRule(object):
    swagger_types = {
        'config_string': 'str',
        'description': 'str',
        'display_string': 'str',
        'editor_type': 'str',
        'has_children': 'bool',
        'id': 'str',
        'is_configured': 'bool',
        'is_initializing': 'bool',
        'links': 'PWAAnalysisRuleLinks',
        'name': 'str',
        'path': 'str',
        'plug_in_name': 'str',
        'supported_behaviors': 'list[str]',
        'variable_mapping': 'str',
        'web_exception': 'PWAWebException',
        'web_id': 'str',
    }

    attribute_map = {
        'config_string': 'ConfigString',
        'description': 'Description',
        'display_string': 'DisplayString',
        'editor_type': 'EditorType',
        'has_children': 'HasChildren',
        'id': 'Id',
        'is_configured': 'IsConfigured',
        'is_initializing': 'IsInitializing',
        'links': 'Links',
        'name': 'Name',
        'path': 'Path',
        'plug_in_name': 'PlugInName',
        'supported_behaviors': 'SupportedBehaviors',
        'variable_mapping': 'VariableMapping',
        'web_exception': 'WebException',
        'web_id': 'WebId',
    }

    def __init__(self, config_string=None, description=None, display_string=None, editor_type=None, has_children=None, id=None, is_configured=None, is_initializing=None, links=None, name=None, path=None, plug_in_name=None, supported_behaviors=None, variable_mapping=None, web_exception=None, web_id=None):

        self._config_string = None
        self._description = None
        self._display_string = None
        self._editor_type = None
        self._has_children = None
        self._id = None
        self._is_configured = None
        self._is_initializing = None
        self._links = None
        self._name = None
        self._path = None
        self._plug_in_name = None
        self._supported_behaviors = None
        self._variable_mapping = None
        self._web_exception = None
        self._web_id = None

        if config_string is not None:
            self.config_string = config_string
        if description is not None:
            self.description = description
        if display_string is not None:
            self.display_string = display_string
        if editor_type is not None:
            self.editor_type = editor_type
        if has_children is not None:
            self.has_children = has_children
        if id is not None:
            self.id = id
        if is_configured is not None:
            self.is_configured = is_configured
        if is_initializing is not None:
            self.is_initializing = is_initializing
        if links is not None:
            self.links = links
        if name is not None:
            self.name = name
        if path is not None:
            self.path = path
        if plug_in_name is not None:
            self.plug_in_name = plug_in_name
        if supported_behaviors is not None:
            self.supported_behaviors = supported_behaviors
        if variable_mapping is not None:
            self.variable_mapping = variable_mapping
        if web_exception is not None:
            self.web_exception = web_exception
        if web_id is not None:
            self.web_id = web_id

    @property
    def config_string(self):
        return self._config_string

    @config_string.setter
    def config_string(self, config_string):
        self._config_string = config_string

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def display_string(self):
        return self._display_string

    @display_string.setter
    def display_string(self, display_string):
        self._display_string = display_string

    @property
    def editor_type(self):
        return self._editor_type

    @editor_type.setter
    def editor_type(self, editor_type):
        self._editor_type = editor_type

    @property
    def has_children(self):
        return self._has_children

    @has_children.setter
    def has_children(self, has_children):
        self._has_children = has_children

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def is_configured(self):
        return self._is_configured

    @is_configured.setter
    def is_configured(self, is_configured):
        self._is_configured = is_configured

    @property
    def is_initializing(self):
        return self._is_initializing

    @is_initializing.setter
    def is_initializing(self, is_initializing):
        self._is_initializing = is_initializing

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
    def plug_in_name(self):
        return self._plug_in_name

    @plug_in_name.setter
    def plug_in_name(self, plug_in_name):
        self._plug_in_name = plug_in_name

    @property
    def supported_behaviors(self):
        return self._supported_behaviors

    @supported_behaviors.setter
    def supported_behaviors(self, supported_behaviors):
        self._supported_behaviors = supported_behaviors

    @property
    def variable_mapping(self):
        return self._variable_mapping

    @variable_mapping.setter
    def variable_mapping(self, variable_mapping):
        self._variable_mapping = variable_mapping

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
        if not isinstance(other, PWAAnalysisRule):
            return False
        return self.__dict__ == other.__dict__

