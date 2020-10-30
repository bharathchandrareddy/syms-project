from django import forms
from.models import Profile

class ProfileModel(forms.ModelForm):   #this class is created to edit the user details in form and then update the details to database
    class Meta:
        model = Profile   #represents on which model we need to work on
        fields = {
            'first_name','last_name','bio','avatar','gender','dob'

        }
