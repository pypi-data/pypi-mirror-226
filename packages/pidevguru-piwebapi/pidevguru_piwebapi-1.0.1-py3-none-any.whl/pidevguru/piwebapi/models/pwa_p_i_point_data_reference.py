from pprint import pformat
from six import iteritems


class PWAPIPointDataReference(object):
    swagger_types = {
        'descriptor': 'str',
        'digital_set_name': 'str',
        'display_digits': 'int',
        'engineering_units': 'str',
        'future': 'bool',
        'id': 'int',
        'name': 'str',
        'path': 'str',
        'point_class': 'str',
        'point_type': 'str',
        'span': 'float',
        'step': 'bool',
        'web_id': 'str',
        'zero': 'float',
    }

    attribute_map = {
        'descriptor': 'Descriptor',
        'digital_set_name': 'DigitalSetName',
        'display_digits': 'DisplayDigits',
        'engineering_units': 'EngineeringUnits',
        'future': 'Future',
        'id': 'Id',
        'name': 'Name',
        'path': 'Path',
        'point_class': 'PointClass',
        'point_type': 'PointType',
        'span': 'Span',
        'step': 'Step',
        'web_id': 'WebId',
        'zero': 'Zero',
    }

    def __init__(self, descriptor=None, digital_set_name=None, display_digits=None, engineering_units=None, future=None, id=None, name=None, path=None, point_class=None, point_type=None, span=None, step=None, web_id=None, zero=None):

        self._descriptor = None
        self._digital_set_name = None
        self._display_digits = None
        self._engineering_units = None
        self._future = None
        self._id = None
        self._name = None
        self._path = None
        self._point_class = None
        self._point_type = None
        self._span = None
        self._step = None
        self._web_id = None
        self._zero = None

        if descriptor is not None:
            self.descriptor = descriptor
        if digital_set_name is not None:
            self.digital_set_name = digital_set_name
        if display_digits is not None:
            self.display_digits = display_digits
        if engineering_units is not None:
            self.engineering_units = engineering_units
        if future is not None:
            self.future = future
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if path is not None:
            self.path = path
        if point_class is not None:
            self.point_class = point_class
        if point_type is not None:
            self.point_type = point_type
        if span is not None:
            self.span = span
        if step is not None:
            self.step = step
        if web_id is not None:
            self.web_id = web_id
        if zero is not None:
            self.zero = zero

    @property
    def descriptor(self):
        return self._descriptor

    @descriptor.setter
    def descriptor(self, descriptor):
        self._descriptor = descriptor

    @property
    def digital_set_name(self):
        return self._digital_set_name

    @digital_set_name.setter
    def digital_set_name(self, digital_set_name):
        self._digital_set_name = digital_set_name

    @property
    def display_digits(self):
        return self._display_digits

    @display_digits.setter
    def display_digits(self, display_digits):
        self._display_digits = display_digits

    @property
    def engineering_units(self):
        return self._engineering_units

    @engineering_units.setter
    def engineering_units(self, engineering_units):
        self._engineering_units = engineering_units

    @property
    def future(self):
        return self._future

    @future.setter
    def future(self, future):
        self._future = future

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

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
    def point_class(self):
        return self._point_class

    @point_class.setter
    def point_class(self, point_class):
        self._point_class = point_class

    @property
    def point_type(self):
        return self._point_type

    @point_type.setter
    def point_type(self, point_type):
        self._point_type = point_type

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
        if not isinstance(other, PWAPIPointDataReference):
            return False
        return self.__dict__ == other.__dict__

