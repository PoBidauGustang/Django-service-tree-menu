from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("menu/", include("menu_app.urls")),
]

handler404 = "menu_app.views.page_not_found"
