from django import forms
from .models import Customer, Rooms
from .models import Hotels
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
class CustomerForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username','email']

    def __init__(self , *args , **kwargs):
        super(CustomerForm , self).__init__(*args , **kwargs)
        self.fields['username'].widget.attrs={'style': 'width:600px'}
        self.fields['email'].widget.attrs={'style': 'width:600px'}
        self.fields['password1'].widget.attrs={'style': 'width:600px'}
        self.fields['password2'].widget.attrs={'style': 'width:600px'}
        self.fields['password2'].label = 'password again'
        # self.fields['username'].widget.attrs['rows'] = 20

        for fieldname in ['username' , 'password1' , 'password2']:
            self.fields[fieldname].help_text = None
class LoginCustomerForm(AuthenticationForm):
    class Meta:
        model = Customer
        fields = ['username','password']
    def __init__(self , *args , **kwargs):
        super(LoginCustomerForm , self).__init__(*args , **kwargs)
        self.fields['username'].widget.attrs={'style': 'width:400px'}
        self.fields['password'].widget.attrs={'style': 'width:400px'}

class LoginStaffForm(AuthenticationForm):
    class Meta:
        model = Customer
        fields = ['username','password']
    def __init__(self , *args , **kwargs):
        super(LoginStaffForm , self).__init__(*args , **kwargs)
        self.fields['username'].widget.attrs={'style': 'width:400px'}
        self.fields['password'].widget.attrs={'style': 'width:400px'}


class StaffForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username','email','hotel_name']
    def __init__(self , *args , **kwargs):
        super(StaffForm , self).__init__(*args , **kwargs)
        self.fields['username'].widget.attrs={'style': 'width:600px'}
        self.fields['email'].widget.attrs={'style': 'width:600px'}
        self.fields['email'].required = True
        self.fields['password1'].widget.attrs={'style': 'width:600px'}
        self.fields['password2'].widget.attrs={'style': 'width:600px'}
        self.fields['hotel_name'].widget.attrs={'style': 'width:600px'}
        self.fields['password2'].label = 'password again'
        for fieldname in ['username' , 'password1' , 'password2']:
            self.fields[fieldname].help_text = None

    def save(self , *args , **kwargs):
        customer = super(StaffForm , self).save(commit=False)
        customer.is_staff=True
        customer.save()
        return customer

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotels
        exclude = ['owner']

    def __init__(self , *args , **kwargs):
        super(HotelForm , self).__init__(*args , **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.fields['photo'].widget.attrs = {'style': 'width:300px'}
        self.fields['photo'].required=True
        self.fields['name'].required=True
        self.fields['name'].widget.attrs = {'style': 'width:400px'}



class RoomForm(forms.ModelForm):

    class Meta:
        model = Rooms
        widgets = {
            'available_from': forms.DateInput(format=('%m/%d/%Y') ,
                                             attrs={'class': 'form-control' , 'placeholder': 'Select a date' ,
                                                    'type': 'date'}) ,
            'available_to': forms.DateInput(format=('%m/%d/%Y') ,
                                              attrs={'class': 'form-control' , 'placeholder': 'Select a date' ,
                                                     'type': 'date'}) ,
        }
        exclude = ['owner','hotel','booked']

    def __init__(self , *args , **kwargs):
        super(RoomForm , self).__init__(*args , **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.fields['photo'].widget.attrs = {'style': 'width:300px'}
        self.fields['room_name'].widget.attrs = {'style': 'width:400px'}
        self.fields['cost'].widget.attrs = {'style': 'width:400px'}
        self.fields['adults'].widget.attrs = {'style': 'width:400px'}
        self.fields['children'].widget.attrs = {'style': 'width:400px'}
        self.fields['available_from'].widget.attrs = {'style': 'width:400px'}
        self.fields['available_to'].widget.attrs = {'style': 'width:400px'}
        self.fields['location'].widget.attrs = {'style': 'width:400px'}
