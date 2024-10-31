from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from parent.models import Child_Details,Vaccinations,Child_vaccine,Book_Appoinment,appoinment_table
from vaccination.models import Userdetail
from django.contrib.auth.models import User
from datetime import date, timedelta,datetime
from .forms import ChildForm,ChildVaccine_form,AppointmentForm
from datetime import datetime
# Create your views here.

@login_required
def add_info(request,id):
    parent=Userdetail.objects.get(user_id=id)
    if request.method == 'POST':
        # Collecting form data
        ch_name = request.POST['chn']
        ch_fname = request.POST['chf']
        ch_mname = request.POST['chm']
        ch_dob = request.POST['dob']
        ch_age = request.POST['age']
        ch_address = request.POST['ad']
        ch_cn = request.POST['cn']
        parent=parent
        
        

        # Parsing the date of birth (assuming it's in 'YYYY-MM-DD' format)
        try:
            ch_dob = datetime.strptime(ch_dob, '%Y-%m-%d')
        except ValueError:
            # Handle invalid date format here
            return render(request, 'add_childinfo.html', {'error': 'Invalid date format. Please use YYYY-MM-DD.'})

        # Saving the child information in the database
        ch_info = Child_Details.objects.create(
            child_name=ch_name,
            child_father_name=ch_fname,
            child_mother_name=ch_mname,
            child_dob=ch_dob,
            child_age=ch_age,
            child_address=ch_address,
            child_ph=ch_cn,
            parent=parent
        )

        # Current date
        current_date = datetime.now()

        # Calculating the difference in days between DOB and today
        days_difference = (current_date - ch_dob).days
        print(days_difference, '=======================')

        # Filtering vaccinations based on time period
        vaccines = Vaccinations.objects.filter(time_period__timeperiod_indays__lte=days_difference)
        print(len(vaccines))

        for vaccine in vaccines:
            # Calculate expected date for the vaccine
            days_to_add = int(vaccine.time_period.timeperiod_indays)
            expected_date = ch_dob + timedelta(days=days_to_add)

            # Create a Child_vaccine entry
            Child_vaccine.objects.create(child=ch_info, vaccine=vaccine, expected_date=expected_date)

        return redirect('parent:view_details', id=parent.id)

    return render(request, 'add_childinfo.html')
@login_required
def view_details(request,id):
    parent=Userdetail.objects.get(user_id=id)
    details = Child_Details.objects.filter(parent=parent)

    # Dictionary to store child details and their vaccines
    #
    child_vaccine_data = []
    #
    # # Loop through each child and get their vaccines
    # for detail in details:
    #     child_vaccines = Child_vaccine.objects.filter(child=detail)  # Fetch vaccines for each child
    #     child_vaccine_data.append({
    #         'child': detail,
    #         'vaccines': child_vaccines,  # List of vaccine records
    #     })
    #
    # context = {
    #     'child_vaccine_data': child_vaccine_data
    # }
    return render(request, 'view_detail.html', {'detail':details})


def my_profile(request,id):
    u=User.objects.get(id=id)
    # profile=Userdetail.objects.get(id=id)

    return render(request,'my_profile.html',{'profile':u})

def edit_profile(request,id):
    details=User.objects.get(id=id)
    return render(request,'edit_profile.html',{'details':details})


def editchild_details(request, id):
    # Fetch the existing child details using get_object_or_404 for better error handling
    ch_detail = get_object_or_404(Child_Details, id=id)
    user_id=request.user.id

    if request.method == "POST":
        # Bind the form with POST data and the existing instance (ch_detail)
        form = ChildForm(request.POST, instance=ch_detail)

        if form.is_valid():
            # Save the updated instance
            form.save()
            return redirect('parent:view_details',id=user_id)  # Redirect after successful save
    else:
        # Initialize the form with the existing instance for GET requests
        form = ChildForm(instance=ch_detail)

    # Render the template with the form
    return render(request, 'editchild_details.html', {'form': form, 'ch_detail': ch_detail})


def delete_details(requset,id):
    user_id=requset.user.id
    print(user_id,"------------------")
    ch_detail=Child_Details.objects.get(id=id)
    ch_detail.delete()
    return view_details(requset,id=user_id)

def vaccine_details(request, id):
    # Get the child details based on the provided child ID
    detail = get_object_or_404(Child_Details, id=id)
    user_id=request.user.id
    # Fetch all vaccines associated with the child
    child_vaccine = Child_vaccine.objects.filter(child=detail)

    # Get the specific vaccine record to update based on the vaccine ID
    # child_vaccine_record = get_object_or_404(Child_vaccine, id=vid)

    if request.method == "POST":
        # Get the vaccine date from the form submission
        vaccine_date = request.POST.get('add_date')
        print(vaccine_date,'==================')

        if vaccine_date:
       
            return redirect('parent:view_details',id=user_id)  # Redirect to child's vaccine list

    # Context to pass to the template
    context = {
        "child_vaccine": child_vaccine,  # List of all vaccines for the child
        "detail": detail,                # Child details
        # "child_vaccine_record": child_vaccine_record  # The specific vaccine record to update
    }

    # Render the template with the context data
    return render(request, 'vaccinedetails.html', context)



def add_vaccine_date(request, id):
    
    # Get the specific Child_vaccine record based on the ID
    child_vaccine_record = get_object_or_404(Child_vaccine, id=id)
    user_id=request.user.id
    if request.method == "POST":
        # Get the vaccine date from the form submission
        vaccine_date = request.POST.get('add_date')

        if vaccine_date:
            # Update the vaccine record with the new date
            child_vaccine_record.vaccine_date = vaccine_date
            child_vaccine_record.save()

            # Redirect after saving (you can customize the target URL/page)
            return redirect('parent:view_details',id=user_id) # Change to your desired page
        else:
            # Handle missing date case (optional)
            return redirect('parent:view_details',id=user_id)
           

    # Render a form or modal that lets the user input the vaccine date
    context = {
        'child_vaccine_record': child_vaccine_record,  # Pass the vaccine record to the template
    }
    
    # Render a template (e.g., 'add_vaccine_date.html') that has a form for inputting the date
    return render(request, 'vaccinedetails.html', context)



def book_appoinment(request, child_id=None):
    if request.method == 'POST':
        form = AppointmentForm(request.POST, child_id=child_id)
        if form.is_valid():
            child = form.cleaned_data['child']
            vaccine = form.cleaned_data['vaccine']
            appoinment_date = form.cleaned_data['appoinment_date']
            user=request.user
            print(user)

            # Save the appointment
            Book_Appoinment.objects.create(child=child, vaccine=vaccine, appoinment_date=appoinment_date)
            appoinment_table.objects.create(child=child, vaccine=vaccine, appoinment_date=appoinment_date,user=user)
            return JsonResponse({
                'message': f"Appointment for {vaccine} on {appoinment_date} has been booked for {child}."
            })
        else:
            # Return form errors as JSON
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = AppointmentForm(child_id=child_id)
    
    # ch_detail = get_object_or_404(Child_Details, id=child_id)
    # child_vaccine = Child_vaccine.objects.filter(child=ch_detail)


    return render(request, 'book_appoinment.html', {'form': form,'child_id': child_id})


@login_required
def appoinmentdetail(request):
    user=request.user
    print(user)
    appoinment_details=appoinment_table.objects.filter(user=user)
    print(appoinment_details)
    return render(request,'appoinmentdetail.html',{'appoinment':appoinment_details})

   

