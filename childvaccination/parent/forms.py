from django import  forms
from .models import  Child_Details,Child_vaccine,Book_Appoinment,Vaccinations
from datetime import datetime,date

class ChildForm(forms.ModelForm):
    class Meta:
        model = Child_Details
        fields = ['child_name', 'child_age','child_address','child_dob','child_father_name','child_mother_name','child_ph']
        widgets = {
            'child_name': forms.TextInput(attrs={'class': 'form-control '}),
            'child_age': forms.TextInput(attrs={'class': 'form-control'}),
            'child_address': forms.Textarea(attrs={'class': 'form-control'}),
            'child_dob': forms.DateInput(attrs={'class': 'form-control'}),
            'child_father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'child_mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'child_ph': forms.TextInput(attrs={'class': 'form-control'}),

        }


class ChildVaccine_form(forms.ModelForm):
    class Meta:
        model=Child_vaccine
        fields=['vaccine_date']

        widgets = {
          
            'vaccine_date': forms.DateInput(attrs={'class': 'form-control','type':'date'}),


        }

class AppointmentForm(forms.Form):
    child = forms.ModelChoiceField(queryset=Child_Details.objects.all(), label="Select Child")

    vaccine = forms.ModelChoiceField(queryset=Vaccinations.objects.all(), label="Select Vaccine")
    appoinment_date = forms.DateField(widget=forms.SelectDateWidget)

    def __init__(self, *args, **kwargs):
        child_id = kwargs.pop('child_id', None)
        super().__init__(*args, **kwargs)
        if child_id:
            try:
                child = Child_Details.objects.get(id=child_id)
                self.fields['child'].initial = child
                self.child_dob = child.child_dob
                print(self.child_dob)
                current_date = datetime.now()
                cd=date.today()
                print(current_date)
                print(cd)

        # Calculating the difference in days between DOB and today
                days_difference = (cd - self.child_dob).days
                print(days_difference, '=======================')
                received_vaccines = Vaccinations.objects.filter(time_period__timeperiod_indays__lte=days_difference)
                print(received_vaccines)
                print(len(received_vaccines))
                self.fields['vaccine'].queryset = Vaccinations.objects.exclude(id__in=received_vaccines)
            except Child_Details.DoesNotExist:
                self.fields['vaccine'].queryset = Vaccinations.objects.all()
        else:
            self.fields['vaccine'].queryset = Child_vaccine.objects.all()

