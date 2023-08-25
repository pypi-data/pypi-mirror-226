from pprint import pformat
from six import iteritems


class PWANotificationContactTemplate(object):
    swagger_types = {
        'available': 'bool',
        'config_string': 'str',
        'contact_type': 'str',
        'description': 'str',
        'escalation_timeout': 'str',
        'has_children': 'bool',
        'id': 'str',
        'links': 'PWANotificationContactTemplateLinks',
        'maximum_retries': 'int',
        'minimum_acknowledgements': 'int',
        'name': 'str',
        'notify_when_instance_ended': 'bool',
        'path': 'str',
        'plug_in_name': 'str',
        'retry_interval': 'str',
        'web_exception': 'PWAWebException',
        'web_id': 'str',
    }

    attribute_map = {
        'available': 'Available',
        'config_string': 'ConfigString',
        'contact_type': 'ContactType',
        'description': 'Description',
        'escalation_timeout': 'EscalationTimeout',
        'has_children': 'HasChildren',
        'id': 'Id',
        'links': 'Links',
        'maximum_retries': 'MaximumRetries',
        'minimum_acknowledgements': 'MinimumAcknowledgements',
        'name': 'Name',
        'notify_when_instance_ended': 'NotifyWhenInstanceEnded',
        'path': 'Path',
        'plug_in_name': 'PlugInName',
        'retry_interval': 'RetryInterval',
        'web_exception': 'WebException',
        'web_id': 'WebId',
    }

    def __init__(self, available=None, config_string=None, contact_type=None, description=None, escalation_timeout=None, has_children=None, id=None, links=None, maximum_retries=None, minimum_acknowledgements=None, name=None, notify_when_instance_ended=None, path=None, plug_in_name=None, retry_interval=None, web_exception=None, web_id=None):

        self._available = None
        self._config_string = None
        self._contact_type = None
        self._description = None
        self._escalation_timeout = None
        self._has_children = None
        self._id = None
        self._links = None
        self._maximum_retries = None
        self._minimum_acknowledgements = None
        self._name = None
        self._notify_when_instance_ended = None
        self._path = None
        self._plug_in_name = None
        self._retry_interval = None
        self._web_exception = None
        self._web_id = None

        if available is not None:
            self.available = available
        if config_string is not None:
            self.config_string = config_string
        if contact_type is not None:
            self.contact_type = contact_type
        if description is not None:
            self.description = description
        if escalation_timeout is not None:
            self.escalation_timeout = escalation_timeout
        if has_children is not None:
            self.has_children = has_children
        if id is not None:
            self.id = id
        if links is not None:
            self.links = links
        if maximum_retries is not None:
            self.maximum_retries = maximum_retries
        if minimum_acknowledgements is not None:
            self.minimum_acknowledgements = minimum_acknowledgements
        if name is not None:
            self.name = name
        if notify_when_instance_ended is not None:
            self.notify_when_instance_ended = notify_when_instance_ended
        if path is not None:
            self.path = path
        if plug_in_name is not None:
            self.plug_in_name = plug_in_name
        if retry_interval is not None:
            self.retry_interval = retry_interval
        if web_exception is not None:
            self.web_exception = web_exception
        if web_id is not None:
            self.web_id = web_id

    @property
    def available(self):
        return self._available

    @available.setter
    def available(self, available):
        self._available = available

    @property
    def config_string(self):
        return self._config_string

    @config_string.setter
    def config_string(self, config_string):
        self._config_string = config_string

    @property
    def contact_type(self):
        return self._contact_type

    @contact_type.setter
    def contact_type(self, contact_type):
        self._contact_type = contact_type

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def escalation_timeout(self):
        return self._escalation_timeout

    @escalation_timeout.setter
    def escalation_timeout(self, escalation_timeout):
        self._escalation_timeout = escalation_timeout

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
    def maximum_retries(self):
        return self._maximum_retries

    @maximum_retries.setter
    def maximum_retries(self, maximum_retries):
        self._maximum_retries = maximum_retries

    @property
    def minimum_acknowledgements(self):
        return self._minimum_acknowledgements

    @minimum_acknowledgements.setter
    def minimum_acknowledgements(self, minimum_acknowledgements):
        self._minimum_acknowledgements = minimum_acknowledgements

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def notify_when_instance_ended(self):
        return self._notify_when_instance_ended

    @notify_when_instance_ended.setter
    def notify_when_instance_ended(self, notify_when_instance_ended):
        self._notify_when_instance_ended = notify_when_instance_ended

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def plug_in_name(self):
        return self._plug_in_name

    @plug_in_name.setter
    def plug_in_name(self, plug_in_name):
        self._plug_in_name = plug_in_name

    @property
    def retry_interval(self):
        return self._retry_interval

    @retry_interval.setter
    def retry_interval(self, retry_interval):
        self._retry_interval = retry_interval

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
        if not isinstance(other, PWANotificationContactTemplate):
            return False
        return self.__dict__ == other.__dict__

