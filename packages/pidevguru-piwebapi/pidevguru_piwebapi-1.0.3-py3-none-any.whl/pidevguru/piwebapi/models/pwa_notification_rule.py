from pprint import pformat
from six import iteritems


class PWANotificationRule(object):
    swagger_types = {
        'auto_created': 'bool',
        'category_names': 'list[str]',
        'criteria': 'str',
        'description': 'str',
        'id': 'str',
        'multi_trigger_event_option': 'str',
        'name': 'str',
        'nonrepetition_interval': 'str',
        'path': 'str',
        'resend_interval': 'str',
        'status': 'str',
        'template_name': 'str',
        'web_exception': 'PWAWebException',
        'web_id': 'str',
    }

    attribute_map = {
        'auto_created': 'AutoCreated',
        'category_names': 'CategoryNames',
        'criteria': 'Criteria',
        'description': 'Description',
        'id': 'Id',
        'multi_trigger_event_option': 'MultiTriggerEventOption',
        'name': 'Name',
        'nonrepetition_interval': 'NonrepetitionInterval',
        'path': 'Path',
        'resend_interval': 'ResendInterval',
        'status': 'Status',
        'template_name': 'TemplateName',
        'web_exception': 'WebException',
        'web_id': 'WebId',
    }

    def __init__(self, auto_created=None, category_names=None, criteria=None, description=None, id=None, multi_trigger_event_option=None, name=None, nonrepetition_interval=None, path=None, resend_interval=None, status=None, template_name=None, web_exception=None, web_id=None):

        self._auto_created = None
        self._category_names = None
        self._criteria = None
        self._description = None
        self._id = None
        self._multi_trigger_event_option = None
        self._name = None
        self._nonrepetition_interval = None
        self._path = None
        self._resend_interval = None
        self._status = None
        self._template_name = None
        self._web_exception = None
        self._web_id = None

        if auto_created is not None:
            self.auto_created = auto_created
        if category_names is not None:
            self.category_names = category_names
        if criteria is not None:
            self.criteria = criteria
        if description is not None:
            self.description = description
        if id is not None:
            self.id = id
        if multi_trigger_event_option is not None:
            self.multi_trigger_event_option = multi_trigger_event_option
        if name is not None:
            self.name = name
        if nonrepetition_interval is not None:
            self.nonrepetition_interval = nonrepetition_interval
        if path is not None:
            self.path = path
        if resend_interval is not None:
            self.resend_interval = resend_interval
        if status is not None:
            self.status = status
        if template_name is not None:
            self.template_name = template_name
        if web_exception is not None:
            self.web_exception = web_exception
        if web_id is not None:
            self.web_id = web_id

    @property
    def auto_created(self):
        return self._auto_created

    @auto_created.setter
    def auto_created(self, auto_created):
        self._auto_created = auto_created

    @property
    def category_names(self):
        return self._category_names

    @category_names.setter
    def category_names(self, category_names):
        self._category_names = category_names

    @property
    def criteria(self):
        return self._criteria

    @criteria.setter
    def criteria(self, criteria):
        self._criteria = criteria

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
    def multi_trigger_event_option(self):
        return self._multi_trigger_event_option

    @multi_trigger_event_option.setter
    def multi_trigger_event_option(self, multi_trigger_event_option):
        self._multi_trigger_event_option = multi_trigger_event_option

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def nonrepetition_interval(self):
        return self._nonrepetition_interval

    @nonrepetition_interval.setter
    def nonrepetition_interval(self, nonrepetition_interval):
        self._nonrepetition_interval = nonrepetition_interval

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def resend_interval(self):
        return self._resend_interval

    @resend_interval.setter
    def resend_interval(self, resend_interval):
        self._resend_interval = resend_interval

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

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
        if not isinstance(other, PWANotificationRule):
            return False
        return self.__dict__ == other.__dict__

