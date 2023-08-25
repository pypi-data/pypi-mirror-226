from pprint import pformat
from six import iteritems


class PWAStreamAnnotation(object):
    swagger_types = {
        'creation_date': 'str',
        'creator': 'str',
        'description': 'str',
        'errors': 'list[PWAPropertyError]',
        'id': 'str',
        'modifier': 'str',
        'modify_date': 'str',
        'name': 'str',
        'value': 'object',
        'web_exception': 'PWAWebException',
    }

    attribute_map = {
        'creation_date': 'CreationDate',
        'creator': 'Creator',
        'description': 'Description',
        'errors': 'Errors',
        'id': 'Id',
        'modifier': 'Modifier',
        'modify_date': 'ModifyDate',
        'name': 'Name',
        'value': 'Value',
        'web_exception': 'WebException',
    }

    def __init__(self, creation_date=None, creator=None, description=None, errors=None, id=None, modifier=None, modify_date=None, name=None, value=None, web_exception=None):

        self._creation_date = None
        self._creator = None
        self._description = None
        self._errors = None
        self._id = None
        self._modifier = None
        self._modify_date = None
        self._name = None
        self._value = None
        self._web_exception = None

        if creation_date is not None:
            self.creation_date = creation_date
        if creator is not None:
            self.creator = creator
        if description is not None:
            self.description = description
        if errors is not None:
            self.errors = errors
        if id is not None:
            self.id = id
        if modifier is not None:
            self.modifier = modifier
        if modify_date is not None:
            self.modify_date = modify_date
        if name is not None:
            self.name = name
        if value is not None:
            self.value = value
        if web_exception is not None:
            self.web_exception = web_exception

    @property
    def creation_date(self):
        return self._creation_date

    @creation_date.setter
    def creation_date(self, creation_date):
        self._creation_date = creation_date

    @property
    def creator(self):
        return self._creator

    @creator.setter
    def creator(self, creator):
        self._creator = creator

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
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def modifier(self):
        return self._modifier

    @modifier.setter
    def modifier(self, modifier):
        self._modifier = modifier

    @property
    def modify_date(self):
        return self._modify_date

    @modify_date.setter
    def modify_date(self, modify_date):
        self._modify_date = modify_date

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

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
        if not isinstance(other, PWAStreamAnnotation):
            return False
        return self.__dict__ == other.__dict__

