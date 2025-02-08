from django.shortcuts import render
from .models import Transactions
from rest_framework.response import Response
from .serializers import TransactionsSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.db.models import Sum

# Create your views here.

@api_view(['GET','POST'])
def get_transactions(request):
        queryset = Transactions.objects.all().order_by('-pk')
        serializer = TransactionsSerializer(queryset, many=True)

        return Response({
                "data": serializer.data
        })

class TransactionsAPI(APIView):
        def get(self,request):
                queryset = Transactions.objects.all()
                serializer = TransactionsSerializer(queryset, many=True)

                return Response({
                        "data": serializer.data,
                        "total" : round(queryset.aggregate(total = Sum('amount'))['total'] or 0,4),
                })
                
        def put(self, request):
                data = request.data
                serializer = TransactionsSerializer(data = data)
                if not serializer.is_valid():

                        return Response({
                                "message" : "Data not saved",
                                "errors" : serializer.errors,
                        })
                serializer.save()
                return Response({
                        "message" : "Data is Saved",
                        "data" : serializer.data,
                })
        
        def patch(self, request):
                data = request.data
                if not data.get('id'):
                        return Response({
                                "message" : "Data not updated",
                                "errors" : "Id is required"
                        })
                
                Transaction = Transactions.objects.get(id = data.get('id'))
                serializer = TransactionsSerializer(Transaction, data = data, partial = True)


        def delete(self, request):
                data = request.data
                if not data.get('id'):
                        return Response({
                                "message" : "Data not updated",
                                "errors" : "Id is required"
                        })
                
                Transaction = Transactions.objects.get(id = data.get('id'))
                serializer = TransactionsSerializer(Transaction, data = data, partial = True)

                return Response({
                        "message" : "Data Deleted",
                        "data" : {}
                })
