from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.HomeView.as_view(), name='home'),
    # path('home/<int:pk>', views.CandidateView.as_view(), name='candidate'),
    path('home/<int:id>',views.CandidateView, name='candidate'),
    path('singup/', views.user_signup, name='signup'),
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('updatedata/<int:id>/', views.update_data, name='updatedata'),
    path('delete/<int:id>/', views.delete_post, name='deletepost'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
