from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    student_class = models.CharField(max_length=50)
    total_fee = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.student_class})"

class FeeSubmission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount_submitted = models.IntegerField()
    date = models.DateField(auto_now_add=True)
