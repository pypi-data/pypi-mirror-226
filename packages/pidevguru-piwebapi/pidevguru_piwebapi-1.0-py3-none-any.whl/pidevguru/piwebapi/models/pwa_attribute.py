from pprint import pformat
from six import iteritems


class PWAAttribute(object):
    swagger_types = {
        'category_names': 'list[str]',
        'config_string': 'str',
        'data_reference': 'PWADataReference',
        'data_reference_plug_in': 'str',
        'default_units_name': 'str',
        'default_units_name_abbreviation': 'str',
        'description': 'str',
        'display_digits': 'int',
        'has_children': 'bool',
        'id': 'str',
        'is_configuration_item': 'bool',
        'is_excluded': 'bool',
        'is_hidden': 'bool',
        'is_manual_data_entry': 'bool',
        'links': 'PWAAttributeLinks',
        'name': 'str',
        'path': 'str',
        'paths': 'list[str]',
        'span': 'float',
        'step': 'bool',
        'trait_name': 'str',
        'type': 'str',
        'type_qualifier': 'str',
        'web_exception': 'PWAWebException',
        'web_id': 'str',
        'zero': 'float',
    }

    attribute_map = {
        'category_names': 'CategoryNames',
        'config_string': 'ConfigString',
        'data_reference': 'DataReference',
        'data_reference_plug_in': 'DataReferencePlugIn',
        'default_units_name': 'DefaultUnitsName',
        'default_units_name_abbreviation': 'DefaultUnitsNameAbbreviation',
        'description': 'Description',
        'display_digits': 'DisplayDigits',
        'has_children': 'HasChildren',
        'id': 'Id',
        'is_configuration_item': 'IsConfigurationItem',
        'is_excluded': 'IsExcluded',
        'is_hidden': 'IsHidden',
        'is_manual_data_entry': 'IsManualDataEntry',
        'links': 'Links',
        'name': 'Name',
        'path': 'Path',
        'paths': 'Paths',
        'span': 'Span',
        'step': 'Step',
        'trait_name': 'TraitName',
        'type': 'Type',
        'type_qualifier': 'TypeQualifier',
        'web_exception': 'WebException',
        'web_id': 'WebId',
        'zero': 'Zero',
    }

    def __init__(self, category_names=None, config_string=None, data_reference=None, data_reference_plug_in=None, default_units_name=None, default_units_name_abbreviation=None, description=None, display_digits=None, has_children=None, id=None, is_configuration_item=None, is_excluded=None, is_hidden=None, is_manual_data_entry=None, links=None, name=None, path=None, paths=None, span=None, step=None, trait_name=None, type=None, type_qualifier=None, web_exception=None, web_id=None, zero=None):

        self._category_names = None
        self._config_string = None
        self._data_reference = None
        self._data_reference_plug_in = None
        self._default_units_name = None
        self._default_units_name_abbreviation = None
        self._description = None
        self._display_digits = None
        self._has_children = None
        self._id = None
        self._is_configuration_item = None
        self._is_excluded = None
        self._is_hidden = None
        self._is_manual_data_entry = None
        self._links = None
        self._name = None
        self._path = None
        self._paths = None
        self._span = None
        self._step = None
        self._trait_name = None
        self._type = None
        self._type_qualifier = None
        self._web_exception = None
        self._web_id = None
        self._zero = None

        if category_names is not None:
            self.category_names = category_names
        if config_string is not None:
            self.config_string = config_string
        if data_reference is not None:
            self.data_reference = data_reference
        if data_reference_plug_in is not None:
            self.data_reference_plug_in = data_reference_plug_in
        if default_units_name is not None:
            self.default_units_name = default_units_name
        if default_units_name_abbreviation is not None:
            self.default_units_name_abbreviation = default_units_name_abbreviation
        if description is not None:
            self.description = description
        if display_digits is not None:
            self.display_digits = display_digits
        if has_children is not None:
            self.has_children = has_children
        if id is not None:
            self.id = id
        if is_configuration_item is not None:
            self.is_configuration_item = is_configuration_item
        if is_excluded is not None:
            self.is_excluded = is_excluded
        if is_hidden is not None:
            self.is_hidden = is_hidden
        if is_manual_data_entry is not None:
            self.is_manual_data_entry = is_manual_data_entry
        if links is not None:
            self.links = links
        if name is not None:
            self.name = name
        if path is not None:
            self.path = path
        if paths is not None:
            self.paths = paths
        if span is not None:
            self.span = span
        if step is not None:
            self.step = step
        if trait_name is not None:
            self.trait_name = trait_name
        if type is not None:
            self.type = type
        if type_qualifier is not None:
            self.type_qualifier = type_qualifier
        if web_exception is not None:
            self.web_exception = web_exception
        if web_id is not None:
            self.web_id = web_id
        if zero is not None:
            self.zero = zero

    @property
    def category_names(self):
        return self._category_names

    @category_names.setter
    def category_names(self, category_names):
        self._category_names = category_names

    @property
    def config_string(self):
        return self._config_string

    @config_string.setter
    def config_string(self, config_string):
        self._config_string = config_string

    @property
    def data_reference(self):
        return self._data_reference

    @data_reference.setter
    def data_reference(self, data_reference):
        self._data_reference = data_reference

    @property
    def data_reference_plug_in(self):
        return self._data_reference_plug_in

    @data_reference_plug_in.setter
    def data_reference_plug_in(self, data_reference_plug_in):
        self._data_reference_plug_in = data_reference_plug_in

    @property
    def default_units_name(self):
        return self._default_units_name

    @default_units_name.setter
    def default_units_name(self, default_units_name):
        self._default_units_name = default_units_name

    @property
    def default_units_name_abbreviation(self):
        return self._default_units_name_abbreviation

    @default_units_name_abbreviation.setter
    def default_units_name_abbreviation(self, default_units_name_abbreviation):
        self._default_units_name_abbreviation = default_units_name_abbreviation

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def display_digits(self):
        return self._display_digits

    @display_digits.setter
    def display_digits(self, display_digits):
        self._display_digits = display_digits

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
    def is_configuration_item(self):
        return self._is_configuration_item

    @is_configuration_item.setter
    def is_configuration_item(self, is_configuration_item):
        self._is_configuration_item = is_configuration_item

    @property
    def is_excluded(self):
        return self._is_excluded

    @is_excluded.setter
    def is_excluded(self, is_excluded):
        self._is_excluded = is_excluded

    @property
    def is_hidden(self):
        return self._is_hidden

    @is_hidden.setter
    def is_hidden(self, is_hidden):
        self._is_hidden = is_hidden

    @property
    def is_manual_data_entry(self):
        return self._is_manual_data_entry

    @is_manual_data_entry.setter
    def is_manual_data_entry(self, is_manual_data_entry):
        self._is_manual_data_entry = is_manual_data_entry

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
    def span(self):
        return self._span

    @span.setter
    def span(self, span):
        self._span = span

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, step):
        self._step = step

    @property
    def trait_name(self):
        return self._trait_name

    @trait_name.setter
    def trait_name(self, trait_name):
        self._trait_name = trait_name

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def type_qualifier(self):
        return self._type_qualifier

    @type_qualifier.setter
    def type_qualifier(self, type_qualifier):
        self._type_qualifier = type_qualifier

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

    @property
    def zero(self):
        return self._zero

    @zero.setter
    def zero(self, zero):
        self._zero = zero

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
        if not isinstance(other, PWAAttribute):
            return False
        return self.__dict__ == other.__dict__

