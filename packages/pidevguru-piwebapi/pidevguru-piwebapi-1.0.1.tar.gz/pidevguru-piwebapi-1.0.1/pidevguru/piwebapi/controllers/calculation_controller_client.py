from __future__ import absolute_import
from six import iteritems


class CalculationControllerClient(object):
    def __init__(self, api_client):
        self.api_client = api_client

    def get_at_intervals(self, expression, end_time=None, sample_interval=None, selected_fields=None, start_time=None, web_id=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_at_intervals_with_http(expression, end_time, sample_interval, selected_fields, start_time, web_id, **kwargs)
        else:
            data = self.get_at_intervals_with_http(expression, end_time, sample_interval, selected_fields, start_time, web_id, **kwargs)
            return data

    def get_at_intervals_with_http(self, expression, end_time=None, sample_interval=None, selected_fields=None, start_time=None, web_id=None, **kwargs):
        all_params = list(['expression', 'end_time', 'sample_interval', 'selected_fields', 'start_time', 'web_id'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_at_intervals_with_http" % key
                )
            params[key] = val
        del params['kwargs']

        if ('expression' not in params) or (params['expression'] is None):
            raise ValueError("Missing the required parameter `expression`")

        collection_formats = {}

        query_params = {}

        path_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'expression' in params:
            if params['expression'] is not None:
                query_params['expression'] = params['expression']
        if 'end_time' in params:
            if params['end_time'] is not None:
                query_params['endTime'] = params['end_time']
        if 'sample_interval' in params:
            if params['sample_interval'] is not None:
                query_params['sampleInterval'] = params['sample_interval']
        if 'selected_fields' in params:
            if params['selected_fields'] is not None:
                query_params['selectedFields'] = params['selected_fields']
        if 'start_time' in params:
            if params['start_time'] is not None:
                query_params['startTime'] = params['start_time']
        if 'web_id' in params:
            if params['web_id'] is not None:
                query_params['webId'] = params['web_id']

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/calculation/intervals',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWATimedValues',
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def get_at_recorded(self, expression, end_time=None, selected_fields=None, start_time=None, web_id=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_at_recorded_with_http(expression, end_time, selected_fields, start_time, web_id, **kwargs)
        else:
            data = self.get_at_recorded_with_http(expression, end_time, selected_fields, start_time, web_id, **kwargs)
            return data

    def get_at_recorded_with_http(self, expression, end_time=None, selected_fields=None, start_time=None, web_id=None, **kwargs):
        all_params = list(['expression', 'end_time', 'selected_fields', 'start_time', 'web_id'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_at_recorded_with_http" % key
                )
            params[key] = val
        del params['kwargs']

        if ('expression' not in params) or (params['expression'] is None):
            raise ValueError("Missing the required parameter `expression`")

        collection_formats = {}

        query_params = {}

        path_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'expression' in params:
            if params['expression'] is not None:
                query_params['expression'] = params['expression']
        if 'end_time' in params:
            if params['end_time'] is not None:
                query_params['endTime'] = params['end_time']
        if 'selected_fields' in params:
            if params['selected_fields'] is not None:
                query_params['selectedFields'] = params['selected_fields']
        if 'start_time' in params:
            if params['start_time'] is not None:
                query_params['startTime'] = params['start_time']
        if 'web_id' in params:
            if params['web_id'] is not None:
                query_params['webId'] = params['web_id']

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/calculation/recorded',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWATimedValues',
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def get_summary(self, expression, calculation_basis=None, end_time=None, sample_interval=None, sample_type=None, selected_fields=None, start_time=None, summary_duration=None, summary_type=None, time_type=None, web_id=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_summary_with_http(expression, calculation_basis, end_time, sample_interval, sample_type, selected_fields, start_time, summary_duration, summary_type, time_type, web_id, **kwargs)
        else:
            data = self.get_summary_with_http(expression, calculation_basis, end_time, sample_interval, sample_type, selected_fields, start_time, summary_duration, summary_type, time_type, web_id, **kwargs)
            return data

    def get_summary_with_http(self, expression, calculation_basis=None, end_time=None, sample_interval=None, sample_type=None, selected_fields=None, start_time=None, summary_duration=None, summary_type=None, time_type=None, web_id=None, **kwargs):
        all_params = list(['expression', 'calculation_basis', 'end_time', 'sample_interval', 'sample_type', 'selected_fields', 'start_time', 'summary_duration', 'summary_type', 'time_type', 'web_id'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_summary_with_http" % key
                )
            params[key] = val
        del params['kwargs']

        if ('expression' not in params) or (params['expression'] is None):
            raise ValueError("Missing the required parameter `expression`")

        collection_formats = {}

        query_params = {}

        path_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'expression' in params:
            if params['expression'] is not None:
                query_params['expression'] = params['expression']
        if 'calculation_basis' in params:
            if params['calculation_basis'] is not None:
                query_params['calculationBasis'] = params['calculation_basis']
        if 'end_time' in params:
            if params['end_time'] is not None:
                query_params['endTime'] = params['end_time']
        if 'sample_interval' in params:
            if params['sample_interval'] is not None:
                query_params['sampleInterval'] = params['sample_interval']
        if 'sample_type' in params:
            if params['sample_type'] is not None:
                query_params['sampleType'] = params['sample_type']
        if 'selected_fields' in params:
            if params['selected_fields'] is not None:
                query_params['selectedFields'] = params['selected_fields']
        if 'start_time' in params:
            if params['start_time'] is not None:
                query_params['startTime'] = params['start_time']
        if 'summary_duration' in params:
            if params['summary_duration'] is not None:
                query_params['summaryDuration'] = params['summary_duration']
        if 'summary_type' in params:
            if params['summary_type'] is not None:
                query_params['summaryType'] = params['summary_type']
                collection_formats['summaryType'] = 'multi'
        if 'time_type' in params:
            if params['time_type'] is not None:
                query_params['timeType'] = params['time_type']
        if 'web_id' in params:
            if params['web_id'] is not None:
                query_params['webId'] = params['web_id']

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/calculation/summary',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWAItemsSummaryValue',
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def get_at_times(self, expression, time, selected_fields=None, sort_order=None, web_id=None, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_at_times_with_http(expression, time, selected_fields, sort_order, web_id, **kwargs)
        else:
            data = self.get_at_times_with_http(expression, time, selected_fields, sort_order, web_id, **kwargs)
            return data

    def get_at_times_with_http(self, expression, time, selected_fields=None, sort_order=None, web_id=None, **kwargs):
        all_params = list(['expression', 'time', 'selected_fields', 'sort_order', 'web_id'])
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_at_times_with_http" % key
                )
            params[key] = val
        del params['kwargs']

        if ('expression' not in params) or (params['expression'] is None):
            raise ValueError("Missing the required parameter `expression`")

        if ('time' not in params) or (params['time'] is None):
            raise ValueError("Missing the required parameter `time`")

        collection_formats = {}

        query_params = {}

        path_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'expression' in params:
            if params['expression'] is not None:
                query_params['expression'] = params['expression']
        if 'time' in params:
            if params['time'] is not None:
                query_params['time'] = params['time']
                collection_formats['time'] = 'multi'
        if 'selected_fields' in params:
            if params['selected_fields'] is not None:
                query_params['selectedFields'] = params['selected_fields']
        if 'sort_order' in params:
            if params['sort_order'] is not None:
                query_params['sortOrder'] = params['sort_order']
        if 'web_id' in params:
            if params['web_id'] is not None:
                query_params['webId'] = params['web_id']

        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/json', 'text/html', 'application/x-ms-application'])

        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        return self.api_client.call_api('/calculation/times',
                                        'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PWATimedValues',
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)
