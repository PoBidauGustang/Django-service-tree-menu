from django.contrib import admin

from tree_menu.menu_app.models import Menu, MenuItem


class MenuAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "parent", "menu", "description")
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
