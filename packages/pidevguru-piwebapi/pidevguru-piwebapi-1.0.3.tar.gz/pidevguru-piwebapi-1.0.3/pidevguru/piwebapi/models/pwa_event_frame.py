from pprint import pformat
from six import iteritems


class PWAEventFrame(object):
    swagger_types = {
        'acknowledged_by': 'str',
        'acknowledged_date': 'str',
        'are_values_captured': 'bool',
        'can_be_acknowledged': 'bool',
        'category_names': 'list[str]',
        'description': 'str',
        'end_time': 'str',
        'extended_properties': 'dict(str, PWAValue)',
        'has_children': 'bool',
        'id': 'str',
        'is_acknowledged': 'bool',
        'is_annotated': 'bool',
        'is_locked': 'bool',
        'links': 'PWAEventFrameLinks',
        'name': 'str',
        'path': 'str',
        'ref_element_web_ids': 'list[str]',
        'security': 'PWASecurity',
        'severity': 'str',
        'start_time': 'str',
        'template_name': 'str',
        'web_exception': 'PWAWebException',
        'web_id': 'str',
    }

    attribute_map = {
        'acknowledged_by': 'AcknowledgedBy',
        'acknowledged_date': 'AcknowledgedDate',
        'are_values_captured': 'AreValuesCaptured',
        'can_be_acknowledged': 'CanBeAcknowledged',
        'category_names': 'CategoryNames',
        'description': 'Description',
        'end_time': 'EndTime',
        'extended_properties': 'ExtendedProperties',
        'has_children': 'HasChildren',
        'id': 'Id',
        'is_acknowledged': 'IsAcknowledged',
        'is_annotated': 'IsAnnotated',
        'is_locked': 'IsLocked',
        'links': 'Links',
        'name': 'Name',
        'path': 'Path',
        'ref_element_web_ids': 'RefElementWebIds',
        'security': 'Security',
        'severity': 'Severity',
        'start_time': 'StartTime',
        'template_name': 'TemplateName',
        'web_exception': 'WebException',
        'web_id': 'WebId',
    }

    def __init__(self, acknowledged_by=None, acknowledged_date=None, are_values_captured=None, can_be_acknowledged=None, category_names=None, description=None, end_time=None, extended_properties=None, has_children=None, id=None, is_acknowledged=None, is_annotated=None, is_locked=None, links=None, name=None, path=None, ref_element_web_ids=None, security=None, severity=None, start_time=None, template_name=None, web_exception=None, web_id=None):

        self._acknowledged_by = None
        self._acknowledged_date = None
        self._are_values_captured = None
        self._can_be_acknowledged = None
        self._category_names = None
        self._description = None
        self._end_time = None
        self._extended_properties = None
        self._has_children = None
        self._id = None
        self._is_acknowledged = None
        self._is_annotated = None
        self._is_locked = None
        self._links = None
        self._name = None
        self._path = None
        self._ref_element_web_ids = None
        self._security = None
        self._severity = None
        self._start_time = None
        self._template_name = None
        self._web_exception = None
        self._web_id = None

        if acknowledged_by is not None:
            self.acknowledged_by = acknowledged_by
        if acknowledged_date is not None:
            self.acknowledged_date = acknowledged_date
        if are_values_captured is not None:
            self.are_values_captured = are_values_captured
        if can_be_acknowledged is not None:
            self.can_be_acknowledged = can_be_acknowledged
        if category_names is not None:
            self.category_names = category_names
        if description is not None:
            self.description = description
        if end_time is not None:
            self.end_time = end_time
        if extended_properties is not None:
            self.extended_properties = extended_properties
        if has_children is not None:
            self.has_children = has_children
        if id is not None:
            self.id = id
        if is_acknowledged is not None:
            self.is_acknowledged = is_acknowledged
        if is_annotated is not None:
            self.is_annotated = is_annotated
        if is_locked is not None:
            self.is_locked = is_locked
        if links is not None:
            self.links = links
        if name is not None:
            self.name = name
        if path is not None:
            self.path = path
        if ref_element_web_ids is not None:
            self.ref_element_web_ids = ref_element_web_ids
        if security is not None:
            self.security = security
        if severity is not None:
            self.severity = severity
        if start_time is not None:
            self.start_time = start_time
        if template_name is not None:
            self.template_name = template_name
        if web_exception is not None:
            self.web_exception = web_exception
        if web_id is not None:
            self.web_id = web_id

    @property
    def acknowledged_by(self):
        return self._acknowledged_by

    @acknowledged_by.setter
    def acknowledged_by(self, acknowledged_by):
        self._acknowledged_by = acknowledged_by

    @property
    def acknowledged_date(self):
        return self._acknowledged_date

    @acknowledged_date.setter
    def acknowledged_date(self, acknowledged_date):
        self._acknowledged_date = acknowledged_date

    @property
    def are_values_captured(self):
        return self._are_values_captured

    @are_values_captured.setter
    def are_values_captured(self, are_values_captured):
        self._are_values_captured = are_values_captured

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
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        self._end_time = end_time

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
    def is_acknowledged(self):
        return self._is_acknowledged

    @is_acknowledged.setter
    def is_acknowledged(self, is_acknowledged):
        self._is_acknowledged = is_acknowledged

    @property
    def is_annotated(self):
        return self._is_annotated

    @is_annotated.setter
    def is_annotated(self, is_annotated):
        self._is_annotated = is_annotated

    @property
    def is_locked(self):
        return self._is_locked

    @is_locked.setter
    def is_locked(self, is_locked):
        self._is_locked = is_locked

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
    def ref_element_web_ids(self):
        return self._ref_element_web_ids

    @ref_element_web_ids.setter
    def ref_element_web_ids(self, ref_element_web_ids):
        self._ref_element_web_ids = ref_element_web_ids

    @property
    def security(self):
        return self._security

    @security.setter
    def security(self, security):
        self._security = security

    @property
    def severity(self):
        return self._severity

    @severity.setter
    def severity(self, severity):
        self._severity = severity

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time

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
        if not isinstance(other, PWAEventFrame):
            return False
        return self.__dict__ == other.__dict__

