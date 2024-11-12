from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here
def FacultyHomePage(request):
    return render(request, 'facultyapp/FacultyHomePage.html')

from .forms import AddCourseForm, MarksForm


def add_course(request):
    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facultyapp:FacultyHomePage')
    else:
        form = AddCourseForm()
    return render(request, 'facultyapp/AddCourse.html', {'form': form})


from django.shortcuts import render
from .models import AddCourse
from adminapp.models import StudentList


def student_list(request):
    course = request.GET.get('course')
    section = request.GET.get('section')

    # Get all courses, and filter based on 'course' and 'section' if provided
    student_courses = AddCourse.objects.all()
    if course:
        student_courses = student_courses.filter(course=course)
    if section:
        student_courses = student_courses.filter(section=section)

    # Assuming 'AddCourse' has a ForeignKey to 'StudentList'
    students = StudentList.objects.filter(id__in=student_courses.values('student_id'))

    # Assuming AddCourse.COURSE_CHOICES and AddCourse.SECTION_CHOICES exist
    course_choices = AddCourse.COURSE_CHOICES
    section_choices = AddCourse.SECTION_CHOICES

    context = {
        'students': students,
        'course_choices': course_choices,
        'section_choices': section_choices,
        'selected_course': course,
        'selected_section': section,
    }

    return render(request, 'facultyapp/student_list.html', context)


def post_marks(request):
    if request.method == "POST":
        form = MarksForm(request.POST)
        if form.is_valid():
            marks_instance = form.save(commit=False)
            marks_instance.save()

            # Retrieve the User email based on the student in the form
            student = marks_instance.student
            student_user = student.user
            user_email = student_user.email
            subject = 'Marks Entered'
            message = f'Hello, {student_user.first_name}  marks for {marks_instance.course} have been entered. Marks: {marks_instance.marks}'
            from_email = 'sravanishiva192@gmail.com'
            recipient_list = [user_email]
            send_mail(subject, message, from_email, recipient_list)

            return render(request, 'facultyapp/post_marks.html')
    else:
        form = MarksForm()
    return render(request, 'facultyapp/post_marks.html', {'form': form})
