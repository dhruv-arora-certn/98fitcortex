from rest_framework import exceptions


class MultipleDiseasesException(exceptions.APIException):
	status = 404
	status_detail = "Multiple Diseases Found"
	default_code = "multiple_diseases"

class DiseasesNotDiabetesOrPcod(exceptions.APIException):
	status = 404
	status_detail = "Disease Is not Diabetes or PCOD"
	default_code = "unsupported_disease"
