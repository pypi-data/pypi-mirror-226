from pprint import pformat
from six import iteritems


class PWARequest(object):
    swagger_types = {
        'content': 'str',
        'headers': 'dict(str, str)',
        'method': 'str',
        'parameters': 'list[str]',
        'parent_ids': 'list[str]',
        'request_template': 'PWARequestTemplate',
        'resource': 'str',
    }

    attribute_map = {
        'content': 'Content',
        'headers': 'Headers',
        'method': 'Method',
        'parameters': 'Parameters',
        'parent_ids': 'ParentIds',
        'request_template': 'RequestTemplate',
        'resource': 'Resource',
    }

    def __init__(self, content=None, headers=None, method=None, parameters=None, parent_ids=None, request_template=None, resource=None):

        self._content = None
        self._headers = None
        self._method = None
        self._parameters = None
        self._parent_ids = None
        self._request_template = None
        self._resource = None

        if content is not None:
            self.content = content
        if headers is not None:
            self.headers = headers
        if method is not None:
            self.method = method
        if parameters is not None:
            self.parameters = parameters
        if parent_ids is not None:
            self.parent_ids = parent_ids
        if request_template is not None:
            self.request_template = request_template
        if resource is not None:
            self.resource = resource

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, headers):
        self._headers = headers

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, method):
        self._method = method

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        self._parameters = parameters

    @property
    def parent_ids(self):
        return self._parent_ids

    @parent_ids.setter
    def parent_ids(self, parent_ids):
        self._parent_ids = parent_ids

    @property
    def request_template(self):
        return self._request_template

    @request_template.setter
    def request_template(self, request_template):
        self._request_template = request_template

    @property
    def resource(self):
        return self._resource

    @resource.setter
    def resource(self, resource):
        self._resource = resource

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
        if not isinstance(other, PWARequest):
            return False
        return self.__dict__ == other.__dict__

