from pprint import pformat
from six import iteritems


class PWAAssetServerLinks(object):
    swagger_types = {
        'analysis_rule_plug_ins': 'str',
        'databases': 'str',
        'notification_contact_templates': 'str',
        'notification_plug_ins': 'str',
        'security': 'str',
        'security_entries': 'str',
        'security_identities': 'str',
        'security_mappings': 'str',
        'time_rule_plug_ins': 'str',
        'unit_classes': 'str',
    }

    attribute_map = {
        'analysis_rule_plug_ins': 'AnalysisRulePlugIns',
        'databases': 'Databases',
        'notification_contact_templates': 'NotificationContactTemplates',
        'notification_plug_ins': 'NotificationPlugIns',
        'security': 'Security',
        'security_entries': 'SecurityEntries',
        'security_identities': 'SecurityIdentities',
        'security_mappings': 'SecurityMappings',
        'time_rule_plug_ins': 'TimeRulePlugIns',
        'unit_classes': 'UnitClasses',
    }

    def __init__(self, analysis_rule_plug_ins=None, databases=None, notification_contact_templates=None, notification_plug_ins=None, security=None, security_entries=None, security_identities=None, security_mappings=None, time_rule_plug_ins=None, unit_classes=None):

        self._analysis_rule_plug_ins = None
        self._databases = None
        self._notification_contact_templates = None
        self._notification_plug_ins = None
        self._security = None
        self._security_entries = None
        self._security_identities = None
        self._security_mappings = None
        self._time_rule_plug_ins = None
        self._unit_classes = None

        if analysis_rule_plug_ins is not None:
            self.analysis_rule_plug_ins = analysis_rule_plug_ins
        if databases is not None:
            self.databases = databases
        if notification_contact_templates is not None:
            self.notification_contact_templates = notification_contact_templates
        if notification_plug_ins is not None:
            self.notification_plug_ins = notification_plug_ins
        if security is not None:
            self.security = security
        if security_entries is not None:
            self.security_entries = security_entries
        if security_identities is not None:
            self.security_identities = security_identities
        if security_mappings is not None:
            self.security_mappings = security_mappings
        if time_rule_plug_ins is not None:
            self.time_rule_plug_ins = time_rule_plug_ins
        if unit_classes is not None:
            self.unit_classes = unit_classes

    @property
    def analysis_rule_plug_ins(self):
        return self._analysis_rule_plug_ins

    @analysis_rule_plug_ins.setter
    def analysis_rule_plug_ins(self, analysis_rule_plug_ins):
        self._analysis_rule_plug_ins = analysis_rule_plug_ins

    @property
    def databases(self):
        return self._databases

    @databases.setter
    def databases(self, databases):
        self._databases = databases

    @property
    def notification_contact_templates(self):
        return self._notification_contact_templates

    @notification_contact_templates.setter
    def notification_contact_templates(self, notification_contact_templates):
        self._notification_contact_templates = notification_contact_templates

    @property
    def notification_plug_ins(self):
        return self._notification_plug_ins

    @notification_plug_ins.setter
    def notification_plug_ins(self, notification_plug_ins):
        self._notification_plug_ins = notification_plug_ins

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
    def security_identities(self):
        return self._security_identities

    @security_identities.setter
    def security_identities(self, security_identities):
        self._security_identities = security_identities

    @property
    def security_mappings(self):
        return self._security_mappings

    @security_mappings.setter
    def security_mappings(self, security_mappings):
        self._security_mappings = security_mappings

    @property
    def time_rule_plug_ins(self):
        return self._time_rule_plug_ins

    @time_rule_plug_ins.setter
    def time_rule_plug_ins(self, time_rule_plug_ins):
        self._time_rule_plug_ins = time_rule_plug_ins

    @property
    def unit_classes(self):
        return self._unit_classes

    @unit_classes.setter
    def unit_classes(self, unit_classes):
        self._unit_classes = unit_classes

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
        if not isinstance(other, PWAAssetServerLinks):
            return False
        return self.__dict__ == other.__dict__

