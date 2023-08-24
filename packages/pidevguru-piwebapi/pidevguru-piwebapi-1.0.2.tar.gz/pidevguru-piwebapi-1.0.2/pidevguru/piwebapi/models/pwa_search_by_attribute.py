from pprint import pformat
from six import iteritems


class PWASearchByAttribute(object):
    swagger_types = {
        'element_template': 'str',
        'search_root': 'str',
        'value_queries': 'list[PWAValueQuery]',
        'web_exception': 'PWAWebException',
    }

    attribute_map = {
        'element_template': 'ElementTemplate',
        'search_root': 'SearchRoot',
        'value_queries': 'ValueQueries',
        'web_exception': 'WebException',
    }

    def __init__(self, element_template=None, search_root=None, value_queries=None, web_exception=None):

        self._element_template = None
        self._search_root = None
        self._value_queries = None
        self._web_exception = None

        if element_template is not None:
            self.element_template = element_template
        if search_root is not None:
            self.search_root = search_root
        if value_queries is not None:
            self.value_queries = value_queries
        if web_exception is not None:
            self.web_exception = web_exception

    @property
    def element_template(self):
        return self._element_template

    @element_template.setter
    def element_template(self, element_template):
        self._element_template = element_template

    @property
    def search_root(self):
        return self._search_root

    @search_root.setter
    def search_root(self, search_root):
        self._search_root = search_root

    @property
    def value_queries(self):
        return self._value_queries

    @value_queries.setter
    def value_queries(self, value_queries):
        self._value_queries = value_queries

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
        if not isinstance(other, PWASearchByAttribute):
            return False
        return self.__dict__ == other.__dict__

