from django.utils import timezone
from django.db import models

class User(models.Model):
    USER_TYPE_CHOICES = [
        ('user', 'User'),
        ('librarian', 'Librarian'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    contact = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.email 

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField(null=True, blank=True)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    stock = models.IntegerField(default=1)
    
    @property
    def available_stock(self):
        assigned_count = BookAssignment.objects.filter(book=self, is_returned=False).count()
        return self.stock - assigned_count
    
    def __str__(self):
        return self.title

class BookAssignment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    is_approved = models.BooleanField(default=False)
    renewal_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    renewal_date = models.DateField(null=True, blank=True) 

    def __str__(self):
        return f'{self.user.name}'

    @property
    def is_renewed(self):
        return self.renewal_date is not None
    
class BookRequest(models.Model):
    REQUEST_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    request_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=REQUEST_STATUS_CHOICES, default='pending')
    is_notified = models.BooleanField(default=False) 

    def __str__(self):
        return f'{self.user.name,self.book.title}'
      