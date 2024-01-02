"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from obraBack.views import LoginView, Usuarios, Projects, UploadFotoProjetoView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/login/', LoginView.as_view(), name='login'),
    path('api/user_details/<int:user_id>/', LoginView.get_user_details, name='user-details'),

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/usuario/create', Usuarios.create_user, name='create_user'),
    path('api/usuario/update/', Usuarios.update_user, name='update_user'),
    path('api/usuario/delete/', Usuarios.delete_user, name='delete_user'),
    path('api/usuario/all/', Usuarios.get_users, name='get_users'),
    path('api/usuario/name/<int:user_id>/', Usuarios.get_name, name='get_name'),

    path('api/projects/', Projects.all_projects, name='all_projects'),
    path('api/projects/names/', Projects.all_projects_names, name='all_projects_names'),
    path('api/projects/<int:id>/', Projects.my_projects, name='my_projects'),
    path('api/project/<int:project_id>/', Projects.get_project_by_id, name='get_project_by_id'),

    path('api/uploadphoto/', UploadFotoProjetoView.upload_photo, name='upload_photo'),

]
