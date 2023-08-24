from __future__ import absolute_import
from six import iteritems


class BatchControllerClient(object):
    def __init__(self, api_client):
        self.api_client = api_client

    def execute(self, batch, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.execute_with_http(batch, **kwargs)
        else:
            data = self.execute_with_http(batch, **kwargs)
            return data

    def execute_with_http(self, batch, **kwargs):
        all_params = list(['batch'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method execute_with_http" % key
                )
            params[key] = val
        del params['kwargs']

        if ('batch' not in params) or (params['batch'] is None):
            raise ValueError("Missing the required parameter `batch`")

        collection_formats = {}

        query_params = {}

        path_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'batch' in params:
            body_params = params['batch']

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/batch',
                                        'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='dict(str, PWAResponse)',
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)
