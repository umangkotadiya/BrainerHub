from django.urls import path
from .views import FileUploadView, EmployeeListView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='upload'),
    path('employee_list/', EmployeeListView.as_view(), name='upload'),
]
