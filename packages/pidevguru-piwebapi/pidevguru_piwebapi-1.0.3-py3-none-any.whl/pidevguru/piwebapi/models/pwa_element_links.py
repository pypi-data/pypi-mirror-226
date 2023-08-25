from pprint import pformat
from six import iteritems


class PWAElementLinks(object):
    swagger_types = {
        'analyses': 'str',
        'attributes': 'str',
        'categories': 'str',
        'database': 'str',
        'default_attribute': 'str',
        'elements': 'str',
        'end_value': 'str',
        'event_frames': 'str',
        'interpolated_data': 'str',
        'notification_rules': 'str',
        'parent': 'str',
        'plot_data': 'str',
        'recorded_data': 'str',
        'security': 'str',
        'security_entries': 'str',
        'summary_data': 'str',
        'template': 'str',
        'value': 'str',
    }

    attribute_map = {
        'analyses': 'Analyses',
        'attributes': 'Attributes',
        'categories': 'Categories',
        'database': 'Database',
        'default_attribute': 'DefaultAttribute',
        'elements': 'Elements',
        'end_value': 'EndValue',
        'event_frames': 'EventFrames',
        'interpolated_data': 'InterpolatedData',
        'notification_rules': 'NotificationRules',
        'parent': 'Parent',
        'plot_data': 'PlotData',
        'recorded_data': 'RecordedData',
        'security': 'Security',
        'security_entries': 'SecurityEntries',
        'summary_data': 'SummaryData',
        'template': 'Template',
        'value': 'Value',
    }

    def __init__(self, analyses=None, attributes=None, categories=None, database=None, default_attribute=None, elements=None, end_value=None, event_frames=None, interpolated_data=None, notification_rules=None, parent=None, plot_data=None, recorded_data=None, security=None, security_entries=None, summary_data=None, template=None, value=None):

        self._analyses = None
        self._attributes = None
        self._categories = None
        self._database = None
        self._default_attribute = None
        self._elements = None
        self._end_value = None
        self._event_frames = None
        self._interpolated_data = None
        self._notification_rules = None
        self._parent = None
        self._plot_data = None
        self._recorded_data = None
        self._security = None
        self._security_entries = None
        self._summary_data = None
        self._template = None
        self._value = None

        if analyses is not None:
            self.analyses = analyses
        if attributes is not None:
            self.attributes = attributes
        if categories is not None:
            self.categories = categories
        if database is not None:
            self.database = database
        if default_attribute is not None:
            self.default_attribute = default_attribute
        if elements is not None:
            self.elements = elements
        if end_value is not None:
            self.end_value = end_value
        if event_frames is not None:
            self.event_frames = event_frames
        if interpolated_data is not None:
            self.interpolated_data = interpolated_data
        if notification_rules is not None:
            self.notification_rules = notification_rules
        if parent is not None:
            self.parent = parent
        if plot_data is not None:
            self.plot_data = plot_data
        if recorded_data is not None:
            self.recorded_data = recorded_data
        if security is not None:
            self.security = security
        if security_entries is not None:
            self.security_entries = security_entries
        if summary_data is not None:
            self.summary_data = summary_data
        if template is not None:
            self.template = template
        if value is not None:
            self.value = value

    @property
    def analyses(self):
        return self._analyses

    @analyses.setter
    def analyses(self, analyses):
        self._analyses = analyses

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        self._attributes = attributes

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, categories):
        self._categories = categories

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database):
        self._database = database

    @property
    def default_attribute(self):
        return self._default_attribute

    @default_attribute.setter
    def default_attribute(self, default_attribute):
        self._default_attribute = default_attribute

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, elements):
        self._elements = elements

    @property
    def end_value(self):
        return self._end_value

    @end_value.setter
    def end_value(self, end_value):
        self._end_value = end_value

    @property
    def event_frames(self):
        return self._event_frames

    @event_frames.setter
    def event_frames(self, event_frames):
        self._event_frames = event_frames

    @property
    def interpolated_data(self):
        return self._interpolated_data

    @interpolated_data.setter
    def interpolated_data(self, interpolated_data):
        self._interpolated_data = interpolated_data

    @property
    def notification_rules(self):
        return self._notification_rules

    @notification_rules.setter
    def notification_rules(self, notification_rules):
        self._notification_rules = notification_rules

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def plot_data(self):
        return self._plot_data

    @plot_data.setter
    def plot_data(self, plot_data):
        self._plot_data = plot_data

    @property
    def recorded_data(self):
        return self._recorded_data

    @recorded_data.setter
    def recorded_data(self, recorded_data):
        self._recorded_data = recorded_data

    @property
    def security(self):
        return self._security

    @security.setter
    def security(self, security):
        self._security = security

    @property
    def security_entries(self):
        return self._security_entries

    @security_entries.setter
    def security_entries(self, security_entries):
        self._security_entries = security_entries

    @property
    def summary_data(self):
        return self._summary_data

    @summary_data.setter
    def summary_data(self, summary_data):
        self._summary_data = summary_data

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, template):
        self._template = template

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

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
        if not isinstance(other, PWAElementLinks):
            return False
        return self.__dict__ == other.__dict__

