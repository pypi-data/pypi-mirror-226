from pprint import pformat
from six import iteritems


class PWAStreamUpdatesRetrieve(object):
    swagger_types = {
        'events': 'list[PWADataPipeEvent]',
        'exception': 'PWAErrors',
        'latest_marker': 'str',
        'requested_marker': 'str',
        'source': 'str',
        'source_name': 'str',
        'source_path': 'str',
        'status': 'str',
    }

    attribute_map = {
        'events': 'Events',
        'exception': 'Exception',
        'latest_marker': 'LatestMarker',
        'requested_marker': 'RequestedMarker',
        'source': 'Source',
        'source_name': 'SourceName',
        'source_path': 'SourcePath',
        'status': 'Status',
    }

    def __init__(self, events=None, exception=None, latest_marker=None, requested_marker=None, source=None, source_name=None, source_path=None, status=None):

        self._events = None
        self._exception = None
        self._latest_marker = None
        self._requested_marker = None
        self._source = None
        self._source_name = None
        self._source_path = None
        self._status = None

        if events is not None:
            self.events = events
        if exception is not None:
            self.exception = exception
        if latest_marker is not None:
            self.latest_marker = latest_marker
        if requested_marker is not None:
            self.requested_marker = requested_marker
        if source is not None:
            self.source = source
        if source_name is not None:
            self.source_name = source_name
        if source_path is not None:
            self.source_path = source_path
        if status is not None:
            self.status = status

    @property
    def events(self):
        return self._events

    @events.setter
    def events(self, events):
        self._events = events

    @property
    def exception(self):
        return self._exception

    @exception.setter
    def exception(self, exception):
        self._exception = exception

    @property
    def latest_marker(self):
        return self._latest_marker

    @latest_marker.setter
    def latest_marker(self, latest_marker):
        self._latest_marker = latest_marker

    @property
    def requested_marker(self):
        return self._requested_marker

    @requested_marker.setter
    def requested_marker(self, requested_marker):
        self._requested_marker = requested_marker

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        self._source = source

    @property
    def source_name(self):
        return self._source_name

    @source_name.setter
    def source_name(self, source_name):
        self._source_name = source_name

    @property
    def source_path(self):
        return self._source_path

    @source_path.setter
    def source_path(self, source_path):
        self._source_path = source_path

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

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
        if not isinstance(other, PWAStreamUpdatesRetrieve):
            return False
        return self.__dict__ == other.__dict__

