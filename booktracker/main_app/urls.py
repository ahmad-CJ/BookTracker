from django.urls import path
from . import views
from .views import BookList, BookDetail, BookCreate, BookUpdate, BookDelete
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('', views.home, name='home'),
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),

    path('books/', BookList.as_view(), name='book_list'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book_detail'),
    path('books/create/', BookCreate.as_view(), name='book_create'),
    path('books/<int:pk>/update/', BookUpdate.as_view(), name='book_update'),
    path('books/<int:pk>/delete/', BookDelete.as_view(), name='book_delete'),
    path('books/<int:book_id>/review/', views.add_review, name='add_review'),
    path('books/<int:book_id>/toggle-read/', views.toggle_read_status, name='toggle_read'),

]
