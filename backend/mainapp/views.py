from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import JsonResponse
from django.middleware.csrf import get_token

from rest_framework import generics, permissions, status, viewsets, parsers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, parser_classes
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from social_django.utils import psa, load_strategy
from drf_social_oauth2.views import ConvertTokenView

from .models import Issue, UserProfile
from .serializers import UserSerializer, LoginSerializer, IssueSerializer
from .permissions import IsAdmin, IsMaintainer


class LoginView(APIView):
    """View for maintainer/admin login with email and password"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Get or create token
        token, created = Token.objects.get_or_create(user=user)
        
        # Return user data and token
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })


@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
@psa()
def google_auth(request, backend):
    """Endpoint for Google OAuth authentication for reporters"""
    # This is handled by python-social-auth
    if backend != 'google-oauth2':
        return Response(
            {'error': 'Only Google OAuth2 is supported'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # The actual authentication happens in the @psa() decorator
    # which creates or authenticates the user
    user = request.user
    
    # Check if user is authenticated
    if not user.is_authenticated:
        return Response(
            {'error': 'Authentication failed'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Get or create token
    token, created = Token.objects.get_or_create(user=user)
    
    # Return user data and token
    return Response({
        'token': token.key,
        'user': UserSerializer(user).data,
        'is_new_user': created
    })


class UserDetailView(generics.RetrieveAPIView):
    """View to retrieve user details"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_auth_url(request):
    """Get the Google OAuth2 authorization URL"""
    strategy = load_strategy(request)
    google_backend = strategy.backend_class('google-oauth2')
    redirect_uri = strategy.build_absolute_uri('/auth/complete/google-oauth2/')
    
    # Get the authorization URL
    auth_url, state = google_backend.auth_url(
        redirect_uri=redirect_uri,
        state=strategy.session_get('state', None)
    )
    
    # Return the URL and CSRF token
    return JsonResponse({
        'auth_url': auth_url,
        'csrf_token': get_token(request)
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_info(request):
    """Return current user info as JSON"""
    user = request.user
    return JsonResponse({
        'id': user.id,
        'email': user.email,
        'name': user.get_full_name() or user.username,
        'is_reporter': hasattr(user, 'profile') and user.profile.is_reporter(),
        'is_maintainer': hasattr(user, 'profile') and user.profile.is_maintainer(),
        'is_admin': hasattr(user, 'profile') and user.profile.is_admin()
    })


@method_decorator(csrf_exempt, name='dispatch')
class CreateIssueView(APIView):
    """Dedicated endpoint for creating issues with file attachments after OAuth"""
    permission_classes = [permissions.AllowAny]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    
    def post(self, request, *args, **kwargs):
        # Create a mutable copy of the data
        data = request.data.copy()
        
        # Validate required fields
        if 'title' not in data:
            return Response({'error': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)
        if 'description' not in data:
            return Response({'error': 'Description is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create serializer with data
        serializer = IssueSerializer(data=data)
        if serializer.is_valid():
            # Handle both authenticated and anonymous users
            if request.user.is_authenticated:
                issue = serializer.save(created_by=request.user)
            else:
                # Try to find or create a default anonymous user
                try:
                    anon_user = User.objects.get(username='anonymous')
                except User.DoesNotExist:
                    anon_user = User.objects.create_user(
                        username='anonymous',
                        email='anonymous@example.com',
                        password=None
                    )
                issue = serializer.save(created_by=anon_user)
            
            return Response(
                {
                    'message': 'Issue created successfully',
                    'issue': IssueSerializer(issue).data
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateIssueStatusView(APIView):
    """Endpoint for admins and maintainers to update issue status and severity"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, issue_id, *args, **kwargs):
        # This method handles POST requests
        return self._update_issue(request, issue_id)
    
    def patch(self, request, issue_id, *args, **kwargs):
        # This method handles PATCH requests
        return self._update_issue(request, issue_id)
    
    def _update_issue(self, request, issue_id):
        # Check if user is admin or maintainer
        user = request.user
        if not (hasattr(user, 'profile') and (user.profile.is_admin() or user.profile.is_maintainer())):
            return Response({'error': 'Only admins and maintainers can update issue status'}, status=status.HTTP_403_FORBIDDEN)
        try:
            issue = Issue.objects.get(pk=issue_id)
        except Issue.DoesNotExist:
            return Response({'error': 'Issue not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Only allow updating status and severity fields
        allowed_fields = ['status', 'severity']
        update_data = {}
        
        for field in allowed_fields:
            if field in request.data:
                update_data[field] = request.data[field]
        
        if not update_data:
            return Response({'error': 'No valid fields to update'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate the data
        serializer = IssueSerializer(issue, data=update_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Issue updated successfully',
                'issue': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class IssueViewSet(viewsets.ModelViewSet):
    """ViewSet for managing issues"""
    serializer_class = IssueSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    
    def get_permissions(self):
        """Return custom permissions based on action"""
        if self.action == 'create':
            # Anyone can create issues
            return [permissions.AllowAny()]
        elif self.action in ['list', 'retrieve']:
            # Reporters can view issues
            return [permissions.IsAuthenticated()]
        elif self.action == 'destroy':
            # Only admins can delete issues
            return [IsAdmin()]
        else:
            # Maintainers can update, etc.
            return [IsMaintainer()]
    
    def get_queryset(self):
        user = self.request.user
        
        # If user is a reporter, only show their issues
        if hasattr(user, 'profile') and user.profile.is_reporter():
            return Issue.objects.filter(created_by=user)
        
        # Maintainers and admins can see all issues
        return Issue.objects.all()
    
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(created_by=self.request.user)
        else:
            # Try to find or create a default anonymous user
            try:
                anon_user = User.objects.get(username='anonymous')
            except User.DoesNotExist:
                anon_user = User.objects.create_user(
                    username='anonymous',
                    email='anonymous@example.com',
                    password=None
                )
            serializer.save(created_by=anon_user)


class IssueStatsView(APIView):
    """View for retrieving issue statistics by status and severity"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        # Get the user's queryset based on their role
        user = request.user
        
        if hasattr(user, 'profile') and user.profile.is_reporter():
            # Reporters can only see stats for their own issues
            queryset = Issue.objects.filter(created_by=user)
        else:
            # Maintainers and admins can see stats for all issues
            queryset = Issue.objects.all()
        
        # Initialize dictionaries with all possible status and severity values set to 0
        status_stats = {
            Issue.STATUS_OPEN: 0,
            Issue.STATUS_TRIAGED: 0,
            Issue.STATUS_IN_PROGRESS: 0,
            Issue.STATUS_DONE: 0
        }
        
        severity_stats = {
            Issue.SEVERITY_LOW: 0,
            Issue.SEVERITY_MEDIUM: 0,
            Issue.SEVERITY_HIGH: 0,
            Issue.SEVERITY_CRITICAL: 0
        }
        
        # Get counts by status
        status_counts = queryset.values('status').annotate(count=Count('status'))
        for item in status_counts:
            status_stats[item['status']] = item['count']
        
        # Get counts by severity
        severity_counts = queryset.values('severity').annotate(count=Count('severity'))
        for item in severity_counts:
            severity_stats[item['severity']] = item['count']
        
        # Return the statistics
        return Response({
            'status_counts': status_stats,
            'severity_counts': severity_stats,
            'total_issues': queryset.count()
        })
