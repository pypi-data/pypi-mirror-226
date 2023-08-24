# coding: utf-8
import  unittest
from pidevguru.piwebapi.models import PWAPoint, PWADataServer, PWAElement, PWAAttribute
from pidevguru.piwebapi.pi_web_api_client import PIWebApiClient
from pidevguru.piwebapi.web_id import WebIdGenerator


class TestMain(unittest.TestCase):

    def getPIWebApiClient(self):
        piwebapi = PIWebApiClient("https://marc-pi2018.marc.net/piwebapi", False)
        piwebapi.set_basic_auth(username="marc.adm", password="1")
        return piwebapi

    def test_generateWebIdInfo(self):
        client = self.getPIWebApiClient()
        path = "\\\\MARC-PI2018\\CDT158"
        webIdHelper = WebIdGenerator()
        web_id1 = webIdHelper.generate_web_id_by_path("\\\\MARC-PI2018\\CDT158", type(PWAPoint()))
        pt = client.point.get(selected_fields="WebId", web_id=web_id1)
        web_id2 = webIdHelper.generate_web_id_by_path("\\\\MARC-PI2018", type(PWADataServer()))
        ds = client.dataServer.get(web_id2)
        pass

    def test_more_tests(self):
        client = self.getPIWebApiClient()
        webIdHelper = WebIdGenerator()
        pi_data_server_web_id = webIdHelper.generate_web_id_by_path("\\\\MARC-PI2018", type(PWADataServer()), None)
        point1_web_id = webIdHelper.generate_web_id_by_path("\\\\MARC-PI2018\\SINUSOID", type(PWAPoint()))
        point2_web_id = webIdHelper.generate_web_id_by_path("\\\\MARC-PI2018\\CDT158", type(PWAPoint()))
        point3_web_id = webIdHelper.generate_web_id_by_path("\\\\MARC-PI2018\\SINUSOIDU", type(PWAPoint()))
        pi_attribute_web_id = webIdHelper.generate_web_id_by_path(
            "\\\\MARC-PI2018\\Weather\\Cities\\New York|Pressure",
            type(PWAAttribute()), type(PWAElement()))

        pi_element_web_id = webIdHelper.generate_web_id_by_path(
            "\\\\MARC-PI2018\\Weather\\Cities\\New York", type(PWAElement()), None)

        pi_data_server = client.dataServer.get(pi_data_server_web_id)
        pi_attribute = client.attribute.get(pi_attribute_web_id)
        pi_element = client.element.get(pi_element_web_id)


if __name__ == '__main__':
    unittest.main()
