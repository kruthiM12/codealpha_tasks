import re
from django import forms
from django.contrib.auth.models import User
from .models import Order, UserProfile

INDIAN_STATES = [
    ('', 'Select State'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Delhi', 'Delhi (NCT)'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('West Bengal', 'West Bengal'),
]


class UserRegistrationForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Rahul Sharma', 'class': 'form-input'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'e.g. rahul.sharma@example.com', 'class': 'form-input'})
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. 9876543210', 'class': 'form-input'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Minimum 6 characters', 'class': 'form-input'}),
        required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter your password', 'class': 'form-input'}),
        required=True
    )

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        clean_p = re.sub(r'[\s\-\+]', '', phone)
        if clean_p.startswith('91') and len(clean_p) == 12:
            clean_p = clean_p[2:]
        if not re.match(r'^[6-9]\d{9}$', clean_p):
            raise forms.ValidationError(
                "Please enter a valid 10-digit Indian mobile number starting with 6, 7, 8, or 9."
            )
        return clean_p

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        if password and len(password) < 6:
            self.add_error('password', "Password must be at least 6 characters long.")
        return cleaned_data


class CheckoutForm(forms.ModelForm):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Rahul Sharma', 'class': 'form-input'})
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'e.g. 9876543210', 'class': 'form-input'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'e.g. rahul@example.com', 'class': 'form-input'})
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Flat 204, Building / Street Name', 'class': 'form-input'})
    )
    landmark = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Near Baner Hill / Axis Bank (Optional)', 'class': 'form-input'})
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Pune', 'class': 'form-input'})
    )
    state = forms.ChoiceField(
        choices=INDIAN_STATES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    pincode = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'e.g. 411045', 'class': 'form-input', 'maxlength': '6'})
    )
    payment_method = forms.ChoiceField(
        choices=Order.PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'payment-radio'})
    )

    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'email', 'address', 'landmark', 'city', 'state', 'pincode', 'payment_method']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        clean_p = re.sub(r'[\s\-\+]', '', phone)
        if clean_p.startswith('91') and len(clean_p) == 12:
            clean_p = clean_p[2:]
        if not re.match(r'^[6-9]\d{9}$', clean_p):
            raise forms.ValidationError(
                "Enter a valid 10-digit Indian mobile number (e.g. 9876543210)."
            )
        return clean_p

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode', '').strip()
        if not re.match(r'^[1-9]\d{5}$', pincode):
            raise forms.ValidationError("Enter a valid 6-digit Indian PIN Code (e.g. 411045).")
        return pincode


class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    landmark = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    state = forms.ChoiceField(choices=INDIAN_STATES, widget=forms.Select(attrs={'class': 'form-select'}))
    pincode = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'maxlength': '6'}))

    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'landmark', 'city', 'state', 'pincode']
