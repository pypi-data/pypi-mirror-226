from __future__ import absolute_import
from six import iteritems


class AttributeControllerClient(object):
    def __init__(self, api_client):
        self.api_client = api_client

    def get_by_path(self, path, associations=None, selected_fields=None, web_id_type=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_by_path_with_http(path, associations, selected_fields, web_id_type, **kwargs)
        else:
            data = self.get_by_path_with_http(path, associations, selected_fields, web_id_type, **kwargs)
            return data

    def get_by_path_with_http(self, path, associations=None, selected_fields=None, web_id_type=None, **kwargs):
        all_params = list(['path', 'associations', 'selected_fields', 'web_id_type'])
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
        if 'associations' in params:
            if params['associations'] is not None:
                query_params['associations'] = params['associations']
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

        return self.api_client.call_api('/attributes',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWAAttribute',
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def get_multiple(self, as_parallel=None, associations=None, include_mode=None, path=None, selected_fields=None, web_id=None, web_id_type=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_multiple_with_http(as_parallel, associations, include_mode, path, selected_fields, web_id, web_id_type, **kwargs)
        else:
            data = self.get_multiple_with_http(as_parallel, associations, include_mode, path, selected_fields, web_id, web_id_type, **kwargs)
            return data

    def get_multiple_with_http(self, as_parallel=None, associations=None, include_mode=None, path=None, selected_fields=None, web_id=None, web_id_type=None, **kwargs):
        all_params = list(['as_parallel', 'associations', 'include_mode', 'path', 'selected_fields', 'web_id', 'web_id_type'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_multiple_with_http" % key
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
        if 'as_parallel' in params:
            if params['as_parallel'] is not None:
                query_params['asParallel'] = params['as_parallel']
        if 'associations' in params:
            if params['associations'] is not None:
                query_params['associations'] = params['associations']
        if 'include_mode' in params:
            if params['include_mode'] is not None:
                query_params['includeMode'] = params['include_mode']
        if 'path' in params:
            if params['path'] is not None:
                query_params['path'] = params['path']
                collection_formats['path'] = 'multi'
        if 'selected_fields' in params:
            if params['selected_fields'] is not None:
                query_params['selectedFields'] = params['selected_fields']
        if 'web_id' in params:
            if params['web_id'] is not None:
                query_params['webId'] = params['web_id']
                collection_formats['webId'] = 'multi'
        if 'web_id_type' in params:
            if params['web_id_type'] is not None:
                query_params['webIdType'] = params['web_id_type']

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/attributes/multiple',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWAItemsItemAttribute',
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def get_attributes_query(self, associations=None, database_web_id=None, max_count=None, query=None, selected_fields=None, start_index=None, web_id_type=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_attributes_query_with_http(associations, database_web_id, max_count, query, selected_fields, start_index, web_id_type, **kwargs)
        else:
            data = self.get_attributes_query_with_http(associations, database_web_id, max_count, query, selected_fields, start_index, web_id_type, **kwargs)
            return data

    def get_attributes_query_with_http(self, associations=None, database_web_id=None, max_count=None, query=None, selected_fields=None, start_index=None, web_id_type=None, **kwargs):
        all_params = list(['associations', 'database_web_id', 'max_count', 'query', 'selected_fields', 'start_index', 'web_id_type'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_attributes_query_with_http" % key
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
        if 'associations' in params:
            if params['associations'] is not None:
                query_params['associations'] = params['associations']
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

        return self.api_client.call_api('/attributes/search',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWAItemsAttribute',
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

        return self.api_client.call_api('/attributes/{webId}',
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

    def get(self, web_id, associations=None, selected_fields=None, web_id_type=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_with_http(web_id, associations, selected_fields, web_id_type, **kwargs)
        else:
            data = self.get_with_http(web_id, associations, selected_fields, web_id_type, **kwargs)
            return data

    def get_with_http(self, web_id, associations=None, selected_fields=None, web_id_type=None, **kwargs):
        all_params = list(['web_id', 'associations', 'selected_fields', 'web_id_type'])
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
        if 'associations' in params:
            if params['associations'] is not None:
                query_params['associations'] = params['associations']
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

        return self.api_client.call_api('/attributes/{webId}',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWAAttribute',
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def update(self, web_id, attribute, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.update_with_http(web_id, attribute, **kwargs)
        else:
            data = self.update_with_http(web_id, attribute, **kwargs)
            return data

    def update_with_http(self, web_id, attribute, **kwargs):
        all_params = list(['web_id', 'attribute'])
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

        if ('attribute' not in params) or (params['attribute'] is None):
            raise ValueError("Missing the required parameter `attribute`")

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
        if 'attribute' in params:
            body_params = params['attribute']

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/attributes/{webId}',
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

    def get_attributes(self, web_id, associations=None, category_name=None, max_count=None, name_filter=None, search_full_hierarchy=None, selected_fields=None, show_excluded=None, show_hidden=None, sort_field=None, sort_order=None, start_index=None, template_name=None, trait=None, trait_category=None, value_type=None, web_id_type=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_attributes_with_http(web_id, associations, category_name, max_count, name_filter, search_full_hierarchy, selected_fields, show_excluded, show_hidden, sort_field, sort_order, start_index, template_name, trait, trait_category, value_type, web_id_type, **kwargs)
        else:
            data = self.get_attributes_with_http(web_id, associations, category_name, max_count, name_filter, search_full_hierarchy, selected_fields, show_excluded, show_hidden, sort_field, sort_order, start_index, template_name, trait, trait_category, value_type, web_id_type, **kwargs)
            return data

    def get_attributes_with_http(self, web_id, associations=None, category_name=None, max_count=None, name_filter=None, search_full_hierarchy=None, selected_fields=None, show_excluded=None, show_hidden=None, sort_field=None, sort_order=None, start_index=None, template_name=None, trait=None, trait_category=None, value_type=None, web_id_type=None, **kwargs):
        all_params = list(['web_id', 'associations', 'category_name', 'max_count', 'name_filter', 'search_full_hierarchy', 'selected_fields', 'show_excluded', 'show_hidden', 'sort_field', 'sort_order', 'start_index', 'template_name', 'trait', 'trait_category', 'value_type', 'web_id_type'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_attributes_with_http" % key
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
        if 'associations' in params:
            if params['associations'] is not None:
                query_params['associations'] = params['associations']
        if 'category_name' in params:
            if params['category_name'] is not None:
                query_params['categoryName'] = params['category_name']
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
        if 'show_excluded' in params:
            if params['show_excluded'] is not None:
                query_params['showExcluded'] = params['show_excluded']
        if 'show_hidden' in params:
            if params['show_hidden'] is not None:
                query_params['showHidden'] = params['show_hidden']
        if 'sort_field' in params:
            if params['sort_field'] is not None:
                query_params['sortField'] = params['sort_field']
        if 'sort_order' in params:
            if params['sort_order'] is not None:
                query_params['sortOrder'] = params['sort_order']
        if 'start_index' in params:
            if params['start_index'] is not None:
                query_params['startIndex'] = params['start_index']
        if 'template_name' in params:
            if params['template_name'] is not None:
                query_params['templateName'] = params['template_name']
        if 'trait' in params:
            if params['trait'] is not None:
                query_params['trait'] = params['trait']
                collection_formats['trait'] = 'multi'
        if 'trait_category' in params:
            if params['trait_category'] is not None:
                query_params['traitCategory'] = params['trait_category']
                collection_formats['traitCategory'] = 'multi'
        if 'value_type' in params:
            if params['value_type'] is not None:
                query_params['valueType'] = params['value_type']
        if 'web_id_type' in params:
            if params['web_id_type'] is not None:
                query_params['webIdType'] = params['web_id_type']

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/attributes/{webId}/attributes',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWAItemsAttribute',
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def create_attribute(self, web_id, attribute, web_id_type=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.create_attribute_with_http(web_id, attribute, web_id_type, **kwargs)
        else:
            data = self.create_attribute_with_http(web_id, attribute, web_id_type, **kwargs)
            return data

    def create_attribute_with_http(self, web_id, attribute, web_id_type=None, **kwargs):
        all_params = list(['web_id', 'attribute', 'web_id_type'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_attribute_with_http" % key
                )
            params[key] = val
        del params['kwargs']

        if ('web_id' not in params) or (params['web_id'] is None):
            raise ValueError("Missing the required parameter `web_id`")

        if ('attribute' not in params) or (params['attribute'] is None):
            raise ValueError("Missing the required parameter `attribute`")

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
        if 'attribute' in params:
            body_params = params['attribute']
        if 'web_id_type' in params:
            if params['web_id_type'] is not None:
                query_params['webIdType'] = params['web_id_type']

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/attributes/{webId}/attributes',
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

        return self.api_client.call_api('/attributes/{webId}/categories',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWAItemsAttributeCategory',
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def create_config(self, web_id, web_id_type=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.create_config_with_http(web_id, web_id_type, **kwargs)
        else:
            data = self.create_config_with_http(web_id, web_id_type, **kwargs)
            return data

    def create_config_with_http(self, web_id, web_id_type=None, **kwargs):
        all_params = list(['web_id', 'web_id_type'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_config_with_http" % key
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
        if 'web_id_type' in params:
            if params['web_id_type'] is not None:
                query_params['webIdType'] = params['web_id_type']

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/attributes/{webId}/config',
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

    def get_value(self, web_id, selected_fields=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_value_with_http(web_id, selected_fields, **kwargs)
        else:
            data = self.get_value_with_http(web_id, selected_fields, **kwargs)
            return data

    def get_value_with_http(self, web_id, selected_fields=None, **kwargs):
        all_params = list(['web_id', 'selected_fields'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_value_with_http" % key
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

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/attributes/{webId}/value',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWATimedValue',
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def set_value(self, web_id, value, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.set_value_with_http(web_id, value, **kwargs)
        else:
            data = self.set_value_with_http(web_id, value, **kwargs)
            return data

    def set_value_with_http(self, web_id, value, **kwargs):
        all_params = list(['web_id', 'value'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method set_value_with_http" % key
                )
            params[key] = val
        del params['kwargs']

        if ('web_id' not in params) or (params['web_id'] is None):
            raise ValueError("Missing the required parameter `web_id`")

        if ('value' not in params) or (params['value'] is None):
            raise ValueError("Missing the required parameter `value`")

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
        if 'value' in params:
            body_params = params['value']

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/attributes/{webId}/value',
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
