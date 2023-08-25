from pprint import pformat
from six import iteritems


class PWADeliveryChannelPlugInLinks(object):
    swagger_types = {
        'asset_server': 'str',
    }

    attribute_map = {
        'asset_server': 'AssetServer',
    }

    def __init__(self, asset_server=None):

        self._asset_server = None

        if asset_server is not None:
            self.asset_server = asset_server

    @property
    def asset_server(self):
        return self._asset_server

    @asset_server.setter
    def asset_server(self, asset_server):
        self._asset_server = asset_server

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
        if not isinstance(other, PWADeliveryChannelPlugInLinks):
            return False
        return self.__dict__ == other.__dict__

