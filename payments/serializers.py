from rest_framework import serializers


class PaymentSerializer(serializers.Serializer):
    product_name = serializers.CharField(required=False)
    amount = serializers.IntegerField(required=False)

    class Meta:
        fields = ["product_name", "amount"]

class ResponseSerializer(serializers.Serializer):
    razorpay_payment_id = serializers.CharField() 
    razorpay_order_id = serializers.CharField()
    razorpay_signature = serializers.CharField()

class VerifyPaymentSerializer(serializers.Serializer):
    response = ResponseSerializer()