from django.urls import path
from . import views
from .views import PostListView, CreatePostView, PostDetailView, UpdatePostView, PostDeleteView

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
    path('recruit/', views.recruit, name='circle-recruit'),
    path('job_listings/', views.jobs_listing, name='circle-jobs'),
    path('find_people/', views.find_people, name='circle-findPeople'),
    path('search_people/', views.search, name='search'),
]
