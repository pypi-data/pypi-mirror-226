from pprint import pformat
from six import iteritems


class PWAElement(object):
    swagger_types = {
        'category_names': 'list[str]',
        'description': 'str',
        'errors': 'list[PWAPropertyError]',
        'extended_properties': 'dict(str, PWAValue)',
        'has_children': 'bool',
        'id': 'str',
        'links': 'PWAElementLinks',
        'name': 'str',
        'path': 'str',
        'paths': 'list[str]',
        'template_name': 'str',
        'web_exception': 'PWAWebException',
        'web_id': 'str',
    }

    attribute_map = {
        'category_names': 'CategoryNames',
        'description': 'Description',
        'errors': 'Errors',
        'extended_properties': 'ExtendedProperties',
        'has_children': 'HasChildren',
        'id': 'Id',
        'links': 'Links',
        'name': 'Name',
        'path': 'Path',
        'paths': 'Paths',
        'template_name': 'TemplateName',
        'web_exception': 'WebException',
        'web_id': 'WebId',
    }

    def __init__(self, category_names=None, description=None, errors=None, extended_properties=None, has_children=None, id=None, links=None, name=None, path=None, paths=None, template_name=None, web_exception=None, web_id=None):

        self._category_names = None
        self._description = None
        self._errors = None
        self._extended_properties = None
        self._has_children = None
        self._id = None
        self._links = None
        self._name = None
        self._path = None
        self._paths = None
        self._template_name = None
        self._web_exception = None
        self._web_id = None

        if category_names is not None:
            self.category_names = category_names
        if description is not None:
            self.description = description
        if errors is not None:
            self.errors = errors
        if extended_properties is not None:
            self.extended_properties = extended_properties
        if has_children is not None:
            self.has_children = has_children
        if id is not None:
            self.id = id
        if links is not None:
            self.links = links
        if name is not None:
            self.name = name
        if path is not None:
            self.path = path
        if paths is not None:
            self.paths = paths
        if template_name is not None:
            self.template_name = template_name
        if web_exception is not None:
            self.web_exception = web_exception
        if web_id is not None:
            self.web_id = web_id

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
    def errors(self):
        return self._errors

    @errors.setter
    def errors(self, errors):
        self._errors = errors

    @property
    def extended_properties(self):
        return self._extended_properties

    @extended_properties.setter
    def extended_properties(self, extended_properties):
        self._extended_properties = extended_properties

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
    def paths(self):
        return self._paths

    @paths.setter
    def paths(self, paths):
        self._paths = paths

    @property
    def template_name(self):
        return self._template_name

    @template_name.setter
    def template_name(self, template_name):
        self._template_name = template_name

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
        if not isinstance(other, PWAElement):
            return False
        return self.__dict__ == other.__dict__

