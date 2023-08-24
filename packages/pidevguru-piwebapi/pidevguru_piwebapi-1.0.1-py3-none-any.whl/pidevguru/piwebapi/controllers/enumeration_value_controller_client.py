from __future__ import absolute_import
from six import iteritems


class EnumerationValueControllerClient(object):
    def __init__(self, api_client):
        self.api_client = api_client

    def get_by_path(self, path, selected_fields=None, web_id_type=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_by_path_with_http(path, selected_fields, web_id_type, **kwargs)
        else:
            data = self.get_by_path_with_http(path, selected_fields, web_id_type, **kwargs)
            return data

    def get_by_path_with_http(self, path, selected_fields=None, web_id_type=None, **kwargs):
        all_params = list(['path', 'selected_fields', 'web_id_type'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_by_path_with_http" % key
                )
            params[key] = val
        del params['kwargs']

        if ('path' not in params) or (params['path'] is None):
            raise ValueError("Missing the required parameter `path`")

        collection_formats = {}

        query_params = {}

        path_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'path' in params:
            if params['path'] is not None:
                query_params['path'] = params['path']
        if 'selected_fields' in params:
            if params['selected_fields'] is not None:
                query_params['selectedFields'] = params['selected_fields']
        if 'web_id_type' in params:
            if params['web_id_type'] is not None:
                query_params['webIdType'] = params['web_id_type']

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/enumerationvalues',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWAEnumerationValue',
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def delete_enumeration_value(self, web_id, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.delete_enumeration_value_with_http(web_id, **kwargs)
        else:
            data = self.delete_enumeration_value_with_http(web_id, **kwargs)
            return data

    def delete_enumeration_value_with_http(self, web_id, **kwargs):
        all_params = list(['web_id'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_enumeration_value_with_http" % key
                )
            params[key] = val
        del params['kwargs']

        if ('web_id' not in params) or (params['web_id'] is None):
            raise ValueError("Missing the required parameter `web_id`")

        collection_formats = {}

        query_params = {}

        path_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'web_id' in params:
            if params['web_id'] is not None:
                path_params['webId'] = params['web_id']

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/enumerationvalues/{webId}',
                                        'DELETE',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type=None,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def get(self, web_id, selected_fields=None, web_id_type=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_with_http(web_id, selected_fields, web_id_type, **kwargs)
        else:
            data = self.get_with_http(web_id, selected_fields, web_id_type, **kwargs)
            return data

    def get_with_http(self, web_id, selected_fields=None, web_id_type=None, **kwargs):
        all_params = list(['web_id', 'selected_fields', 'web_id_type'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_with_http" % key
                )
            params[key] = val
        del params['kwargs']

        if ('web_id' not in params) or (params['web_id'] is None):
            raise ValueError("Missing the required parameter `web_id`")

        collection_formats = {}

        query_params = {}

        path_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'web_id' in params:
            if params['web_id'] is not None:
                path_params['webId'] = params['web_id']
        if 'selected_fields' in params:
            if params['selected_fields'] is not None:
                query_params['selectedFields'] = params['selected_fields']
        if 'web_id_type' in params:
            if params['web_id_type'] is not None:
                query_params['webIdType'] = params['web_id_type']

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/enumerationvalues/{webId}',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWAEnumerationValue',
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def update_enumeration_value(self, web_id, enumeration_value, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.update_enumeration_value_with_http(web_id, enumeration_value, **kwargs)
        else:
            data = self.update_enumeration_value_with_http(web_id, enumeration_value, **kwargs)
            return data

    def update_enumeration_value_with_http(self, web_id, enumeration_value, **kwargs):
        all_params = list(['web_id', 'enumeration_value'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_enumeration_value_with_http" % key
                )
            params[key] = val
        del params['kwargs']

        if ('web_id' not in params) or (params['web_id'] is None):
            raise ValueError("Missing the required parameter `web_id`")

        if ('enumeration_value' not in params) or (params['enumeration_value'] is None):
            raise ValueError("Missing the required parameter `enumeration_value`")

        collection_formats = {}

        query_params = {}

        path_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'web_id' in params:
            if params['web_id'] is not None:
                path_params['webId'] = params['web_id']
        if 'enumeration_value' in params:
            body_params = params['enumeration_value']

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/enumerationvalues/{webId}',
                                        'PATCH',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type=None,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)
