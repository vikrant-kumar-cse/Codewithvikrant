from django.shortcuts import render,redirect
from courses.models import Course, Video,QuesModel
# Create your views here.S
from django.shortcuts import HttpResponse

def home(request):
    courses=Course.objects.all()
    #return HttpResponse("<h1>Welcome To Code With vikrant site</h1>")
    return render(request,"courses/home.html", context={"courses": courses})


def coursepage(request, slug):
    coursee=Course.objects.get(slug = slug)
    serial_number=request.GET.get('lecture')
    print(serial_number,coursee)
    if serial_number is None:
        serial_number=1
    video = Video.objects.get(serial_number = serial_number , course = coursee)
    if((request.user.is_authenticated is False)and(video.is_preview is False)):
        return redirect("login")

    context={
        "course": coursee,
        "video": video
    }
    return render(request,"courses/course_page.html",context=context)




'''
FROM HERE LOGIN,LOGOUT AND SIGNUP PADGE IS START
'''
#from django.contrib.auth.forms import UserCreationForm
from courses.forms import RegistrationForm

def signup(request):
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, "courses/signup.html", {'form': form})

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # This will save the user and hash the password automatically
            # Create the Profile object after saving the User
            profile_obj = Profile.objects.create(user=user)
            profile_obj.save()
            return redirect('login')
        
        # If the form is not valid, render it again with error messages
        return render(request, "courses/signup.html", {'form': form})

    return render(request, "courses/signup.html", {'form': form})

from django.contrib.auth.forms import AuthenticationForm
from courses.forms import LoginForm
def login(request):
    if(request.method=="GET"):
      form1=LoginForm()      
      return render(request,"courses/login.html",{'form1':form1})
    if(request.method=="POST"):
        form1=LoginForm(request= request ,data=request.POST)
        if(form1.is_valid()):
            print("Hi")
            return redirect('home')
        return render(request,"courses/login.html",{'form1':form1})
    
from django.contrib.auth import logout

def signout(request):
    logout(request)
    return redirect('home')

from django.contrib.auth import get_user_model
User=get_user_model()
from django.contrib import messages
from .helpers import send_forget_password_mail
from django.core.mail import send_mail
from .models import Profile
import uuid
def ForgetPassword(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            
            if not User.objects.filter(email=email).exists():
                messages.error(request, 'No user found with this Email.')
                return redirect('/courses/forget-password/')
            
            user_obj = User.objects.get(email=email)
            
            # Check if a Profile exists for the user
            profile_obj, created = Profile.objects.get_or_create(user=user_obj)
            
            # Generate a token and save it to the profile
            token = str(uuid.uuid4())
            profile_obj.forget_password_token = token
            profile_obj.save()
            
            # Send the reset password email
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'An email has been sent.')
            return redirect('/forget-password/')
                
    except Exception as e:
        print(e)
        messages.error(request, 'Something went wrong. Please try again.')
    
    return render(request, "courses/forget-password.html")







