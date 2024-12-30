from django.contrib import admin
from .models import User, Book, BookAssignment,BookRequest

#Registered models here
admin.site.register(User)
admin.site.register(Book)
admin.site.register(BookAssignment)
admin.site.register(BookRequest)