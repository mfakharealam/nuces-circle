"""django_nuces URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('view_profile/current-user-id=<int:uid>/', user_views.view_profile, name='view-profile'),
    # education
    path('view_profile/edu_add/', user_views.add_education_info, name='add-edu'),
    path('view_profile/edu_add/submit', user_views.submit_education_info, name='submit-edu'),
    path('view_profile/edu_edit/<int:edu_info_id>/', user_views.edit_education_info, name='edit-edu'),
    path('view_profile/edu_edit/<int:edu_info_id>/update', user_views.update_education_info, name='update-edu'),
    # experience
    path('view_profile/exp_add/', user_views.add_exp_info, name='add-exp'),
    path('view_profile/exp_add/submit', user_views.submit_exp_info, name='submit-exp'),
    path('view_profile/exp_edit/<int:exp_info_id>/', user_views.edit_exp_info, name='edit-exp'),
    path('view_profile/exp_edit/<int:exp_info_id>/update', user_views.update_exp_info, name='update-exp'),
    # skill
    path('view_profile/add_skill/', user_views.add_skill_info, name='add-skill'),
    path('view_profile/add_skill/submit', user_views.submit_skill_info, name='submit-skill'),
    path('view_profile/skill_edit/<int:skill_id>/', user_views.edit_skill_info, name='edit-skill'),
    path('view_profile/skill_edit/<int:skill_id>/update', user_views.update_skill_info, name='update-skill'),
    path('view_profile/skill_edit/<int:skill_id>/delete', user_views.delete_skill_info, name='delete-skill'),
    # interests
    path('view_profile/int_edit/', user_views.edit_interest_info, name='edit-int'),
    path('view_profile/int_edit/update', user_views.update_interest_info, name='update-int'),
    # auth
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='circle-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='circle-logout'),
    # connect user
    path('connect-request/send/<int:uid>/', user_views.send_connect_request, name='send-connect-request'),
    path('connect-request/cancel/<int:uid>/', user_views.cancel_connect_request, name='cancel-connect-request'),
    path('connect-request/accept/<int:uid>/', user_views.accept_connect_request, name='accept-connect-request'),
    path('connect-request/delete/<int:uid>/', user_views.delete_connect_request, name='delete-connect-request'),

    path('', include('nucescircle.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
