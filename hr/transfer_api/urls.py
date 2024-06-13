from django.urls import path
from hr.transfer_api import views

urlpatterns = [
    path("positions-create/", views.PositionCreateView.as_view(), name="position-create"),
    path("positions-update/<int:pk>/", views.PositionUpdateView.as_view(), name="position-update"),
    path("positions-delete/<int:pk>/", views.PositionDeleteView.as_view(), name="positions-delete"),
    path("nationality-create/", views.NationalityCreateView.as_view(), name="nationality-create"),
    path("nationality-update/<int:pk>/", views.NationalityUpdateView.as_view(), name="nationality-update"),
    path("nationality-delete/<int:pk>/", views.NationalityDeleteView.as_view(), name="nationality-delete"),
    path("job-create/", views.JobCreateView.as_view(), name="job-create"),
    path("job-update/<int:pk>/", views.JobUpdateView.as_view(), name="job-update"),
    path("job-delete/<int:pk>/", views.JobDeleteView.as_view(), name="job-delete"),
    path("form-create/", views.FormCreateView.as_view(), name="form-create-transfer-api"),
    path("form-update/<int:pk>/", views.FormUpdateView.as_view(), name="form-update-transfer-api"),
    path("category-create/", views.JobCategoryCreateView.as_view(), name="category-create-transfer-api"),
    path("category-update/<int:pk>/", views.JobCategoryUpdateView.as_view(), name="category-update-transfer-api"),
    path("category-delete/<int:pk>/", views.JobCategoryDeleteView.as_view(), name="category-delete-transfer-api"),
    path("vacant-status/<int:pk>/", views.VacantUpdateView.as_view(), name="vacant-status-update-transfer-api"),
    path("vacant-delete/<int:pk>/", views.VacantDeleteView.as_view(), name="vacant-delete-transfer-api"),
]
