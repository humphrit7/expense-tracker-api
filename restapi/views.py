from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from restapi import models, serializers


class ExpenseListCreate(ListCreateAPIView):
    serializer_class = serializers.Expense
    queryset = models.Expense.objects.all()
    filterset_fields = ["category", "merchant"]


class ExpenseRetrieveDelete(RetrieveDestroyAPIView):
    serializer_class = serializers.Expense
    queryset = models.Expense.objects.all()
