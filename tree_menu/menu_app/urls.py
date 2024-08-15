from django.urls import path

from menu_app.views import base, draw_sub_menu

urlpatterns = [
    path("", base, name="main_menu"),
    path("<path:path>/", draw_sub_menu, name="draw_sub_menu"),
]
