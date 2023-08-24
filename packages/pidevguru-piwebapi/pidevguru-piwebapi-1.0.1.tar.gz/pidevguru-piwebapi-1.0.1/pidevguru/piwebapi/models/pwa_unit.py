from pprint import pformat
from six import iteritems


class PWAUnit(object):
    swagger_types = {
        'abbreviation': 'str',
        'description': 'str',
        'factor': 'float',
        'id': 'str',
        'links': 'PWAUnitLinks',
        'name': 'str',
        'offset': 'float',
        'path': 'str',
        'reference_factor': 'float',
        'reference_offset': 'float',
        'reference_unit_abbreviation': 'str',
        'web_exception': 'PWAWebException',
        'web_id': 'str',
    }

    attribute_map = {
        'abbreviation': 'Abbreviation',
        'description': 'Description',
        'factor': 'Factor',
        'id': 'Id',
        'links': 'Links',
        'name': 'Name',
        'offset': 'Offset',
        'path': 'Path',
        'reference_factor': 'ReferenceFactor',
        'reference_offset': 'ReferenceOffset',
        'reference_unit_abbreviation': 'ReferenceUnitAbbreviation',
        'web_exception': 'WebException',
        'web_id': 'WebId',
    }

    def __init__(self, abbreviation=None, description=None, factor=None, id=None, links=None, name=None, offset=None, path=None, reference_factor=None, reference_offset=None, reference_unit_abbreviation=None, web_exception=None, web_id=None):

        self._abbreviation = None
        self._description = None
        self._factor = None
        self._id = None
        self._links = None
        self._name = None
        self._offset = None
        self._path = None
        self._reference_factor = None
        self._reference_offset = None
        self._reference_unit_abbreviation = None
        self._web_exception = None
        self._web_id = None

        if abbreviation is not None:
            self.abbreviation = abbreviation
        if description is not None:
            self.description = description
        if factor is not None:
            self.factor = factor
        if id is not None:
            self.id = id
        if links is not None:
            self.links = links
        if name is not None:
            self.name = name
        if offset is not None:
            self.offset = offset
        if path is not None:
            self.path = path
        if reference_factor is not None:
            self.reference_factor = reference_factor
        if reference_offset is not None:
            self.reference_offset = reference_offset
        if reference_unit_abbreviation is not None:
            self.reference_unit_abbreviation = reference_unit_abbreviation
        if web_exception is not None:
            self.web_exception = web_exception
        if web_id is not None:
            self.web_id = web_id

    @property
    def abbreviation(self):
        return self._abbreviation

    @abbreviation.setter
    def abbreviation(self, abbreviation):
        self._abbreviation = abbreviation

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def factor(self):
        return self._factor

    @factor.setter
    def factor(self, factor):
        self._factor = factor

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
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        self._offset = offset

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def reference_factor(self):
        return self._reference_factor

    @reference_factor.setter
    def reference_factor(self, reference_factor):
        self._reference_factor = reference_factor

    @property
    def reference_offset(self):
        return self._reference_offset

    @reference_offset.setter
    def reference_offset(self, reference_offset):
        self._reference_offset = reference_offset

    @property
    def reference_unit_abbreviation(self):
        return self._reference_unit_abbreviation

    @reference_unit_abbreviation.setter
    def reference_unit_abbreviation(self, reference_unit_abbreviation):
        self._reference_unit_abbreviation = reference_unit_abbreviation

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
        if not isinstance(other, PWAUnit):
            return False
        return self.__dict__ == other.__dict__

