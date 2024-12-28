from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, JobApplicationDetailView, UserRegistrationView, JobListingListCreateView, JobListingDetailView, JobApplicationListCreateView, EmployerDashboardView, JobSeekerDashboardView, JobListingViewSet, JobApplicationDetailView, loginView, logoutView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('jobs/', JobListingListCreateView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', JobListingDetailView.as_view(), name='job-detail'),
    path('jobs/<int:job_id>/applications/', JobApplicationListCreateView.as_view(), name='job-application-list'),
    path('dashboard/employer/', EmployerDashboardView.as_view(), name='employer-dashboard'),
    path('dashboard/seeker/', JobSeekerDashboardView.as_view(), name='job-seeker-dashboard'),
    path('jobs/', JobListingViewSet.as_view({'get': 'list', 'post': 'create'}), name='job-listings'),
    path('jobs/<int:pk>/', JobListingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='job-detail'),
    path('jobs/<int:job_id>/applications/', JobApplicationListCreateView.as_view(), name='job-application-list'),
    path('jobs/<int:job_id>/applications/<int:pk>/', JobApplicationDetailView.as_view(), name='job-application-detail'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('custom-login/', CustomLoginView.as_view(), name='user-login'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
