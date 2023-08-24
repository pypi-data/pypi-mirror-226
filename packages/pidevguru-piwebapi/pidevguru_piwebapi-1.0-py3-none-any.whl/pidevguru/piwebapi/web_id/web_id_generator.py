# coding: utf-8
import base64

from pidevguru.piwebapi.models import PWAAttribute, PWAElement, PWAAssetServer, PWADataServer, PWAAnalysis, \
	PWAAnalysisTemplate, PWAElementTemplate, PWAEventFrame, PWAAnalysisCategory, PWAAnalysisRule, PWAAnalysisRulePlugIn, \
	PWAAttributeCategory, PWAAttributeTemplate, PWAAssetDatabase, PWAElementCategory, PWAEnumerationSet, PWAEnumerationValue, \
	PWATimeRule, PWATimeRulePlugIn, PWASecurityMapping, PWASecurityIdentity, PWATable, PWATableCategory, PWAPoint, PWAUnit, \
	PWAUnitClass
from pidevguru.piwebapi.web_id.web_id_exception import WebIdException

class WebIdGenerator(object):
	def __init__(self):
		self.marker_owner = None
		pass

	def generate_web_id_by_path(self, path,  objct_type, owner_type=None):
		self.validate_type_and_owner_type(objct_type, owner_type)
		marker = self.get_marker(objct_type)
		owner_marker = self.get_owner_marker(owner_type)
		if path[0:2] == "\\\\":
			path = path[2:]
		encoded_path = self.encode_string(path.upper())
		return "P1{}{}{}".format(marker, owner_marker, encoded_path)

	def validate_type_and_owner_type(self, object_type, owner_type):
		if isinstance(PWAAttribute(), object_type):
			if isinstance(PWAElement(), owner_type) and isinstance(PWAEventFrame(), owner_type):
				raise WebIdException("PIAttribte owner type must be a PIElement or a PIEventFrame.")
		elif isinstance(PWAAttributeTemplate(), object_type):
			if isinstance(PWAElementTemplate(), owner_type):
				raise WebIdException("PIElementTemplate owner type must be a PIElementTemplate.")
		elif isinstance(PWAEnumerationSet(), object_type) or isinstance(PWAEnumerationValue(), object_type):
			if isinstance(PWADataServer(), owner_type) == False and isinstance(PWAAssetServer(), owner_type) == False:
				raise  WebIdException("PIEnumerationSet and  PIEnumerationValue owner type must be a PIDataServer or PIAssetServer.")
		elif isinstance(PWATimeRule(), object_type):
			if isinstance(PWAAnalysis(), owner_type) and isinstance(PWAAnalysisTemplate(), owner_type):
				raise WebIdException("PITimeRule owner type must be a PIAnalysis and PIAnalysisTemplate.")

	def get_owner_marker(self, owner_type):
		if owner_type == None:
			return ""
		if isinstance(PWAAssetServer(),owner_type):
			self.marker_owner = "R"
		elif isinstance(PWADataServer(), owner_type):
			self.marker_owner = "D"
		elif isinstance(PWAAnalysis(), owner_type):
			self.marker_owner = "X"
		elif isinstance(PWAAnalysisTemplate(), owner_type):
			self.marker_owner = "T"
		elif isinstance(PWAElement(), owner_type):
			self.marker_owner = "E"
		if isinstance(PWAElementTemplate(), owner_type):
			self.marker_owner = "E"
		elif isinstance(PWAEventFrame(), owner_type):
			self.marker_owner = "F"
		return self.marker_owner

	def get_marker(self, object_type):
		marker = None

		if isinstance(PWAAnalysis(), object_type):
			marker = "Xs"
		elif isinstance(PWAAnalysisCategory(), object_type):
			marker = "XC"
		elif isinstance(PWAAnalysisTemplate(), object_type):
			marker = "XT"
		elif isinstance(PWAAnalysisRule(), object_type):
			marker = "XR"
		elif isinstance(PWAAnalysisRulePlugIn(), object_type):
			marker = "XP"
		elif isinstance(PWAAttribute(), object_type):
			marker = "Ab"
		elif isinstance(PWAAttributeCategory(), object_type):
			marker = "AC"
		elif isinstance(PWAAttributeTemplate(), object_type):
			marker = "AT"
		elif isinstance(PWAAssetDatabase(), object_type):
			marker = "RD"
		elif isinstance(PWAAssetServer(), object_type):
			marker = "RS"
		elif isinstance(PWAElement(), object_type):
			marker = "Em"
		elif isinstance(PWAElementCategory(), object_type):
			marker = "EC"
		elif isinstance(PWAElementTemplate(), object_type):
			marker = "ET"
		elif isinstance(PWAEnumerationSet(), object_type):
			marker = "MS"
		elif isinstance(PWAEnumerationValue(), object_type):
			marker = "MV"
		elif isinstance(PWAEventFrame(), object_type):
			marker = "Fm"
		elif isinstance(PWATimeRule(), object_type):
			marker = "TR"
		elif isinstance(PWATimeRulePlugIn(), object_type):
			marker = "TP"
		elif isinstance(PWASecurityIdentity(), object_type):
			marker = "SI"
		elif isinstance(PWASecurityMapping(), object_type):
			marker = "SM"
		elif isinstance(PWATable(), object_type):
			marker = "Bl"
		elif isinstance(PWATableCategory(), object_type):
			marker = "BC"
		elif isinstance(PWAPoint(), object_type):
			marker = "DP"
		elif isinstance(PWADataServer(), object_type):
			marker = "DS"
		elif isinstance(PWAUnit(), object_type):
			marker = "Ut"
		elif isinstance(PWAUnitClass(), object_type):
			marker = "UC"
		if (marker == None):
			raise WebIdException("Invalid object type.")
		return marker

	def encode_string(self, value):
		bytes = value.upper().encode('utf-8')
		return self.encode(bytes)

	def encode(self, value):
		encoded = base64.b64encode(value).decode()
		return encoded.strip('=').replace('+', '-').replace('/', '_')








