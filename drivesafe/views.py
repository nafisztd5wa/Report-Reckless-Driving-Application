from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import ReportingForm, UploadedFiles, Submission
from django.conf import settings
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from .forms import LoginForm
nltk.download('punkt')
nltk.download('stopwords')

def home(request):
    HttpResponse("Hello, world! This is the home page.")
    login_url = reverse_lazy('account_login')
    return render(request, 'drivesafe/index.html', {'login_url': login_url})

def submissions_list(request):
    submissions = Submission.objects.all()
    return render(request, 'submissions.html', {'submissions': submissions})

@staff_member_required
def update_status(request, submission_id):
    if request.method == 'POST':
        submission = get_object_or_404(UploadedFiles, pk=submission_id)
        #submission = UploadedFiles.objects.get(pk=submission_id)
        new_status = request.POST.get('status')
        submission.status = new_status
        submission.save()
        messages.success(request, f"Status updated successfully for {submission.user.username}.")
        return redirect('drivesafe:submissions')
    else:
        return render(request, 'error_page.html', {'error_message': 'Invalid request method'})


@staff_member_required
def update_response(request, submission_id):
    if request.method == 'POST':
        submission = get_object_or_404(UploadedFiles, pk=submission_id)
        new_response = request.POST.get('admin_response')  # Get the new response from the form data
        submission.admin_response = new_response  # Update the admin_response field
        submission.last_updated = timezone.now()
        submission.update_seen = False
        submission.save()
        messages.error(request, 'The response has been added')
        messages.success(request, f"Response updated successfully for {submission.user.username}.")
        return redirect('drivesafe:submissions')  # Redirect to the submissions list page
    else:
        return render(request, 'error_page.html', {'error_message': 'Invalid request method'})


def index(request):
    if request.method == 'GET':
        return render(request, 'drivesafe/index.html')
    else:
        return HttpResponseNotAllowed(['GET'])


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                #messages.success(request, 'You have successfully logged in.')
                # Redirect to a success page or wherever you want
                if request.user.is_staff and not request.user.is_superuser:
                    return redirect('drivesafe:admin_home')
                else:
                    return redirect('drivesafe:regular_user_home')
            else:
                messages.error(request, 'Invalid email or password.')
                # Redirect back to the login page with an error message
                return render(request, 'drivesafe/index.html', {'form': form})
    else:
        form = LoginForm()
        #messages.error(request, 'Invalid email or password.')
    return render(request, 'drivesafe/index.html', {'form': form})

def login_redirect(request):
    #need to work on logic for site vs regular
    if request.user.is_authenticated:
        #return render(request, 'drivesafe/regular_user_home.html')
        if request.user.is_staff and not request.user.is_superuser:
            return redirect('drivesafe:admin_home')
        else:
            return redirect('drivesafe:regular_user_home')
    else:
        return redirect('account_login') #redirect to login page if user is not authenticated

@login_required
def regular_user(request):
    context = {
        'username': request.user.username,
        'full_name': request.user.get_full_name()
    }
    return render(request, 'drivesafe/regular_user_home.html', context)


@staff_member_required
def admin_home(request):
    context = {
        'username': request.user.username,
        'full_name': request.user.get_full_name()
    }
    return render(request, 'drivesafe/site_admin_home.html', context)
#keiufog


def report(request):
    context = {
        'username': request.user.username
    }
    if request.method == 'POST':
        form = ReportingForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            return redirect('drivesafe:form_submitted')  # Redirects to where we want to go when submitted
    else:
        form = ReportingForm()
    return render(request, 'drivesafe/reporting.html', {'form': form}) #redirects to where we want to go if submission is bad,
                                                    # so back to user page or back to the form page if it is different
def form_submitted(request):
    return render(request, 'drivesafe/form_submitted.html')

def anon_form_submitted(request):
    return render(request, 'drivesafe/anon_form_submitted.html')
@login_required
def view_submissions(request):
    if not (request.user.is_staff and not request.user.is_superuser):
        return HttpResponseForbidden("You do not have access to this page.")
    submissions = UploadedFiles.objects.all()
    for submission in submissions:
        if submission.status == 'New':
            submission.status = 'In Progress'
            submission.save()
    return render(request, 'drivesafe/submissions.html', {'submissions': submissions})

def view_user_submissions(request):
    user_submissions = UploadedFiles.objects.filter(user=request.user)
    new_updates = user_submissions.filter(update_seen=False)

    context = {
        'user_submissions': user_submissions,
        'new_updates': new_updates.exists(),
    }

    response = render(request, 'drivesafe/view_user_submissions.html', context)
    new_updates.update(update_seen=True)
    return response

def delete_submission(request, submission_id):
    submission = get_object_or_404(UploadedFiles, pk=submission_id)
    if submission.user == request.user:
        submission.delete()
        messages.success(request, "Submission has been successfully deleted")
    return redirect('drivesafe:user_submissions')

def anonymous_report(request):
    anonymous_user = User.objects.filter(username='anonymous').first()
    if request.method == 'POST':
        form = ReportingForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = anonymous_user  # Set user to the anonymous user
            uploaded_file.save()
            return redirect('drivesafe:anon_form_submitted')  # Redirect to a submission confirmation page
    else:
        form = ReportingForm()
    return render(request, 'drivesafe/reporting.html', {'form': form})
def common_words(request):
    submissions = UploadedFiles.objects.all()

    all_text = []
    for submission in submissions:
        all_text.append(submission.car_color)
        all_text.append(submission.car_model)
        all_text.append(submission.car_identifying_features)
        all_text.append(submission.driver_details)
        all_text.append(submission.additional_information)

    stop_words = set(stopwords.words('english'))
    words = word_tokenize(' '.join(all_text))
    words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]

    common_words = Counter(words).most_common(10)

    context = {
        'username': request.user.username,
        'full_name': request.user.get_full_name(),
        'common_words': common_words
    }
    return render(request, 'drivesafe/common_words.html', context)


def submissions_categories(request):
    in_progress_submissions = Submission.objects.filter(status='In Progress')
    completed_submissions = Submission.objects.filter(status='Completed')
    return render(request, 'submissions.html', {'in_progress_submissions': in_progress_submissions, 'completed_submissions': completed_submissions})
@staff_member_required
def update_status_and_response(request, submission_id):
    if request.method == 'POST':
        submission = get_object_or_404(UploadedFiles, pk=submission_id)
        new_status = request.POST.get('status')
        new_response = request.POST.get('admin_response')

        if request.POST.get('action') == 'update_both':
            submission.status = new_status
            submission.admin_response = new_response
            submission.update_seen = False
            submission.save()
            messages.success(request, f"Status and response updated successfully for {submission.user.username}.")
        else:
            if new_status:
                submission.status = new_status
                submission.update_seen = False
                submission.save()
                messages.success(request, f"Status updated successfully for {submission.user.username}.")
            if new_response:
                submission.admin_response = new_response
                submission.update_seen = False
                submission.save()
                messages.success(request, f"Response updated successfully for {submission.user.username}.")

        return redirect('drivesafe:submissions')
    else:
        return render(request, 'error_page.html', {'error_message': 'Invalid request method'})
