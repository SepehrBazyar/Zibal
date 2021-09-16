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
        GET = request.GET
        return Response(
            Transaction.result(GET['type'], GET['mode'], GET.get('merchantId', None)),
            status=status.HTTP_200_OK
        )
