from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Book, BookAssignment,BookRequest
from .forms import UserRegistrationForm, UserLoginForm, BookRequestForm, BookForm
from django.utils import timezone
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
#Login scenarios
def index(request):
    return render(request,'auth/index.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.user_type = form.cleaned_data['user_type']
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/register.html', {'form': form})

@csrf_exempt
def login_view(request):
    print("yes1")
    if request.method == 'POST':
        print("yes2")
        form = UserLoginForm(request.POST)
        if form.is_valid():
            print("yes3")
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print("no")
            try:
                print("yes")
                user = User.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    if user.user_type == 'librarian':
                        return redirect('ldashboard')  
                    else:
                        return redirect('udashboard')  
                else:
                    form.add_error('password', 'Incorrect password')
            except User.DoesNotExist:
                form.add_error('email', 'User does not exist')
    else:
        form = UserLoginForm()
    # return render(request, 'auth/login.html', {'form': form})
    return render(request, 'registration/login.html', {'form': form})


@login_required
def logout_view(request):
    request.session.flush()
    return redirect('login_view')

#User Dashboard and operation scenarios
@login_required
def udashboard(request):
    books = Book.objects.all() 
    context = {
        'books': books,
    }
    return render(request, 'user_dashboard/udashboard.html', context)

@login_required
def book_collection(request):
    if 'user_id' not in request.session:
        return redirect('user_login')
    
    user = User.objects.get(id=request.session['user_id'])
    allbooks = Book.objects.all()
    return render(request, 'book_collection.html', {'allbooks': allbooks})

@login_required
def my_books(request):
    if 'user_id' not in request.session:
        return redirect('user_login')
    
    user = User.objects.get(id=request.session['user_id'])
    assignments = BookAssignment.objects.filter(user=user)
    return render(request, 'user_dashboard/my_books.html', {'assignments': assignments})

@login_required
def request_book(request):
    user = User.objects.get(id=request.session['user_id'])  
    books = Book.objects.filter(is_available=True) 
    return render(request, 'user_dashboard/request_book.html', {'books': books})

#Librarian Dashboard and operation scenarios
@login_required
def ldashboard(request):
    print(request.user.is_authenticated)
    return render(request, 'lib_dashboard/ldashboard.html')

@login_required
def all_books_and_request(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id) 
    email = user.email 
    request_date = datetime.now().date() 
    
    if request.method == 'POST':
        existing_request = BookRequest.objects.filter(user=user,book=book,is_notified =False, request_date=request_date,status='pending').exists()
        
        if existing_request:
            messages.warning(request, 'You have already requested this book.')
        else:
            new_request = BookRequest(user=user, book=book, is_notified =False, request_date=request_date,status='pending')
            new_request.save()
            messages.success(request, 'Book request submitted successfully!')
        return redirect('udashboard')

    return render(request, 'user_dashboard/book_detail.html', {'book': book})

@login_required
def add_book(request):
    if request.method == 'POST':
        print("no")
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            print("yes")
            form.save()
            messages.success(request, "Book added successfully!")
            return redirect('ldashboard') 
    else:
        form = BookForm()
    return render(request, 'lib_dashboard/add_book.html', {'form': form})

@login_required
def stock_and_status(request):
    books = Book.objects.all() 
    return render(request, 'lib_dashboard/stock_and_status.html', {'books': books})

@login_required
def assi_revoke_list(request):
    assignments = BookAssignment.objects.filter(is_returned=False)  
    return render(request, 'lib_dashboard/assi_revoke_list.html', {'assignments': assignments})

@login_required
def assi_revoke(request, assignment_id):
    assignment = get_object_or_404(BookAssignment, id=assignment_id)
    book = assignment.book

    book.stock  += 1
    book.save()

    assignment.delete()
    messages.success(request, f'Assignment for "{book.title}" has been revoked and the book is now available.')

    return redirect('assi_revoke_list')  

@login_required
def pending(request):
    pending_requests = BookRequest.objects.filter(status='pending')
    
    context = {
        'pending_requests': pending_requests,
        'total_books': Book.objects.count(),
        'pending_requests_count': BookRequest.objects.filter(status='pending').count()
    }
    return render(request, 'lib_dashboard/pending.html', context)

@login_required
def approve_request(request, request_id):
    book_request = get_object_or_404(BookRequest, id=request_id)

    if book_request.book.stock > 0 and book_request.status == 'pending':
        book_request.status = 'approved'
        book_request.book.stock -= 1
        book_request.book.save()
        book_request.save()

        BookAssignment.objects.create(
            book=book_request.book,
            user=book_request.user,
            due_date=timezone.now() + timezone.timedelta(days=14)
        )
        messages.success(request, f'The request for "{book_request.book.title}" has been approved.')
    else:
        messages.error(request, f'Cannot approve the request for "{book_request.book.title}". No stock available or request is already processed.')

    return redirect('pending')

@login_required
def reject_request(request, request_id):
    book_request = get_object_or_404(BookRequest, id=request_id)
    if book_request.status == 'pending':
        book_request.status = 'rejected'
        book_request.save()
        messages.warning(request, f'You have rejected the request for "{book_request.book.title}".')

    return redirect('pending')
