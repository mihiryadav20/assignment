from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for viewsets
router = DefaultRouter()
router.register(r'issues', views.IssueViewSet, basename='issue')

# URL patterns
urlpatterns = [
    # Authentication endpoints
    path('auth/', include([
        # Email/password authentication for maintainers/admins
        path('login/', views.LoginView.as_view(), name='login'),
        path('user/', views.UserDetailView.as_view(), name='user-detail'),
        
        # Google OAuth endpoints
        path('url/', views.get_auth_url, name='auth-url'),
        path('complete/<backend>/', views.google_auth, name='google-auth-complete'),
    ])),
    
    # User info endpoint
    path('api/user/', views.get_user_info, name='user-info'),
    
    # Dedicated endpoint for creating issues with file attachments
    path('issues/create/', views.CreateIssueView.as_view(), name='create-issue'),
    
    # Endpoint for admins/maintainers to update issue status and severity
    path('issues/<uuid:issue_id>/update-status/', views.UpdateIssueStatusView.as_view(), name='update-issue-status'),
    
    # Endpoint for issue statistics by status and severity
    path('issues/stats/', views.IssueStatsView.as_view(), name='issue-stats'),
    
    # Include router URLs
    path('', include(router.urls)),
]
