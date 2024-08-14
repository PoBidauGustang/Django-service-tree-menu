from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from tree_menu.menu_app.models import Menu


def page_not_found(request: HttpRequest, exception) -> HttpResponse:
    return render(
        request, "menu_app/404.html", {"path": request.path}, status=404
    )


def base(request: HttpRequest) -> HttpResponse:
    main_menu_items = Menu.objects.all()
    return render(
        request, "menu_app/index.html", {"main_menu_items": main_menu_items}
    )


def draw_sub_menu(request: HttpRequest, path) -> HttpResponse:
    splitted_path = path.split("/")
    sub_menu_slugs = None if len(splitted_path) == 1 else splitted_path[1:]
    return render(
        request,
        "menu_app/index.html",
        {"main_menu_slug": splitted_path[0], "sub_menu_slugs": sub_menu_slugs},
    )
