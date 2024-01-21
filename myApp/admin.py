from django.contrib import admin
from myApp.models import JobInfo,User,History
# Register your models here.

class JobManager(admin.ModelAdmin):
    list_display = ["id","title","address","type","educational","workExperience","workTag","salary","salaryMonth","companyTags","hrWork","hrName","pratice","companyTitle","companyAvatar","companyNature","companyStatus","companyPeople","detailUrl","companyUrl","dist"]
    list_display_links = ['title']
    list_filter = ['type']
    search_fields = ['title']
    list_editable = ["address","type","educational","workExperience","workTag","salary","salaryMonth",
                                 "companyTags","hrWork","hrName","pratice","companyTitle","companyAvatar","companyNature",
                                 "companyStatus","companyPeople","detailUrl","companyUrl","dist"]
    readonly_fields = ['id']
    list_per_page = 20
    date_hierarchy = "createTime"

class UserManager(admin.ModelAdmin):
    list_display = ['id','username','password','avatar','createTime','address','educational','work','workExpirence']
    list_display_links = ['username']
    search_fields = ['username']
    list_editable = ['password','avatar','address','educational','work','workExpirence']
    readonly_fields = ['username']
    list_per_page = 5
    date_hierarchy = "createTime"

class HistoryManager(admin.ModelAdmin):
    list_display = ['id','job','user','count']
    list_display_links = ['id']
    list_per_page = 5

admin.site.register(JobInfo, JobManager)
admin.site.register(User, UserManager)
admin.site.register(History, HistoryManager)

