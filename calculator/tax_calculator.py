import json
from decimal import Decimal
import logging
logger = logging.getLogger(__name__)


class TaxCalculator:
    def __init__(self, salary, data):
        self.salary = salary
        self.data = data

    def get_tax_bands(self):
        """
        Returns Json object of tax bands.
        """
        try:
            logger.info("processing file data")
            return json.loads(str(self.data))
        except Exception as ex:
            logger.error(ex)

    def get_tax_amount(self):
        """
        Returns Tax amount owed.
        """
        try:
            bands = self.get_tax_bands()
            total_tax = 0
            salary = Decimal(self.salary)
            remainder = salary
            data = []
            ordered_bands = sorted(bands, key=lambda k: k['min_value'], reverse=True)
            for band in ordered_bands:
                    min_value = Decimal(band['min_value'])
                    max_value = Decimal(band['max_value'])
                    tax_rate = Decimal(band['tax_rate'])

                    if remainder >= min_value:
                        taxable = remainder - min_value
                        total_tax = total_tax + (taxable * tax_rate)
                        data.append({
                            'tax_rate': str(tax_rate),
                            'tax': str((taxable * tax_rate)),
                            'tax_range': '{} - {}'.format(min_value, max_value)
                        })
                        remainder = remainder - taxable
        except Exception as ex:
            logger.error(ex)
            return None
        logger.info("tax owed: {}".format(Decimal(round(total_tax, 2))))
        return Decimal(round(total_tax, 2)), data
