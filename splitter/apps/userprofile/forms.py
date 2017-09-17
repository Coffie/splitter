from django import forms

class PaymentForm(forms.Form):
    amount = forms.CharField(max_length=10)
    message = forms.CharField(max_length=64)
    
    def clean(self):
        cleaned_data = super(PaymentForm, self).clean()
        amount = cleaned_data.get('amount')
        message = cleaned_data.get('message')
        if not amount or not message:
            raise forms.ValidationError('Please fill in both fields')