def ChangePassword(request, token):
    context = {}

    try:
        # Check if the profile object with the given token exists
        profile_obj = Profile.objects.filter(forget_password_token=token).first()

        # If no profile is found, handle the case
        if profile_obj is None:
            messages.error(request, 'Invalid or expired token.')
            return redirect('forgot-password')  # Redirect to a relevant page

        # If profile exists, proceed
        context = {'user_id': profile_obj.user.id}
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            
            # Check if user_id is present and is a valid number
            if not user_id or not user_id.isdigit():
                messages.error(request, 'Invalid user ID.')
                return redirect(f'/change-password/{token}/')

            # Convert user_id to an integer
            user_id = int(user_id)
            
            # Check if new_password and confirm_password match
            if new_password != confirm_password:
                messages.error(request, 'Both passwords should be equal.')
                return redirect(f'/change-password/{token}/')
            
            # Fetch the user object and change the password
            try:
                user_obj = User.objects.get(id=user_id)
                user_obj.set_password(new_password)
                user_obj.save()
                messages.success(request, 'Password has been changed successfully. Please log in with your new password.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
                return redirect(f'/change-password/{token}/')
        
    except Exception as e:
        print(e)
        messages.error(request, 'Something went wrong. Please try again.')

    return render(request, "courses/change-password.html", context)








































def checkout(request,slug):
    course=Course.objects.get(slug = slug)
    if not request.user.is_authenticated:
        return redirect("login")
    context={
        "course":course
    }
    return render(request,"courses/check_out.html",context=context)

    
'''
def Testpage(request,slug):
    if request.method=='POST':
        course=Course.objects.get(slug=slug)
        question=QuesModel.objects.filter(course=course)
        score=0
        wrong=0
        correct=0
        total=0
        for q in question:
            total+=1
            print(request.POST.get(q.question))
            print(q.ans)
            print()
            if q.ans==(request.POST.get(q.question)):
                score+=10
                correct+=1
            else:
                wrong+=1
        percent=score/(total*10)*100
        context={
            'score':score,
            'time':request.POST.get('timer'),
            'correct':correct,
            'wrong':wrong,
            'total':total,
            'percent':percent,
        }
        return render(request,"courses/result.html",context)
    
    else:
        question=QuesModel.objects.all()
        course=Course.objects.get(slug=slug)
        #test = QuesModel.objects.get(course = course)
        context={
            'question':question,
            "course":course,
            #"test":test
        }
        return render(request,"courses/Testpage.html",context)

'''
from django.shortcuts import render
from courses.models import TestResult
from courses.models import Course, QuesModel
from courses.models import UserCourse
from django.contrib import messages 

from django.shortcuts import render, get_object_or_404

def Testpage(request, slug):
    # Get the course based on the slug
    course = get_object_or_404(Course, slug=slug)
    user = request.user

    # Check if the user is enrolled in the course
    is_enrolled = UserCourse.objects.filter(user=user, course=course).exists()

    # If the user is not enrolled, redirect them to the dashboard
    if not is_enrolled:
        messages.warning(request, "Please enroll in the course to take the test.")
        return redirect('home')  # Redirect to a course list or another appropriate page

    # Handle the POST request for submitting the test
    if request.method == 'POST':
        questions = QuesModel.objects.filter(course=course)
        score = 0
        wrong = 0
        correct = 0
        total = 0

        # Calculate the score based on submitted answers
        for q in questions:
            total += 1
            if q.ans == request.POST.get(q.question):
                score += 10  # Assuming each question carries 10 points
                correct += 1
            else:
                wrong += 1

        # Calculate the percentage
        percent = (score / (total * 10)) * 100
        time_taken = request.POST.get('timer')

        # Save the test result in the database
        TestResult.objects.create(
            user=user,
            course=course,
            score=score,
            correct_answers=correct,
            wrong_answers=wrong,
            total_questions=total,
            percentage=percent,
            time_taken=int(time_taken)
        )

        # Pass the result data to the context for rendering the result page
        context = {
            'score': score,
            'time': time_taken,
            'correct': correct,
            'wrong': wrong,
            'total': total,
            'percent': percent,
        }
        return render(request, "courses/result.html", context)

    # Handle the GET request to display the test page
    else:
        questions = QuesModel.objects.filter(course=course)
        context = {
            'questions': questions,
            'course': course,
        }
        return render(request, "courses/Testpage.html", context)










from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from courses.forms import EnrollmentForm  # Correct the import to EnrollmentForm

@login_required
def enroll_course(request, slug):
    # Get the course based on the slug
    course = Course.objects.get(slug=slug)
    user = request.user

    # Check if the user is already enrolled in the course
    is_enrolled = UserCourse.objects.filter(user=user, course=course).exists()

    # If the user is already enrolled, redirect them to the dashboard or show a message
    if is_enrolled:
        return redirect('dashboard')  # Redirect to the user dashboard if already enrolled

    # If not enrolled, proceed with form processing
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.user = user  # Assign the logged-in user
            enrollment.course = course  # Assign the course from the slug
            enrollment.save()
            return redirect('dashboard')  # Redirect to the user dashboard
    else:
        form = EnrollmentForm()

    # Render the form for enrollment if not already enrolled
    context = {
        'form': form,
        'course': course,
        'is_enrolled': is_enrolled,
    }

    return render(request, 'courses/check_out.html', context)


from django.shortcuts import render

@login_required
def enrollment_success(request):
    return render(request, 'courses/enrollment_success.html')



'''
@login_required
def dashboard(request):
    #course = Course.objects.get(slug=slug)
    user = request.user
    enrollments = UserCourse.objects.filter(user=user)
    
    
    context = {
        'enrollments': enrollments,
    }
    
    return render(request, 'courses/dashboard.html', context)

'''

from .models import TestResult
def dashboard(request):
    user = request.user
    enrollments = UserCourse.objects.filter(user=user)
    test_results = TestResult.objects.filter(user=user).order_by('-date_taken')

    context = {
        'enrollments': enrollments,
        'test_results': test_results,  # Add test results to context
    }

    return render(request, 'courses/dashboard.html', context)



def user_enrollments_view(request, user_id):
    user = User.objects.get(id=user_id)
    enrolled_courses = user.enrollment_set.all()

    return render(request, 'enrollment/user_enrollments.html', {
        'user': user,
        'enrolled_courses': enrolled_courses
    })