from pprint import pformat
from six import iteritems


class PWAExtendedTimedValue(object):
    swagger_types = {
        'annotated': 'bool',
        'annotations': 'list[PWAStreamAnnotation]',
        'errors': 'list[PWAPropertyError]',
        'good': 'bool',
        'questionable': 'bool',
        'substituted': 'bool',
        'timestamp': 'str',
        'units_abbreviation': 'str',
        'value': 'object',
        'web_exception': 'PWAWebException',
    }

    attribute_map = {
        'annotated': 'Annotated',
        'annotations': 'Annotations',
        'errors': 'Errors',
        'good': 'Good',
        'questionable': 'Questionable',
        'substituted': 'Substituted',
        'timestamp': 'Timestamp',
        'units_abbreviation': 'UnitsAbbreviation',
        'value': 'Value',
        'web_exception': 'WebException',
    }

    def __init__(self, annotated=None, annotations=None, errors=None, good=None, questionable=None, substituted=None, timestamp=None, units_abbreviation=None, value=None, web_exception=None):

        self._annotated = None
        self._annotations = None
        self._errors = None
        self._good = None
        self._questionable = None
        self._substituted = None
        self._timestamp = None
        self._units_abbreviation = None
        self._value = None
        self._web_exception = None

        if annotated is not None:
            self.annotated = annotated
        if annotations is not None:
            self.annotations = annotations
        if errors is not None:
            self.errors = errors
        if good is not None:
            self.good = good
        if questionable is not None:
            self.questionable = questionable
        if substituted is not None:
            self.substituted = substituted
        if timestamp is not None:
            self.timestamp = timestamp
        if units_abbreviation is not None:
            self.units_abbreviation = units_abbreviation
        if value is not None:
            self.value = value
        if web_exception is not None:
            self.web_exception = web_exception

    @property
    def annotated(self):
        return self._annotated

    @annotated.setter
    def annotated(self, annotated):
        self._annotated = annotated

    @property
    def annotations(self):
        return self._annotations

    @annotations.setter
    def annotations(self, annotations):
        self._annotations = annotations

    @property
    def errors(self):
        return self._errors

    @errors.setter
    def errors(self, errors):
        self._errors = errors

    @property
    def good(self):
        return self._good

    @good.setter
    def good(self, good):
        self._good = good

    @property
    def questionable(self):
        return self._questionable

    @questionable.setter
    def questionable(self, questionable):
        self._questionable = questionable

    @property
    def substituted(self):
        return self._substituted

    @substituted.setter
    def substituted(self, substituted):
        self._substituted = substituted

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        self._timestamp = timestamp

    @property
    def units_abbreviation(self):
        return self._units_abbreviation

    @units_abbreviation.setter
    def units_abbreviation(self, units_abbreviation):
        self._units_abbreviation = units_abbreviation

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
        if not isinstance(other, PWAExtendedTimedValue):
            return False
        return self.__dict__ == other.__dict__

