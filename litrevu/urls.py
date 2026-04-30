"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import authentication.views
import blog.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', authentication.views.LoginPageView.as_view(), name='login'),
    path('signup/', authentication.views.SignupPageView.as_view(), name='signup'),
    path('logout/', authentication.views.LogoutPageView.as_view(), name='logout'),
    path('ticket/create/', blog.views.CreateTicketView.as_view(), name='create_ticket'),
    path('ticket/update/<int:ticket_id>/', blog.views.UpdateTicketView.as_view(), name='update_ticket'),
    path('ticket/delete/<int:ticket_id>/', blog.views.DeleteTicketView.as_view(), name='delete_ticket'),
    path('review/create/<int:ticket_id>/', blog.views.CreateReviewView.as_view(), name='create_review'),
    path('ticket-and-review/create/', blog.views.CreateTicketAndReviewView.as_view(), name='create_ticket_and_review'),
    path('review/update/<int:review_id>/', blog.views.UpdateReviewView.as_view(), name='update_review'),
    path('review/delete/<int:review_id>/', blog.views.DeleteReviewView.as_view(), name='delete_review'),
    path('posts/', blog.views.PostsPageView.as_view(), name='posts'),
    path('subscriptions/', blog.views.SubscriptionsView.as_view(), name='subscriptions'),
    path('subscriptions/delete/<int:followed_user_id>/', blog.views.DeleteFollowView.as_view(), name='delete_follow'),
    path('feed/', blog.views.FeedPageView.as_view(), name='feed'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
