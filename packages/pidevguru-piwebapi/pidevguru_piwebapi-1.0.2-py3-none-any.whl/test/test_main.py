# coding: utf-8

import unittest
from time import time

from pidevguru.piwebapi.models import PWAAnalysis, PWAItemsStreamValues, PWAStreamValues, PWATimedValue, PWARequest, PWAPoint, PWARequestTemplate, PWAValueQuery, PWASearchByAttribute
from pidevguru.piwebapi.pi_web_api_client import PIWebApiClient
from pidevguru.piwebapi.rest import ApiException
import time



class TestMain(unittest.TestCase):

    def getPIWebApiClient(self):
        piwebapi = PIWebApiClient("https://marc-pi2018.marc.net/piwebapi", False)
        piwebapi.set_basic_auth(username="marc.adm", password="1")
        return piwebapi


    def test_getHome(self):
        client = self.getPIWebApiClient()
        landing = client.home.get()
        pass


    def test_getDataServer(self):
        client = self.getPIWebApiClient()
        dataServer = client.dataServer.get_by_path("\\\\MARC-PI2018", None, None);
        dataServer2 = client.dataServer.get_by_path_with_http("\\\\MARC-PI2018");
        pass


    def test_getMultiplePoints(self):
        client = self.getPIWebApiClient()
        dataServers = client.dataServer.list(None, None)
        point1 = client.point.get_by_path("\\\\MARC-PI2018\\sinusoid")
        point2 = client.point.get_by_path("\\\\MARC-PI2018\\cdt158", None, None)
        point3 = client.point.get_by_path("\\\\MARC-PI2018\\sinusoidu", None, None)

        pass

    def test_getStreamSets(self):
        client = self.getPIWebApiClient()
        point1 = client.point.get_by_path("\\\\MARC-PI2018\\sinusoid", None, None);
        point2 = client.point.get_by_path("\\\\MARC-PI2018\\cdt158", None, None);
        point3 = client.point.get_by_path("\\\\MARC-PI2018\\sinusoidu", None, None);

        webIds = list()
        webIds.append(point1.web_id);
        webIds.append(point2.web_id);
        webIds.append(point3.web_id);


        result = client.streamSet.get_recorded_ad_hoc(webIds)

        pass



    def test_calculations(self):
        client = self.getPIWebApiClient()
        data_server = client.dataServer.get_by_path("\\\\MARC-PI2018", None, None);
        expression = "'sinusoid'*2 + 'cdt158'"
        time = list()
        time.append("*-1d")
        values = client.calculation.get_at_times(web_id=data_server.web_id, expression=expression, time=time)

        expression2 = "'cdt158'+tagval('sinusoid','*-1d')"
        values2 = client.calculation.get_at_times(web_id=data_server.web_id, expression=expression2, time=time)

        pass



    def test_getDataInBulkTest(self):
        client = self.getPIWebApiClient()
        point1 = client.point.get_by_path("\\\\MARC-PI2018\\sinusoid", None, None);
        point2 = client.point.get_by_path("\\\\MARC-PI2018\\cdt158", None, None);
        point3 = client.point.get_by_path("\\\\MARC-PI2018\\sinusoidu", None, None);

        webIds = list()
        webIds.append(point1.web_id);
        webIds.append(point2.web_id);
        webIds.append(point3.web_id);

        piItemsStreamValues = client.streamSet.get_recorded_ad_hoc(webIds, start_time="*-3d", end_time="*",
                                                                   include_filtered_values=True, max_count=1000)

        pass


    def test_getElement(self):
        client = self.getPIWebApiClient()
        element = client.element.get_by_path("\\\\MARC-PI2018\\CrossPlatformLab\\marc.adm")
        pass

    def test_searchByAttribute(self):
        client = self.getPIWebApiClient()
        element = client.element.get_by_path("\\\\MARC-PI2018\\Weather\Cities\\New York")
        element_template = client.elementTemplate.get_by_path("\\\\MARC-PI2018\\Weather\\ElementTemplates[CityTemplate]")
        value_query1 = PWAValueQuery(attribute_name="Pressure", attribute_value=10, search_operator="GreaterThan")
        values_queries = list()
        values_queries.append(value_query1)

        search_by_attribute = PWASearchByAttribute(search_root=element.web_id, element_template  = element_template.web_id, value_queries=values_queries);


        response =  client.element.create_search_by_attribute(search_by_attribute, False)

        pass


    def test_getAttribute(self):
        client = self.getPIWebApiClient()
        attribute = client.attribute.get_by_path("\\\\MARC-PI2018\\CrossPlatformLab\\marc.adm|Attribute1",
                                                 selected_fields="Name")
        pass

    def test_getExceptionError(self):
        client = self.getPIWebApiClient()
        try:
            point1 = client.point.get_by_path("\\\\MARC-PI2018\\sinusoid12334322")
        except ApiException as e:
            print(e);
            errorMsg = e.error['Errors'][0]
        pass

    def test_getBatch(self):
        client = self.getPIWebApiClient()
        landing = client.home.get();
        req1 = PWARequest()
        req2 = PWARequest()
        req3 = PWARequest()
        req4 = PWARequest()
        req1.method = "GET"
        req1.resource = "https://marc-pi2018.marc.net/piwebapi/points?path=\\\\MARC-PI2018\\sinusoid"
        req2.method = "GET"
        req2.resource = "https://marc-pi2018.marc.net/piwebapi/points?path=\\\\MARC-PI2018\\cdt158"
        req3.method = "GET"
        req3.resource = "https://marc-pi2018.marc.net/piwebapi/streamsets/value?webid={0}&webid={1}"
        req3.parameters = ["$.1.Content.WebId", "$.2.Content.WebId"]
        req3.parent_ids = ["1", "2"]

        req4.method = "GET"
        request_template = PWARequestTemplate()
        request_template.resource = "https://marc-pi2018.marc.net/piwebapi/streams/{0}/value"
        req4.request_template = request_template
        req4.parameters = ["$.3.Content.Items[*].WebId"]
        req4.parent_ids = ["3"]

        batch = {
            "1": req1,
            "2": req2,
            "3": req3,
            "4": req4
        }

        batchResponse = client.batch.execute(batch)
        point1 = client.api_client.deserialize_object(batchResponse["1"].content, 'PWAPoint')
        point2 = client.api_client.deserialize_object(batchResponse["2"].content, 'PWAPoint')
        itemsStreamValue = client.api_client.deserialize_object(batchResponse["3"].content, 'PWAItemsStreamValue')
        pass

    def test_updatePoint(self):
        client = self.getPIWebApiClient()
        sinusoid_point = client.point.get_by_path("\\\\marc-pi2018\\sinusoid");
        updated_point = PWAPoint()
        updated_point.descriptor = "New desc"
        client.point.update_with_http(sinusoid_point.web_id, updated_point)
        pass

    def test_updateValuesInBulk(self):
        client = self.getPIWebApiClient()
        point1 = client.point.get_by_path("\\\\MARC-PI2018\\sinusoid");
        point2 = client.point.get_by_path("\\\\MARC-PI2018\\cdt158", selected_fields="WebId");
        point3 = client.point.get_by_path("\\\\MARC-PI2018\\sinusoidu", web_id_type="PathOnly");
        streamValuesItems = PWAItemsStreamValues()
        streamValue1 = PWAStreamValues()
        streamValue2 = PWAStreamValues()
        streamValue3 = PWAStreamValues()
        value1 = PWATimedValue()
        value2 = PWATimedValue()
        value3 = PWATimedValue()
        value4 = PWATimedValue()
        value5 = PWATimedValue()
        value6 = PWATimedValue()
        value1.value = 2
        value1.timestamp = ("*-1d")
        value2.value = 3
        value2.timestamp = ("*-2d")
        value3.value = 4
        value3.timestamp = ("*-1d")
        value4.value = 5
        value4.timestamp = ("*-2d")
        value5.value = 6
        value5.timestamp = ("*-1d")
        value6.value = 7
        value6.timestamp = ("*-2d")

        streamValue1.web_id = point1.web_id
        streamValue2.web_id = point2.web_id
        streamValue3.web_id = point3.web_id

        values1 = list()
        values1.append(value1)
        values1.append(value2)
        streamValue1.items = values1

        values2 = list()
        values2.append(value3)
        values2.append(value4)
        streamValue2.items = values2

        values3 = list()
        values3.append(value5)
        values3.append(value6)
        streamValue3.items = values3

        streamValues = list()
        streamValues.append(streamValue1)
        streamValues.append(streamValue2)
        streamValues.append(streamValue3)
        response = client.streamSet.update_values_ad_hoc_with_http(streamValues)
        pass

if __name__ == '__main__':
    unittest.main()
