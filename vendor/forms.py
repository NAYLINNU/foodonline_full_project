from django import forms
from .models import Vendor,OpeningHour
from accounts.validators import allow_image_only
class VendorForm(forms.ModelForm):
    #The reason I use 'FileField' is because I use a custom validator ,image field not working
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_image_only])
    
    

    class Meta:
        model = Vendor
        fields = ['vendor_name','vendor_license']
        
        
class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ['day', 'from_hour','to_hour','is_closed']