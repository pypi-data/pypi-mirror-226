from pprint import pformat
from six import iteritems


class PWANotificationContactTemplateLinks(object):
    swagger_types = {
        'asset_server': 'str',
        'notification_contact_templates': 'str',
        'notification_plug_in': 'str',
        'security': 'str',
        'security_entries': 'str',
    }

    attribute_map = {
        'asset_server': 'AssetServer',
        'notification_contact_templates': 'NotificationContactTemplates',
        'notification_plug_in': 'NotificationPlugIn',
        'security': 'Security',
        'security_entries': 'SecurityEntries',
    }

    def __init__(self, asset_server=None, notification_contact_templates=None, notification_plug_in=None, security=None, security_entries=None):

        self._asset_server = None
        self._notification_contact_templates = None
        self._notification_plug_in = None
        self._security = None
        self._security_entries = None

        if asset_server is not None:
            self.asset_server = asset_server
        if notification_contact_templates is not None:
            self.notification_contact_templates = notification_contact_templates
        if notification_plug_in is not None:
            self.notification_plug_in = notification_plug_in
        if security is not None:
            self.security = security
        if security_entries is not None:
            self.security_entries = security_entries

    @property
    def asset_server(self):
        return self._asset_server

    @asset_server.setter
    def asset_server(self, asset_server):
        self._asset_server = asset_server

    @property
    def notification_contact_templates(self):
        return self._notification_contact_templates

    @notification_contact_templates.setter
    def notification_contact_templates(self, notification_contact_templates):
        self._notification_contact_templates = notification_contact_templates

    @property
    def notification_plug_in(self):
        return self._notification_plug_in

    @notification_plug_in.setter
    def notification_plug_in(self, notification_plug_in):
        self._notification_plug_in = notification_plug_in

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
        if not isinstance(other, PWANotificationContactTemplateLinks):
            return False
        return self.__dict__ == other.__dict__

