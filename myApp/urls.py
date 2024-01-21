from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('registry/', views.registry, name='registry'),
    path('logOut/', views.logOut, name='logOut'),
    path('selfInfo/', views.selfInfo, name='selfInfo'),
    path('changePassword/', views.changePassword, name='changePassword'),
    path('tableData/', views.tableData, name='tableData'),
    path('historyTableData/', views.historyTableData, name='historyTableData'),
    re_path(r'historyTableData/(.*)', views.historyTableData, name='historyTableData'),
    path('addHistory/<int:jobId>', views.addHistory, name='addHistory'),
    path('removeHistory/<int:hisId>', views.removeHistory, name='removeHistory'),
    path('salary/', views.salary, name='salary'),
    path('company/', views.company, name='company'),
    path('companyTags/', views.companyTags, name='companyTags'),
    path('educational/', views.educational, name='educational'),
    path('companyStatus/', views.companyStatus, name='companyStatus'),
    path('yuce/', views.yuce, name='yuce')
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
