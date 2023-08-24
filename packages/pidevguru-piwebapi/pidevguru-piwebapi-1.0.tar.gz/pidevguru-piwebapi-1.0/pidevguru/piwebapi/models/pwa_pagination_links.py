from pprint import pformat
from six import iteritems


class PWAPaginationLinks(object):
    swagger_types = {
        'first': 'str',
        'last': 'str',
        'next': 'str',
        'previous': 'str',
    }

    attribute_map = {
        'first': 'First',
        'last': 'Last',
        'next': 'Next',
        'previous': 'Previous',
    }

    def __init__(self, first=None, last=None, next=None, previous=None):

        self._first = None
        self._last = None
        self._next = None
        self._previous = None

        if first is not None:
            self.first = first
        if last is not None:
            self.last = last
        if next is not None:
            self.next = next
        if previous is not None:
            self.previous = previous

    @property
    def first(self):
        return self._first

    @first.setter
    def first(self, first):
        self._first = first

    @property
    def last(self):
        return self._last

    @last.setter
    def last(self, last):
        self._last = last

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next):
        self._next = next

    @property
    def previous(self):
        return self._previous

    @previous.setter
    def previous(self, previous):
        self._previous = previous

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
        if not isinstance(other, PWAPaginationLinks):
            return False
        return self.__dict__ == other.__dict__

