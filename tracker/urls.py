from django.urls import path
from . import views

urlpatterns = [
    # CRUD маршруты
    path('', views.TransactionListView.as_view(), name='transaction_list'),
    path('create/', views.TransactionCreateView.as_view(), name='transaction_create'),
    path('<int:pk>/update/', views.TransactionUpdateView.as_view(), name='transaction_update'),
    path('<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction_delete'),

    # API маршруты для динамических селектов
    path('api/categories/<int:type_id>/', views.CategoryByTypeListAPIView.as_view(), name='api_categories_by_type'),
    path('api/subcategories/<int:category_id>/', views.SubcategoryByCategoryListAPIView.as_view(), name='api_subcategories_by_category'),
]