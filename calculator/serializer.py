from rest_framework import serializers


class CalculatorSerializer(serializers.Serializer):
    salary = serializers.DecimalField(max_digits=15, decimal_places=2, required=True)
    show_tax_bands = serializers.BooleanField(default=False)

    class Meta:
        fields = '__all__'
