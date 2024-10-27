from django.contrib import admin
from courses.models import Course,Learning,Tag,Prerequisite,Video,UserCourse,Payment,QuesModel
# Register your models here.
#SET CONFIGRATION OF MODELS
class TagAdmin(admin.TabularInline):
    model=Tag

class LearningAdmin(admin.TabularInline):
    model=Learning

class PrerequisiteAdmin(admin.TabularInline):
    model=Prerequisite

class VideoAdmin(admin.TabularInline):
    model=Video

class QuesModelAdmin(admin.TabularInline):
    model=QuesModel

class CourseAdmin(admin.ModelAdmin):
    inlines=[TagAdmin,LearningAdmin,PrerequisiteAdmin,VideoAdmin,QuesModelAdmin]


admin.site.register(Course,CourseAdmin)
admin.site.register(Video)

'''admin.site.register(Tag)
admin.site.register(Prerequisite)
admin.site.register(Learning)'''
admin.site.register(Payment)
admin.site.register(UserCourse)
admin.site.register(QuesModel)
