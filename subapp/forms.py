from django import forms
from .models import User, BookAssignment, Book

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField()
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES)
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'contact']

    def clean_user_type(self):
        user_type = self.cleaned_data.get('user_type')
        if user_type not in ['user', 'librarian']:
            raise forms.ValidationError("Invalid user type")
        return user_type
        
class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

class BookRequestForm(forms.ModelForm):
    class Meta:
        model = BookAssignment
        fields = ['book', 'due_date']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publication_date', 'cover_image', 'stock']
        # data format - YYYY-MM-DD - add placeholder

        widgets = {
            'publication_date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD'
            }),
        #     'cover_image': forms.ImageField(attrs={
        #         'class': 'form-control-file',  
        #         'accept': 'image/*' 
        #     }),
        }

    # def clean_cover_image(self):
    #     cover_image = self.cleaned_data.get('cover_image')
    #     if not cover_image:
    #         raise forms.ValidationError("Cover image is mandatory")
    #     return cover_image
