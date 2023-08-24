from pidevguru.piwebapi import api_client
from pidevguru.piwebapi.controllers.batch_controller_client import BatchControllerClient
from pidevguru.piwebapi.controllers.home_controller_client import HomeControllerClient
from pidevguru.piwebapi.controllers.analysis_controller_client import AnalysisControllerClient
from pidevguru.piwebapi.controllers.analysis_category_controller_client import AnalysisCategoryControllerClient
from pidevguru.piwebapi.controllers.analysis_rule_plug_in_controller_client import AnalysisRulePlugInControllerClient
from pidevguru.piwebapi.controllers.analysis_rule_controller_client import AnalysisRuleControllerClient
from pidevguru.piwebapi.controllers.analysis_template_controller_client import AnalysisTemplateControllerClient
from pidevguru.piwebapi.controllers.asset_database_controller_client import AssetDatabaseControllerClient
from pidevguru.piwebapi.controllers.asset_server_controller_client import AssetServerControllerClient
from pidevguru.piwebapi.controllers.attribute_category_controller_client import AttributeCategoryControllerClient
from pidevguru.piwebapi.controllers.attribute_controller_client import AttributeControllerClient
from pidevguru.piwebapi.controllers.attribute_template_controller_client import AttributeTemplateControllerClient
from pidevguru.piwebapi.controllers.attribute_trait_controller_client import AttributeTraitControllerClient
from pidevguru.piwebapi.controllers.calculation_controller_client import CalculationControllerClient
from pidevguru.piwebapi.controllers.channel_controller_client import ChannelControllerClient
from pidevguru.piwebapi.controllers.data_server_controller_client import DataServerControllerClient
from pidevguru.piwebapi.controllers.element_category_controller_client import ElementCategoryControllerClient
from pidevguru.piwebapi.controllers.element_controller_client import ElementControllerClient
from pidevguru.piwebapi.controllers.element_template_controller_client import ElementTemplateControllerClient
from pidevguru.piwebapi.controllers.enumeration_set_controller_client import EnumerationSetControllerClient
from pidevguru.piwebapi.controllers.enumeration_value_controller_client import EnumerationValueControllerClient
from pidevguru.piwebapi.controllers.event_frame_controller_client import EventFrameControllerClient
from pidevguru.piwebapi.controllers.point_controller_client import PointControllerClient
from pidevguru.piwebapi.controllers.security_identity_controller_client import SecurityIdentityControllerClient
from pidevguru.piwebapi.controllers.security_mapping_controller_client import SecurityMappingControllerClient
from pidevguru.piwebapi.controllers.stream_controller_client import StreamControllerClient
from pidevguru.piwebapi.controllers.stream_set_controller_client import StreamSetControllerClient
from pidevguru.piwebapi.controllers.system_controller_client import SystemControllerClient
from pidevguru.piwebapi.controllers.configuration_controller_client import ConfigurationControllerClient
from pidevguru.piwebapi.controllers.table_category_controller_client import TableCategoryControllerClient
from pidevguru.piwebapi.controllers.table_controller_client import TableControllerClient
from pidevguru.piwebapi.controllers.time_rule_plug_in_controller_client import TimeRulePlugInControllerClient
from pidevguru.piwebapi.controllers.time_rule_controller_client import TimeRuleControllerClient
from pidevguru.piwebapi.controllers.unit_class_controller_client import UnitClassControllerClient
from pidevguru.piwebapi.controllers.unit_controller_client import UnitControllerClient

