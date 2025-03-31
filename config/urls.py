"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    #-- URL for admin --
    path("admin/", admin.site.urls),
    #-- URL for Course & Lesson models --
    path("", include("materials.urls", namespace="materials")),
    #-- URL for User models --
    path("users/", include("users.urls", namespace="users")),
]
