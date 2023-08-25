from __future__ import absolute_import
from six import iteritems


class AnalysisControllerClient(object):
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

        return self.api_client.call_api('/analyses',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWAAnalysis',
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def get_analyses_query(self, database_web_id=None, max_count=None, query=None, selected_fields=None, start_index=None, web_id_type=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_analyses_query_with_http(database_web_id, max_count, query, selected_fields, start_index, web_id_type, **kwargs)
        else:
            data = self.get_analyses_query_with_http(database_web_id, max_count, query, selected_fields, start_index, web_id_type, **kwargs)
            return data

    def get_analyses_query_with_http(self, database_web_id=None, max_count=None, query=None, selected_fields=None, start_index=None, web_id_type=None, **kwargs):
        all_params = list(['database_web_id', 'max_count', 'query', 'selected_fields', 'start_index', 'web_id_type'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_analyses_query_with_http" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        query_params = {}

        path_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'database_web_id' in params:
            if params['database_web_id'] is not None:
                query_params['databaseWebId'] = params['database_web_id']
        if 'max_count' in params:
            if params['max_count'] is not None:
                query_params['maxCount'] = params['max_count']
        if 'query' in params:
            if params['query'] is not None:
                query_params['query'] = params['query']
        if 'selected_fields' in params:
            if params['selected_fields'] is not None:
                query_params['selectedFields'] = params['selected_fields']
        if 'start_index' in params:
            if params['start_index'] is not None:
                query_params['startIndex'] = params['start_index']
        if 'web_id_type' in params:
            if params['web_id_type'] is not None:
                query_params['webIdType'] = params['web_id_type']

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/analyses/search',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWAItemsAnalysis',
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def delete(self, web_id, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.delete_with_http(web_id, **kwargs)
        else:
            data = self.delete_with_http(web_id, **kwargs)
            return data

    def delete_with_http(self, web_id, **kwargs):
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
                    " to method delete_with_http" % key
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

        return self.api_client.call_api('/analyses/{webId}',
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

        return self.api_client.call_api('/analyses/{webId}',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWAAnalysis',
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def update(self, web_id, analysis, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.update_with_http(web_id, analysis, **kwargs)
        else:
            data = self.update_with_http(web_id, analysis, **kwargs)
            return data

    def update_with_http(self, web_id, analysis, **kwargs):
        all_params = list(['web_id', 'analysis'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_with_http" % key
                )
            params[key] = val
        del params['kwargs']

        if ('web_id' not in params) or (params['web_id'] is None):
            raise ValueError("Missing the required parameter `web_id`")

        if ('analysis' not in params) or (params['analysis'] is None):
            raise ValueError("Missing the required parameter `analysis`")

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
        if 'analysis' in params:
            body_params = params['analysis']

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/analyses/{webId}',
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

    def get_categories(self, web_id, selected_fields=None, web_id_type=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_categories_with_http(web_id, selected_fields, web_id_type, **kwargs)
        else:
            data = self.get_categories_with_http(web_id, selected_fields, web_id_type, **kwargs)
            return data

    def get_categories_with_http(self, web_id, selected_fields=None, web_id_type=None, **kwargs):
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
                    " to method get_categories_with_http" % key
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

        return self.api_client.call_api('/analyses/{webId}/categories',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWAItemsAnalysisCategory',
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def get_security(self, web_id, user_identity, force_refresh=None, selected_fields=None, web_id_type=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_security_with_http(web_id, user_identity, force_refresh, selected_fields, web_id_type, **kwargs)
        else:
            data = self.get_security_with_http(web_id, user_identity, force_refresh, selected_fields, web_id_type, **kwargs)
            return data

    def get_security_with_http(self, web_id, user_identity, force_refresh=None, selected_fields=None, web_id_type=None, **kwargs):
        all_params = list(['web_id', 'user_identity', 'force_refresh', 'selected_fields', 'web_id_type'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_security_with_http" % key
                )
            params[key] = val
        del params['kwargs']

        if ('web_id' not in params) or (params['web_id'] is None):
            raise ValueError("Missing the required parameter `web_id`")

        if ('user_identity' not in params) or (params['user_identity'] is None):
            raise ValueError("Missing the required parameter `user_identity`")

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
        if 'user_identity' in params:
            if params['user_identity'] is not None:
                query_params['userIdentity'] = params['user_identity']
                collection_formats['userIdentity'] = 'multi'
        if 'force_refresh' in params:
            if params['force_refresh'] is not None:
                query_params['forceRefresh'] = params['force_refresh']
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

        return self.api_client.call_api('/analyses/{webId}/security',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWAItemsSecurityRights',
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def get_security_entries(self, web_id, name_filter=None, selected_fields=None, web_id_type=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_security_entries_with_http(web_id, name_filter, selected_fields, web_id_type, **kwargs)
        else:
            data = self.get_security_entries_with_http(web_id, name_filter, selected_fields, web_id_type, **kwargs)
            return data

    def get_security_entries_with_http(self, web_id, name_filter=None, selected_fields=None, web_id_type=None, **kwargs):
        all_params = list(['web_id', 'name_filter', 'selected_fields', 'web_id_type'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_security_entries_with_http" % key
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
        if 'name_filter' in params:
            if params['name_filter'] is not None:
                query_params['nameFilter'] = params['name_filter']
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

        return self.api_client.call_api('/analyses/{webId}/securityentries',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWAItemsSecurityEntry',
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def create_security_entry(self, web_id, security_entry, apply_to_children=None, web_id_type=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.create_security_entry_with_http(web_id, security_entry, apply_to_children, web_id_type, **kwargs)
        else:
            data = self.create_security_entry_with_http(web_id, security_entry, apply_to_children, web_id_type, **kwargs)
            return data

    def create_security_entry_with_http(self, web_id, security_entry, apply_to_children=None, web_id_type=None, **kwargs):
        all_params = list(['web_id', 'security_entry', 'apply_to_children', 'web_id_type'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_security_entry_with_http" % key
                )
            params[key] = val
        del params['kwargs']

        if ('web_id' not in params) or (params['web_id'] is None):
            raise ValueError("Missing the required parameter `web_id`")

        if ('security_entry' not in params) or (params['security_entry'] is None):
            raise ValueError("Missing the required parameter `security_entry`")

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
        if 'security_entry' in params:
            body_params = params['security_entry']
        if 'apply_to_children' in params:
            if params['apply_to_children'] is not None:
                query_params['applyToChildren'] = params['apply_to_children']
        if 'web_id_type' in params:
            if params['web_id_type'] is not None:
                query_params['webIdType'] = params['web_id_type']

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/analyses/{webId}/securityentries',
                                        'POST',
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

    def delete_security_entry(self, name, web_id, apply_to_children=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.delete_security_entry_with_http(name, web_id, apply_to_children, **kwargs)
        else:
            data = self.delete_security_entry_with_http(name, web_id, apply_to_children, **kwargs)
            return data

    def delete_security_entry_with_http(self, name, web_id, apply_to_children=None, **kwargs):
        all_params = list(['name', 'web_id', 'apply_to_children'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_security_entry_with_http" % key
                )
            params[key] = val
        del params['kwargs']

        if ('name' not in params) or (params['name'] is None):
            raise ValueError("Missing the required parameter `name`")

        if ('web_id' not in params) or (params['web_id'] is None):
            raise ValueError("Missing the required parameter `web_id`")

        collection_formats = {}

        query_params = {}

        path_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'name' in params:
            if params['name'] is not None:
                path_params['name'] = params['name']
        if 'web_id' in params:
            if params['web_id'] is not None:
                path_params['webId'] = params['web_id']
        if 'apply_to_children' in params:
            if params['apply_to_children'] is not None:
                query_params['applyToChildren'] = params['apply_to_children']

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/analyses/{webId}/securityentries/{name}',
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

    def get_security_entry_by_name(self, name, web_id, selected_fields=None, web_id_type=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_security_entry_by_name_with_http(name, web_id, selected_fields, web_id_type, **kwargs)
        else:
            data = self.get_security_entry_by_name_with_http(name, web_id, selected_fields, web_id_type, **kwargs)
            return data

    def get_security_entry_by_name_with_http(self, name, web_id, selected_fields=None, web_id_type=None, **kwargs):
        all_params = list(['name', 'web_id', 'selected_fields', 'web_id_type'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_security_entry_by_name_with_http" % key
                )
            params[key] = val
        del params['kwargs']

        if ('name' not in params) or (params['name'] is None):
            raise ValueError("Missing the required parameter `name`")

        if ('web_id' not in params) or (params['web_id'] is None):
            raise ValueError("Missing the required parameter `web_id`")

        collection_formats = {}

        query_params = {}

        path_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'name' in params:
            if params['name'] is not None:
                path_params['name'] = params['name']
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

        return self.api_client.call_api('/analyses/{webId}/securityentries/{name}',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWASecurityEntry',
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def update_security_entry(self, name, web_id, security_entry, apply_to_children=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.update_security_entry_with_http(name, web_id, security_entry, apply_to_children, **kwargs)
        else:
            data = self.update_security_entry_with_http(name, web_id, security_entry, apply_to_children, **kwargs)
            return data

    def update_security_entry_with_http(self, name, web_id, security_entry, apply_to_children=None, **kwargs):
        all_params = list(['name', 'web_id', 'security_entry', 'apply_to_children'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_security_entry_with_http" % key
                )
            params[key] = val
        del params['kwargs']

        if ('name' not in params) or (params['name'] is None):
            raise ValueError("Missing the required parameter `name`")

        if ('web_id' not in params) or (params['web_id'] is None):
            raise ValueError("Missing the required parameter `web_id`")

        if ('security_entry' not in params) or (params['security_entry'] is None):
            raise ValueError("Missing the required parameter `security_entry`")

        collection_formats = {}

        query_params = {}

        path_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'name' in params:
            if params['name'] is not None:
                path_params['name'] = params['name']
        if 'web_id' in params:
            if params['web_id'] is not None:
                path_params['webId'] = params['web_id']
        if 'security_entry' in params:
            body_params = params['security_entry']
        if 'apply_to_children' in params:
            if params['apply_to_children'] is not None:
                query_params['applyToChildren'] = params['apply_to_children']

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/analyses/{webId}/securityentries/{name}',
                                        'PUT',
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
