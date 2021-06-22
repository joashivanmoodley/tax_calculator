from rest_framework.response import Response
from rest_framework.views import APIView
from calculator.serializer import CalculatorSerializer
from calculator.tax_calculator import TaxCalculator
from django.conf import settings
import logging
import os
import requests
logger = logging.getLogger(__name__)


def get_latest_data():
    url = 'https://raw.githubusercontent.com/joashivanmoodley/tax_calculator/main/tax_band.json'
    r = requests.get(url, allow_redirects=True)
    os.remove("{}/tax_band.json".format(settings.BASE_DIR))
    open("{}/tax_band.json".format(settings.BASE_DIR), 'w').write(str(r.json()))


class CalculatorView(APIView):
    """
    post:
    Get Tax owed based on Annual Salary.
    parameters:
         -name: username
          description: Foobar long description goes here
          required: true
          type: string
          paramType: form
        - salary: salary
        - show_tax_bands: show_tax_bands
    """

    @staticmethod
    def post(request):
        try:
            data = request.data
            serializer = CalculatorSerializer(data=data)
            if serializer.is_valid():
                salary = serializer.data['salary']
                if 'refresh_data' in serializer.data:
                    refresh_data = serializer.data['refresh_data']
                    if refresh_data:
                        get_latest_data()

                tax_filename = "{}/tax_band.json".format(settings.BASE_DIR)
                tax_file = open(tax_filename, "r")
                tax_bands = tax_file.read()
                tax_file.close()
                cal = TaxCalculator(salary, tax_bands)
                tax_amount, tax_data = cal.get_tax_amount()
                results = {'total_tax': str(tax_amount)}
                show_tax_bands = False
                if 'show_tax_bands' in serializer.data:
                    show_tax_bands = serializer.data['show_tax_bands']
                if show_tax_bands:
                    results['tax_bands'] = tax_data
                logger.info('{}'.format(results))
                return Response(results)
            else:
                return Response({"{}".format(serializer.errors)})
        except Exception as ex:
            logger.error(ex)
            return Response('{}'.format(ex))
