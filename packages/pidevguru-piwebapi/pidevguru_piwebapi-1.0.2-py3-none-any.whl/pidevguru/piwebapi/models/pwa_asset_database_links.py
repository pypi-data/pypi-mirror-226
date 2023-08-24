from pprint import pformat
from six import iteritems


class PWAAssetDatabaseLinks(object):
    swagger_types = {
        'analysis_categories': 'str',
        'analysis_templates': 'str',
        'asset_server': 'str',
        'attribute_categories': 'str',
        'element_categories': 'str',
        'element_templates': 'str',
        'elements': 'str',
        'enumeration_sets': 'str',
        'event_frames': 'str',
        'security': 'str',
        'security_entries': 'str',
        'table_categories': 'str',
        'tables': 'str',
    }

    attribute_map = {
        'analysis_categories': 'AnalysisCategories',
        'analysis_templates': 'AnalysisTemplates',
        'asset_server': 'AssetServer',
        'attribute_categories': 'AttributeCategories',
        'element_categories': 'ElementCategories',
        'element_templates': 'ElementTemplates',
        'elements': 'Elements',
        'enumeration_sets': 'EnumerationSets',
        'event_frames': 'EventFrames',
        'security': 'Security',
        'security_entries': 'SecurityEntries',
        'table_categories': 'TableCategories',
        'tables': 'Tables',
    }

    def __init__(self, analysis_categories=None, analysis_templates=None, asset_server=None, attribute_categories=None, element_categories=None, element_templates=None, elements=None, enumeration_sets=None, event_frames=None, security=None, security_entries=None, table_categories=None, tables=None):

        self._analysis_categories = None
        self._analysis_templates = None
        self._asset_server = None
        self._attribute_categories = None
        self._element_categories = None
        self._element_templates = None
        self._elements = None
        self._enumeration_sets = None
        self._event_frames = None
        self._security = None
        self._security_entries = None
        self._table_categories = None
        self._tables = None

        if analysis_categories is not None:
            self.analysis_categories = analysis_categories
        if analysis_templates is not None:
            self.analysis_templates = analysis_templates
        if asset_server is not None:
            self.asset_server = asset_server
        if attribute_categories is not None:
            self.attribute_categories = attribute_categories
        if element_categories is not None:
            self.element_categories = element_categories
        if element_templates is not None:
            self.element_templates = element_templates
        if elements is not None:
            self.elements = elements
        if enumeration_sets is not None:
            self.enumeration_sets = enumeration_sets
        if event_frames is not None:
            self.event_frames = event_frames
        if security is not None:
            self.security = security
        if security_entries is not None:
            self.security_entries = security_entries
        if table_categories is not None:
            self.table_categories = table_categories
        if tables is not None:
            self.tables = tables

    @property
    def analysis_categories(self):
        return self._analysis_categories

    @analysis_categories.setter
    def analysis_categories(self, analysis_categories):
        self._analysis_categories = analysis_categories

    @property
    def analysis_templates(self):
        return self._analysis_templates

    @analysis_templates.setter
    def analysis_templates(self, analysis_templates):
        self._analysis_templates = analysis_templates

    @property
    def asset_server(self):
        return self._asset_server

    @asset_server.setter
    def asset_server(self, asset_server):
        self._asset_server = asset_server

    @property
    def attribute_categories(self):
        return self._attribute_categories

    @attribute_categories.setter
    def attribute_categories(self, attribute_categories):
        self._attribute_categories = attribute_categories

    @property
    def element_categories(self):
        return self._element_categories

    @element_categories.setter
    def element_categories(self, element_categories):
        self._element_categories = element_categories

    @property
    def element_templates(self):
        return self._element_templates

    @element_templates.setter
    def element_templates(self, element_templates):
        self._element_templates = element_templates

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, elements):
        self._elements = elements

    @property
    def enumeration_sets(self):
        return self._enumeration_sets

    @enumeration_sets.setter
    def enumeration_sets(self, enumeration_sets):
        self._enumeration_sets = enumeration_sets

    @property
    def event_frames(self):
        return self._event_frames

    @event_frames.setter
    def event_frames(self, event_frames):
        self._event_frames = event_frames

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
    def table_categories(self):
        return self._table_categories

    @table_categories.setter
    def table_categories(self, table_categories):
        self._table_categories = table_categories

    @property
    def tables(self):
        return self._tables

    @tables.setter
    def tables(self, tables):
        self._tables = tables

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
        if not isinstance(other, PWAAssetDatabaseLinks):
            return False
        return self.__dict__ == other.__dict__

