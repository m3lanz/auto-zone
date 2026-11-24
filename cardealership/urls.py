from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(),  name='main'),
    path('modelid/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', register_user_view, name='register'),
    path('profile/<str:username>', profile_user_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('profile/change-password/', edit_password_user, name='edit_password'),
    path('listing-creation/', create_listing_view, name='create_listing'),
    path('modelid/<int:pk>/delete/', DeleteListingView.as_view(), name='delete_listing'),
    path('modelid/<int:pk>/edit/', edit_listing_view, name='edit_listing'),
    path('comment-create/<int:pk>/', CreateCommentView.as_view(), name='post_comment'),
    path('comment-delete/<int:pk>/', DeleteCommentView.as_view(), name='delete_comment'),
    path('comment-update/<int:pk>/', UpdateCommentView.as_view(), name='update_comment'),
    path('favorites/', favorite_listing_view, name='favorite_page'),
    path('favorites/action/<int:pk>/', add_to_favorites, name='favorite_toggle')
]