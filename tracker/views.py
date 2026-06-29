from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from rest_framework import generics, serializers

from .models import Transaction, Category, Subcategory
from .forms import TransactionForm
from .filters import TransactionFilter

# ==========================================
# Классические Django Views (CRUD + Фильтры)
# ==========================================

class TransactionListView(FilterView):
    model = Transaction
    template_name = 'tracker/transaction_list.html'
    context_object_name = 'transactions'
    filterset_class = TransactionFilter
    paginate_by = 20  # Пагинация (опционально)

class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'tracker/transaction_form.html'
    success_url = reverse_lazy('transaction_list')

class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'tracker/transaction_form.html'
    success_url = reverse_lazy('transaction_list')

class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'tracker/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction_list')


# ==========================================
# DRF Serializers & Views (API для фронтенда)
# ==========================================

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'name']

class CategoryByTypeListAPIView(generics.ListAPIView):
    """
    Возвращает список категорий, привязанных к конкретному ID типа.
    """
    serializer_class = CategorySerializer

    def get_queryset(self):
        type_id = self.kwargs.get('type_id')
        return Category.objects.filter(type_id=type_id)

class SubcategoryByCategoryListAPIView(generics.ListAPIView):
    """
    Возвращает список подкатегорий, привязанных к конкретному ID категории.
    """
    serializer_class = SubcategorySerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Subcategory.objects.filter(category_id=category_id)