class PIWebApiClient(object):
    __baseUrl = None
    __username = None
    __password = None
    __verifySsl = True
    __config = None

    def __init__(self, baseUrl, verify_ssl=True):
        self.__baseUrl = baseUrl
        self.__verifySsl = verify_ssl
        self.__api_client = api_client.ApiClient(self.__baseUrl, self.__verifySsl)
        self.create_controllers()

    def set_basic_auth(self, username=None, password=None):
        self.__username = username
        self.__password = password
        self.__api_client.set_basic_auth(self.__username, self.__password)

    def set_kerberos_auth(self):
        self.__api_client.set_kerberos_auth()

    def create_controllers(self):
        self.__analysisApi = AnalysisControllerClient(self.__api_client)
        self.__analysisCategoryControllerClient = AnalysisCategoryControllerClient(self.__api_client)
        self.__analysisRulePlugInControllerClient = AnalysisRulePlugInControllerClient(self.__api_client)
        self.__analysisRuleControllerClient = AnalysisRuleControllerClient(self.__api_client)
        self.__analysisTemplateControllerClient = AnalysisTemplateControllerClient(self.__api_client)
        self.__assetDatabaseControllerClient = AssetDatabaseControllerClient(self.__api_client)
        self.__assetServerControllerClient = AssetServerControllerClient(self.__api_client)
        self.__attributeCategoryControllerClient = AttributeCategoryControllerClient(self.__api_client)
        self.__attributeControllerClient = AttributeControllerClient(self.__api_client)
        self.__attributeTemplateControllerClient = AttributeTemplateControllerClient(self.__api_client)
        self.__attributeTraitControllerClient = AttributeTraitControllerClient(self.__api_client)
        self.__calculationControllerClient = CalculationControllerClient(self.__api_client)
        self.__batchControllerClient = BatchControllerClient(self.__api_client)
        self.__channelControllerClient = ChannelControllerClient(self.__api_client)
        self.__dataServerControllerClient = DataServerControllerClient(self.__api_client)
        self.__elementCategoryControllerClient = ElementCategoryControllerClient(self.__api_client)
        self.__elementControllerClient = ElementControllerClient(self.__api_client)
        self.__elementTemplateControllerClient = ElementTemplateControllerClient(self.__api_client)
        self.__enumerationSetControllerClient = EnumerationSetControllerClient(self.__api_client)
        self.__enumerationValueControllerClient = EnumerationValueControllerClient(self.__api_client)
        self.__eventFrameControllerClient = EventFrameControllerClient(self.__api_client)
        self.__homeControllerClient = HomeControllerClient(self.__api_client)
        self.__pointControllerClient = PointControllerClient(self.__api_client)
        self.__securityIdentityControllerClient = SecurityIdentityControllerClient(self.__api_client)
        self.__securityMappingControllerClient = SecurityMappingControllerClient(self.__api_client)
        self.__streamControllerClient = StreamControllerClient(self.__api_client)
        self.__streamSetControllerClient = StreamSetControllerClient(self.__api_client)
        self.__systemControllerClient = SystemControllerClient(self.__api_client)
        self.__configurationControllerClient = ConfigurationControllerClient(self.__api_client)
        self.__tableCategoryControllerClient = TableCategoryControllerClient(self.__api_client)
        self.__tableControllerClient = TableControllerClient(self.__api_client)
        self.__timeRulePlugInControllerClient = TimeRulePlugInControllerClient(self.__api_client)
        self.__timeRuleControllerClient = TimeRuleControllerClient(self.__api_client)
        self.__unitClassControllerClient = UnitClassControllerClient(self.__api_client)
        self.__unitControllerClient = UnitControllerClient(self.__api_client)

    @property
    def api_client(self):
        return self.__api_client
    @property
    def baseUrl(self):
        return self.__baseUrl

    @property
    def useKerberos(self):
        return self.__useKerberos

    @property
    def verifySsl(self):
        return self.__verifySsl

    @property
    def home(self):
      return self.__homeControllerClient

    @property
    def analysis(self):
        return self.__analysisControllerClient

    @property
    def analysisCategory(self):
        return self.__analysisCategoryControllerClient

    @property
    def analysisRulePlugIn(self):
     return self.__analysisRulePlugInControllerClient

    @property
    def analysisRule(self):
        return self.__analysisRuleControllerClient

    @property
    def analysisTemplate(self):
        return self.__analysisTemplateControllerClient

    @property
    def assetDatabase(self):
        return self.__assetDatabaseControllerClient
    @property
    def assetServer(self):
        return self.__assetServerControllerClient
    @property
    def attributeCategory(self):
        return self.__attributeCategoryControllerClient

    @property
    def attribute(self):
        return self.__attributeControllerClient

    @property
    def attributeTemplate(self):
        return self.__attributeTemplateControllerClient

    @property
    def attributeTrait(self):
        return self.__attributeTraitControllerClient

    @property
    def batch(self):
        return self.__batchControllerClient;

    @property
    def calculation(self):
        return self.__calculationControllerClient

    @property
    def channel(self):
        return self.__channelControllerClient

    @property
    def dataServer(self):
        return self.__dataServerControllerClient

    @property
    def elementCategory(self):
        return self.__elementCategoryControllerClient

    @property
    def element(self):
        return self.__elementControllerClient

    @property
    def elementTemplate(self):
        return self.__elementTemplateControllerClient

    @property
    def enumerationSet(self):
        return self.__enumerationSetControllerClient

    @property
    def enumerationValue(self):
        return self.__enumerationValueControllerClient

    @property
    def eventFrame(self):
     return self.__eventFrameControllerClient

    @property
    def point(self):
        return self.__pointControllerClient

    @property
    def securityIdentity(self):
        return self.__securityIdentityControllerClient

    @property
    def securityMapping(self):
        return self.__securityMappingControllerClient

    @property
    def stream(self):
        return self.__streamControllerClient

    @property
    def streamSet(self):
        return self.__streamSetControllerClient

    @property
    def system(self):
        return self.__systemControllerClient

    @property
    def configuration(self):
     return self.__configurationControllerClient

    @property
    def tableCategory(self):
        return self.__tableCategoryControllerClient

    @property
    def table(self):
     return self.__tableControllerClient

    @property
    def timeRulePlugIn(self):
     return self.__timeRulePlugInControllerClient

    @property
    def timeRule(self):
     return self.__timeRuleControllerClient

    @property
    def unitClass(self):
        return self.__unitClassControllerClient

    @property
    def unit(self):
        return self.__unitControllerClient
