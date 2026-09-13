from django.urls import path
from .views.auth_view import login_method, register_method, logout_method
from .views.main_view import index_method, add_post_method, profile_method, full_article_method, edit_post_method, delete_post_method, profile_method, about_method, privacy_method, terms_method, edit_profile
from django.conf import settings             
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



urlpatterns = [
    path("", index_method, name="index"),
    path("login/", login_method, name="login"),
    path("register/", register_method, name="register"),
    path("logout/", logout_method, name="logout"),
    path("add-post/", add_post_method, name="add_post"),
    path("profile/", profile_method, name="profile"),
    path("article/<int:id>/", full_article_method, name="full_article"),
    path("edit-post/<int:id>/", edit_post_method, name="edit_post"),
    path("delete-post/<int:id>/", delete_post_method, name="delete_post"),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path("profile/<str:username>/", profile_method, name="profile"),
    path("about/", about_method, name="about"),
    path("privacy/", privacy_method, name="privacy"),
    path("terms/", terms_method, name="terms"),
    
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='auth/password_reset.html',
             html_email_template_name='emails/password_reset_email.html',
             subject_template_name='emails/password_reset_subject.txt'
         ), 
         name='password_reset'),
         
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), 
         name='password_reset_done'),
         
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), 
         name='password_reset_confirm'),
         
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), 
         name='password_reset_complete'),
    
    
]


# to help serve media files in local development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)