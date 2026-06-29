import django_filters
from .models import Transaction

class TransactionFilter(django_filters.FilterSet):
    # Добавляем кастомные поля для фильтрации "от и до"
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte', label='Дата с')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte', label='Дата по')

    class Meta:
        model = Transaction
        fields = ['status', 'type', 'category', 'subcategory']