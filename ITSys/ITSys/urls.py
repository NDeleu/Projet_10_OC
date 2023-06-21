"""
URL configuration for ITSys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers

from rest_framework_simplejwt.views import TokenRefreshView
from authentication.views import EmailTokenObtainPairView, RegisterView
from projectsManager.views import ProjectViewset, UserViewset, \
    IssueViewset, CommentViewset

router = routers.SimpleRouter()
router.register(r'projects/?', ProjectViewset, basename='projects')
user_router = routers.NestedSimpleRouter(router, r'projects/?', lookup='projects', trailing_slash=False)
user_router.register(r'users/?', UserViewset, basename='users', )
issue_router = routers.NestedSimpleRouter(router, r'projects/?', lookup='projects', trailing_slash=False)
issue_router.register(r'issues/?', IssueViewset, basename='issues', )
comment_router = routers.NestedSimpleRouter(issue_router, r'issues/?', lookup='issues', trailing_slash=False)
comment_router.register(r'comments/?', CommentViewset, basename='comments', )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/',
         EmailTokenObtainPairView.as_view(), name='obtain_tokens'),
    path('api/token/refresh/',
         TokenRefreshView.as_view(), name='refresh_token'),
    path('api/', include(router.urls)),
    path('api/', include(user_router.urls)),
    path('api/', include(issue_router.urls)),
    path('api/', include(comment_router.urls)),
]


