from rest_framework.test import APITestCase
from rest_framework import status


class TaxCalculatorTest(APITestCase):

    def test_salary_post_200_response(self):
        """
        Test a 200 response from url
        """
        data = {'salary': 52000.00}
        result = {"total_tax": '8299.60'}
        response = self.client.post('/calculator/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, result)

    def test_salary_post_result(self):
        """
        Test that the calculation works based of the following tax bands
        [{
            "min_value": 0,
            "max_value": 12500,
            "tax_rate": 0
          },{
            "min_value": 12501,
            "max_value": 50000,
            "tax_rate": 0.2
          },{
            "min_value": 50001,
            "max_value": 150000,
            "tax_rate": 0.4
          },{
            "min_value": 150001,
            "max_value": -1,
            "tax_rate": 0.45
          }]
        """
        data = {'salary': 52000.00}
        result = {"total_tax": '8299.60'}
        response = self.client.post('/calculator/', data, format='json')
        self.assertEqual(response.data, result)

    def test_salary_post_full_result(self):
        """
        Test that the full result is displayed based of the following tax bands:
        [{
            "min_value": 0,
            "max_value": 12500,
            "tax_rate": 0
          },{
            "min_value": 12501,
            "max_value": 50000,
            "tax_rate": 0.2
          },{
            "min_value": 50001,
            "max_value": 150000,
            "tax_rate": 0.4
          },{
            "min_value": 150001,
            "max_value": -1,
            "tax_rate": 0.45
        }]
        """
        data = {'salary': 52000.00, 'show_tax_bands': True}
        result = {
            'total_tax': '8299.60',
              'tax_bands': [
                  {
                      'tax_rate': '0.40000000000000002220446049250313080847263336181640625',
                      'tax': '799.6000000000000443867165245',
                      'tax_range': '50001 - 150000'
                  },
                  {
                      'tax_rate': '0.200000000000000011102230246251565404236316680908203125',
                      'tax': '7500.000000000000416333634234',
                      'tax_range': '12501 - 50000'
                  },
                  {
                      'tax_rate': '0',
                      'tax': '0.00',
                      'tax_range': '0 - 12500'
                  }
              ]
        }
        response = self.client.post('/calculator/', data, format='json')
        self.assertEqual(response.data, result)

