from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Transaction

# Create your views here.
class TransactionDetailAPIView(APIView):
    """
    API View for Show Detail of Transactions
    """

    def get(self, request, format=None):
        type, mode = request.GET.get('type'), request.GET.get('mode')
        merchantId = request.GET.get('merchantId')

        if type not in ('count', 'amount') or mode not in ('daily', 'weekly', 'monthly'):
            return Response({
                'detail': 'The Required Fields were not Satisfied.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = Transaction.result(type, mode, merchantId)
        except:
            return Response({
                'detail': f"'{merchantId}' is not a Valid ObjectId."
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            if response == []:
                return Response({
                    'detail': 'User Not Found.'
                }, status=status.HTTP_404_NOT_FOUND)

            return Response(response, status=status.HTTP_200_OK)
