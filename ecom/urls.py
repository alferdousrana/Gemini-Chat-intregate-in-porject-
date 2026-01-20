from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_ai(request):
    return redirect('/ai/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ai/', include('api.urls')),
    path('', redirect_to_ai),
]