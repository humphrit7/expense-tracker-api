from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from restapi import models, serializers


class ExpenseListCreate(APIView):
    def get(self, request):
        expenses = models.Expense.objects.all()
        serializer = serializers.Expense(expenses, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = serializers.Expense(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
