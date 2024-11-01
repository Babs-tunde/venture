from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('customers/', views.customer_list, name='customer_list'), 
    path('customers/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('customer/<int:customer_id>/transactions/', views.customer_transactions, name='customer_transactions'),
    path('customers/<int:customer_id>/record_payment/', views.customer_payment_view, name='customer_payment'),
    path('create_transaction/', views.create_transaction, name='create_transaction'),
    path('receipt/<int:transaction_id>/', views.receipt_view, name='receipt_view'),
    path('daily_sales/', views.daily_sales, name='daily_sales'),
    path('search/', views.search, name='search'),
    path('create_storebook/', views.create_storebook, name='create_storebook'),
    path('storebook/<int:storebook_id>/', views.storebook_detail, name='storebook_detail'),
    path('storebook/<int:storebook_id>/add_entry/', views.add_storebook_entry, name='add_storebook_entry'),
    path('storebook/<int:storebook_id>/record_payment/', views.record_payment, name='record_payment'),   
    path('storebook/', views.storebook_list, name='storebook_list'),
    path('posting_ledger/', views.posting_ledger, name='posting_ledger'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]



