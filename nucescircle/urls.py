from django.urls import path, include
from . import views
from rest_framework import routers
from .api import JobViewSet
from .views import PostListView, CreatePostView, PostDetailView, \
    UpdatePostView, PostDeleteView, JobListView, JobDeleteView, CreateJobView, JobDetailView

router = routers.DefaultRouter()
router.register('api/jobs', JobViewSet, 'jobs')

urlpatterns = [
    path('', PostListView.as_view(), name='circle-home'),  # home page
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', UpdatePostView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', CreatePostView.as_view(), name='post-create'),
    # path('create/', views.post_create_view, name='create-post'),
    path('about/', views.about, name='circle-about'),
    path('my_circle/', views.my_circle, name='my-circle'),
    path('profile_edit/', views.profile_editing, name='circle-editProfile'),
    path('recruit/', JobListView.as_view(), name='circle-recruit'),
    path('recruit/<int:pk>/delete/', JobDeleteView.as_view(), name='job-delete'),
    path('recruit/<int:pk>/detail/', JobDetailView.as_view(), name='job-detail'),
    path('recruit/post/new/', CreateJobView.as_view(), name='submit-recruit'),
    path('job_listings/', views.jobs_listing, name='circle-jobs'),
    path('find_people/', views.find_people, name='circle-find-people'),
    path('search_people/', views.search, name='search'),
    path('find_people/advanced_search/', views.advanced_search, name='advanced-search'),
    path('find_people/advanced_search/results', views.render_ad_result_page, name='advanced-search-result'),
    path('recruit/<int:jid>/apply/', views.add_job_applicant, name='add-job-applicant'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    # path('load_posts/', views.get_posts, name='inf-scroll-posts'),
    path('next_posts/<int:count>/', views.loadfeed, name='nxt-posts'),
] + router.urls
