from pprint import pformat
from six import iteritems


class PWAUnitClass(object):
    swagger_types = {
        'canonical_unit_abbreviation': 'str',
        'canonical_unit_name': 'str',
        'description': 'str',
        'id': 'str',
        'links': 'PWAUnitClassLinks',
        'name': 'str',
        'path': 'str',
        'web_exception': 'PWAWebException',
        'web_id': 'str',
    }

    attribute_map = {
        'canonical_unit_abbreviation': 'CanonicalUnitAbbreviation',
        'canonical_unit_name': 'CanonicalUnitName',
        'description': 'Description',
        'id': 'Id',
        'links': 'Links',
        'name': 'Name',
        'path': 'Path',
        'web_exception': 'WebException',
        'web_id': 'WebId',
    }

    def __init__(self, canonical_unit_abbreviation=None, canonical_unit_name=None, description=None, id=None, links=None, name=None, path=None, web_exception=None, web_id=None):

        self._canonical_unit_abbreviation = None
        self._canonical_unit_name = None
        self._description = None
        self._id = None
        self._links = None
        self._name = None
        self._path = None
        self._web_exception = None
        self._web_id = None

        if canonical_unit_abbreviation is not None:
            self.canonical_unit_abbreviation = canonical_unit_abbreviation
        if canonical_unit_name is not None:
            self.canonical_unit_name = canonical_unit_name
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
        if web_exception is not None:
            self.web_exception = web_exception
        if web_id is not None:
            self.web_id = web_id

    @property
    def canonical_unit_abbreviation(self):
        return self._canonical_unit_abbreviation

    @canonical_unit_abbreviation.setter
    def canonical_unit_abbreviation(self, canonical_unit_abbreviation):
        self._canonical_unit_abbreviation = canonical_unit_abbreviation

    @property
    def canonical_unit_name(self):
        return self._canonical_unit_name

    @canonical_unit_name.setter
    def canonical_unit_name(self, canonical_unit_name):
        self._canonical_unit_name = canonical_unit_name

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
        if not isinstance(other, PWAUnitClass):
            return False
        return self.__dict__ == other.__dict__

