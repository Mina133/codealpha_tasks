# create event creation form
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Event, Registration

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'modern-input'})

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['number_of_tickets']
        widgets = {
            'number_of_tickets': forms.NumberInput(attrs={
                'min': 1,
                'class': 'modern-input'
            })
        }

    def __init__(self, *args, event=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = event

    def clean_number_of_tickets(self):
        tickets = self.cleaned_data['number_of_tickets']
        if self.event and tickets > self.event.max_tickets - self.event.tickets_sold:
            raise forms.ValidationError(f"Only {self.event.max_tickets - self.event.tickets_sold} tickets available")
        return tickets

class EventCreationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'date', 'time', 'duration', 'max_tickets', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'modern-input', 'placeholder': 'Event Name'}),
            'description': forms.Textarea(attrs={'class': 'modern-input', 'rows': 4, 'placeholder': 'Event Description'}),
            'location': forms.TextInput(attrs={'class': 'modern-input', 'placeholder': 'Event Location'}),
            'date': forms.DateInput(attrs={'class': 'modern-input', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'modern-input', 'type': 'time'}),
            'duration': forms.NumberInput(attrs={'class': 'modern-input', 'min': 1, 'placeholder': 'Duration in hours'}),
            'max_tickets': forms.NumberInput(attrs={'class': 'modern-input', 'min': 1, 'placeholder': 'Maximum tickets available'}),
            'price': forms.NumberInput(attrs={'class': 'modern-input', 'min': 0, 'step': '0.01', 'placeholder': 'Price per ticket'}),
            'image': forms.FileInput(attrs={'class': 'modern-input file-input'})
        }

        