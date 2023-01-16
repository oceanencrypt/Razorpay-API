from unicodedata import name
from django.shortcuts import render
import razorpay
from .serializers import PaymentSerializer, VerifyPaymentSerializer
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.views import APIView
import json
from django.conf import settings

client = razorpay.Client(auth=(settings.RAZORPAY_ID_KEY, settings.RAZORPAY_SECRET_KEY))

class PaymentView(CreateAPIView):
    serializer_class =  PaymentSerializer

    def post(self, request):
        amount = request.data['amount']
        product_name = request.data['product_name']
        payment = client.order.create({"amount": int(amount) * 100, 
                                    "currency": "INR", 
                                    "payment_capture": "1"})

        data = {
                "callback_url": "http://127.0.0.1:8000/payment/callback",
                "razorpay_key": "rzp_test_dFP2CS0ZMKdXFz",
                "order": payment,
                "product_name": product_name
        }
        return Response({"data": data}, status=status.HTTP_200_OK)

class PaymentSuccessView(CreateAPIView):

    serializer_class =  VerifyPaymentSerializer

    def post(self, request):
        res = json.loads(request.data["response"])

        ord_id = ""
        raz_pay_id = ""
        raz_signature = ""

        for key in res.keys():
            if key == 'razorpay_order_id':
                ord_id = res[key]
            elif key == 'razorpay_payment_id':
                raz_pay_id = res[key]
            elif key == 'razorpay_signature':
                raz_signature = res[key]

        data = {
            'razorpay_order_id': ord_id,
            'razorpay_payment_id': raz_pay_id,
            'razorpay_signature': raz_signature
        }


        check = client.utility.verify_payment_signature(data)

        if check is not None:
            print("Redirect to error url or error page")
            return Response({'error': 'Something went wrong'})

        res_data = {
            'message': 'payment successfully received!'
        }

        return Response(res_data, status=status.HTTP_200_OK)