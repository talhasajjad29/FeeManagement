from django.shortcuts import render, redirect
from .models import Student, FeeSubmission
from django.db.models import Sum


from django.shortcuts import render
from .models import Student, FeeSubmission

def home(request):
    search_query = request.GET.get('search', None)
    
    students = Student.objects.all()

    if search_query:
        students = Student.objects.filter(name__icontains=search_query)

    else:
        students = Student.objects.all()

    data = []
    for student in students:
        submissions = FeeSubmission.objects.filter(student=student)
        total_submitted = sum(sub.amount_submitted for sub in submissions)
        pending_fee = student.total_fee - total_submitted
        unpaid_fee = 0 if total_submitted > 0 else student.total_fee

        data.append({
            'student': student,
            'submitted': total_submitted,
            'pending': pending_fee,
            'unpaid': unpaid_fee
        })

    return render(request, 'home.html', {'data': data})


# def add_student(request):
#     if request.method == "POST":
#         name = request.POST['name']
#         student_class = request.POST['student_class']
#         total_fee = request.POST['total_fee']
#         Student.objects.create(name=name, student_class=student_class, total_fee=total_fee)
#         #return redirect('/')
#     return render(request, 'add_student.html')
from django.shortcuts import render, redirect
from .forms import StudentForm

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})

def add_fee(request):
    if request.method == "POST":
        student_id = request.POST['student_id']
        amount = request.POST['amount_submitted']
        student = Student.objects.get(id=student_id)
        FeeSubmission.objects.create(student=student, amount_submitted=amount)
        return redirect('/')
    students = Student.objects.all()
    return render(request, 'add_fee.html', {'students': students})

def generate_slip(request, student_id):
    student = Student.objects.get(id=student_id)
    total_submitted = FeeSubmission.objects.filter(student=student).aggregate(Sum('amount_submitted'))['amount_submitted__sum'] or 0
    pending = student.total_fee - total_submitted
    return render(request, 'slip.html', {
        'student': student,
        'submitted': total_submitted,
        'pending': pending,
    })
