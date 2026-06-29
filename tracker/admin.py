from django.contrib import admin
from .models import Status, Type, Category, Subcategory, Transaction

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')
    list_filter = ('type',) # Добавляем фильтр по типу сбоку

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_filter = ('category',) # Фильтр по категории

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'status', 'type', 'category', 'amount')
    list_filter = ('date', 'type', 'status')
    search_fields = ('comment',)