from django.db import models
from courses.models import Course
class QuesModel(models.Model):
    course=models.ForeignKey(Course,null=False,on_delete=models.CASCADE)
    question_no=models.IntegerField(null=True)
    question=models.CharField(max_length=300,null=True)
    op1=models.CharField(max_length=200,null=True)
    op2=models.CharField(max_length=200,null=True)
    op3=models.CharField(max_length=200,null=True)
    op4=models.CharField(max_length=200,null=True)
    ans=models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.course.name