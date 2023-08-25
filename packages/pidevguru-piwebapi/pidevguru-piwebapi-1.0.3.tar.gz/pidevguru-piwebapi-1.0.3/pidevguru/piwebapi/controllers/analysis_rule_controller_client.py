from __future__ import absolute_import
from six import iteritems


class AnalysisRuleControllerClient(object):
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

        return self.api_client.call_api('/analysisrules',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWAAnalysisRule',
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

        return self.api_client.call_api('/analysisrules/{webId}',
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

        return self.api_client.call_api('/analysisrules/{webId}',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWAAnalysisRule',
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def update(self, web_id, analysis_rule, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.update_with_http(web_id, analysis_rule, **kwargs)
        else:
            data = self.update_with_http(web_id, analysis_rule, **kwargs)
            return data

    def update_with_http(self, web_id, analysis_rule, **kwargs):
        all_params = list(['web_id', 'analysis_rule'])
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

        if ('analysis_rule' not in params) or (params['analysis_rule'] is None):
            raise ValueError("Missing the required parameter `analysis_rule`")

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
        if 'analysis_rule' in params:
            body_params = params['analysis_rule']

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/analysisrules/{webId}',
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

    def get_analysis_rules(self, web_id, max_count=None, name_filter=None, search_full_hierarchy=None, selected_fields=None, sort_field=None, sort_order=None, start_index=None, web_id_type=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_analysis_rules_with_http(web_id, max_count, name_filter, search_full_hierarchy, selected_fields, sort_field, sort_order, start_index, web_id_type, **kwargs)
        else:
            data = self.get_analysis_rules_with_http(web_id, max_count, name_filter, search_full_hierarchy, selected_fields, sort_field, sort_order, start_index, web_id_type, **kwargs)
            return data

    def get_analysis_rules_with_http(self, web_id, max_count=None, name_filter=None, search_full_hierarchy=None, selected_fields=None, sort_field=None, sort_order=None, start_index=None, web_id_type=None, **kwargs):
        all_params = list(['web_id', 'max_count', 'name_filter', 'search_full_hierarchy', 'selected_fields', 'sort_field', 'sort_order', 'start_index', 'web_id_type'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_analysis_rules_with_http" % key
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
        if 'max_count' in params:
            if params['max_count'] is not None:
                query_params['maxCount'] = params['max_count']
        if 'name_filter' in params:
            if params['name_filter'] is not None:
                query_params['nameFilter'] = params['name_filter']
        if 'search_full_hierarchy' in params:
            if params['search_full_hierarchy'] is not None:
                query_params['searchFullHierarchy'] = params['search_full_hierarchy']
        if 'selected_fields' in params:
            if params['selected_fields'] is not None:
                query_params['selectedFields'] = params['selected_fields']
        if 'sort_field' in params:
            if params['sort_field'] is not None:
                query_params['sortField'] = params['sort_field']
        if 'sort_order' in params:
            if params['sort_order'] is not None:
                query_params['sortOrder'] = params['sort_order']
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

        return self.api_client.call_api('/analysisrules/{webId}/analysisrules',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWAItemsAnalysisRule',
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def create_analysis_rule(self, web_id, analysis_rule, web_id_type=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.create_analysis_rule_with_http(web_id, analysis_rule, web_id_type, **kwargs)
        else:
            data = self.create_analysis_rule_with_http(web_id, analysis_rule, web_id_type, **kwargs)
            return data

    def create_analysis_rule_with_http(self, web_id, analysis_rule, web_id_type=None, **kwargs):
        all_params = list(['web_id', 'analysis_rule', 'web_id_type'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_analysis_rule_with_http" % key
                )
            params[key] = val
        del params['kwargs']

        if ('web_id' not in params) or (params['web_id'] is None):
            raise ValueError("Missing the required parameter `web_id`")

        if ('analysis_rule' not in params) or (params['analysis_rule'] is None):
            raise ValueError("Missing the required parameter `analysis_rule`")

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
        if 'analysis_rule' in params:
            body_params = params['analysis_rule']
        if 'web_id_type' in params:
            if params['web_id_type'] is not None:
                query_params['webIdType'] = params['web_id_type']

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/analysisrules/{webId}/analysisrules',
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
