from pprint import pformat
from six import iteritems


class PWAAnalysisTemplateLinks(object):
    swagger_types = {
        'analysis_rule': 'str',
        'analysis_rule_plug_in': 'str',
        'categories': 'str',
        'database': 'str',
        'security': 'str',
        'security_entries': 'str',
        'target': 'str',
        'time_rule': 'str',
        'time_rule_plug_in': 'str',
    }

    attribute_map = {
        'analysis_rule': 'AnalysisRule',
        'analysis_rule_plug_in': 'AnalysisRulePlugIn',
        'categories': 'Categories',
        'database': 'Database',
        'security': 'Security',
        'security_entries': 'SecurityEntries',
        'target': 'Target',
        'time_rule': 'TimeRule',
        'time_rule_plug_in': 'TimeRulePlugIn',
    }

    def __init__(self, analysis_rule=None, analysis_rule_plug_in=None, categories=None, database=None, security=None, security_entries=None, target=None, time_rule=None, time_rule_plug_in=None):

        self._analysis_rule = None
        self._analysis_rule_plug_in = None
        self._categories = None
        self._database = None
        self._security = None
        self._security_entries = None
        self._target = None
        self._time_rule = None
        self._time_rule_plug_in = None

        if analysis_rule is not None:
            self.analysis_rule = analysis_rule
        if analysis_rule_plug_in is not None:
            self.analysis_rule_plug_in = analysis_rule_plug_in
        if categories is not None:
            self.categories = categories
        if database is not None:
            self.database = database
        if security is not None:
            self.security = security
        if security_entries is not None:
            self.security_entries = security_entries
        if target is not None:
            self.target = target
        if time_rule is not None:
            self.time_rule = time_rule
        if time_rule_plug_in is not None:
            self.time_rule_plug_in = time_rule_plug_in

    @property
    def analysis_rule(self):
        return self._analysis_rule

    @analysis_rule.setter
    def analysis_rule(self, analysis_rule):
        self._analysis_rule = analysis_rule

    @property
    def analysis_rule_plug_in(self):
        return self._analysis_rule_plug_in

    @analysis_rule_plug_in.setter
    def analysis_rule_plug_in(self, analysis_rule_plug_in):
        self._analysis_rule_plug_in = analysis_rule_plug_in

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
    def target(self):
        return self._target

    @target.setter
    def target(self, target):
        self._target = target

    @property
    def time_rule(self):
        return self._time_rule

    @time_rule.setter
    def time_rule(self, time_rule):
        self._time_rule = time_rule

    @property
    def time_rule_plug_in(self):
        return self._time_rule_plug_in

    @time_rule_plug_in.setter
    def time_rule_plug_in(self, time_rule_plug_in):
        self._time_rule_plug_in = time_rule_plug_in

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
        if not isinstance(other, PWAAnalysisTemplateLinks):
            return False
        return self.__dict__ == other.__dict__

