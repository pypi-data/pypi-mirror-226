from pprint import pformat
from six import iteritems


class PWAElementTemplate(object):
    swagger_types = {
        'allow_element_to_extend': 'bool',
        'base_template': 'str',
        'can_be_acknowledged': 'bool',
        'category_names': 'list[str]',
        'description': 'str',
        'extended_properties': 'dict(str, PWAValue)',
        'id': 'str',
        'instance_type': 'str',
        'links': 'PWAElementTemplateLinks',
        'name': 'str',
        'naming_pattern': 'str',
        'path': 'str',
        'severity': 'str',
        'web_exception': 'PWAWebException',
        'web_id': 'str',
    }

    attribute_map = {
        'allow_element_to_extend': 'AllowElementToExtend',
        'base_template': 'BaseTemplate',
        'can_be_acknowledged': 'CanBeAcknowledged',
        'category_names': 'CategoryNames',
        'description': 'Description',
        'extended_properties': 'ExtendedProperties',
        'id': 'Id',
        'instance_type': 'InstanceType',
        'links': 'Links',
        'name': 'Name',
        'naming_pattern': 'NamingPattern',
        'path': 'Path',
        'severity': 'Severity',
        'web_exception': 'WebException',
        'web_id': 'WebId',
    }

    def __init__(self, allow_element_to_extend=None, base_template=None, can_be_acknowledged=None, category_names=None, description=None, extended_properties=None, id=None, instance_type=None, links=None, name=None, naming_pattern=None, path=None, severity=None, web_exception=None, web_id=None):

        self._allow_element_to_extend = None
        self._base_template = None
        self._can_be_acknowledged = None
        self._category_names = None
        self._description = None
        self._extended_properties = None
        self._id = None
        self._instance_type = None
        self._links = None
        self._name = None
        self._naming_pattern = None
        self._path = None
        self._severity = None
        self._web_exception = None
        self._web_id = None

        if allow_element_to_extend is not None:
            self.allow_element_to_extend = allow_element_to_extend
        if base_template is not None:
            self.base_template = base_template
        if can_be_acknowledged is not None:
            self.can_be_acknowledged = can_be_acknowledged
        if category_names is not None:
            self.category_names = category_names
        if description is not None:
            self.description = description
        if extended_properties is not None:
            self.extended_properties = extended_properties
        if id is not None:
            self.id = id
        if instance_type is not None:
            self.instance_type = instance_type
        if links is not None:
            self.links = links
        if name is not None:
            self.name = name
        if naming_pattern is not None:
            self.naming_pattern = naming_pattern
        if path is not None:
            self.path = path
        if severity is not None:
            self.severity = severity
        if web_exception is not None:
            self.web_exception = web_exception
        if web_id is not None:
            self.web_id = web_id

    @property
    def allow_element_to_extend(self):
        return self._allow_element_to_extend

    @allow_element_to_extend.setter
    def allow_element_to_extend(self, allow_element_to_extend):
        self._allow_element_to_extend = allow_element_to_extend

    @property
    def base_template(self):
        return self._base_template

    @base_template.setter
    def base_template(self, base_template):
        self._base_template = base_template

    @property
    def can_be_acknowledged(self):
        return self._can_be_acknowledged

    @can_be_acknowledged.setter
    def can_be_acknowledged(self, can_be_acknowledged):
        self._can_be_acknowledged = can_be_acknowledged

    @property
    def category_names(self):
        return self._category_names

    @category_names.setter
    def category_names(self, category_names):
        self._category_names = category_names

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
    def instance_type(self):
        return self._instance_type

    @instance_type.setter
    def instance_type(self, instance_type):
        self._instance_type = instance_type

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
    def naming_pattern(self):
        return self._naming_pattern

    @naming_pattern.setter
    def naming_pattern(self, naming_pattern):
        self._naming_pattern = naming_pattern

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def severity(self):
        return self._severity

    @severity.setter
    def severity(self, severity):
        self._severity = severity

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
        if not isinstance(other, PWAElementTemplate):
            return False
        return self.__dict__ == other.__dict__

