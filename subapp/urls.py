from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #Login scenarios
    path("", views.index,name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.index, name='logout'),
    path('register/', views.register_view, name='register'),


    #User Dashboard and operation scenarios
    path('udashboard/', views.udashboard, name='udashboard'),
    # path('available_book/', views.available_book, name='available_book'),
    path('my_books/', views.my_books, name='my_books'),
        #to request
    path('request_book/', views.request_book, name='request_book'),
    path('all_books_and_request/<int:book_id>/', views.all_books_and_request, name='all_books_and_request'), 
    
    
     #Librarian Dashboard and operation scenarios
    path('ldashboard/', views.ldashboard, name='ldashboard'), 
    # path('librarian_dashboard/', views.librarian_dashboard, name='librarian_dashboard'),
    path('book_collection/', views.book_collection, name='book_collection'),
        #stock scenarios
    path('stock_and_status/', views.stock_and_status, name='stock_and_status'),
        # revoking scenarios
    path('assi_revoke_list/', views.assi_revoke_list, name='assi_revoke_list'),
    path('assi_revoke/<int:assignment_id>/', views.assi_revoke, name='assi_revoke'),
        # Pending requests scenarios
    path('pending/', views.pending, name='pending'), 
    path('approve/<int:request_id>/', views.approve_request, name='approve'),
    path('reject/<int:request_id>', views.reject_request, name='reject'),
        # Add book scenarios
    path('add_book/', views.add_book, name='add_book'),

]