from django.contrib import admin
from django.urls import path, include
from core import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
     path('accounts/login/', 
         auth_views.LoginView.as_view(
             template_name='core/login.html'  # Explicit path to your template
         ), 
         name='login'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('', include('core.urls')),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('farm/create/', views.create_farm, name='create_farm'),
    path('product/add/', views.add_product, name='add_product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
