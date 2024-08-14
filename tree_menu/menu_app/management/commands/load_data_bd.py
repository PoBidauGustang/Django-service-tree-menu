from django.core.management import BaseCommand
from django.utils.crypto import get_random_string

from menu_app.models import Menu, MenuItem


class Command(BaseCommand):
    menu_size: int = 4
    menu_depth: int = 3

    def __create_menu_items(
        self,
        level_name: str,
        menu: Menu,
        parent: MenuItem = None,
        depth: int = 0,
    ) -> None:
        if depth >= self.menu_depth:
            return

        for i in range(self.menu_size):
            menu_item_name = f"{level_name}::level-{depth+1}::item-{i+1}::sub_menu_name-{get_random_string(4)}"
            menu_item = MenuItem.objects.create(
                name=menu_item_name,
                menu=menu,
                parent=parent,
                slug=menu_item_name,
            )
            self.__create_menu_items(level_name, menu, menu_item, depth + 1)

    def __create_menu(self, menu_name: str) -> None:
        menu = Menu.objects.create(name=menu_name, slug=menu_name)
        self.__create_menu_items(level_name=menu.name, menu=menu)

    def handle(self, *args, **kwargs):
        for i in range(self.menu_size):
            menu_name = f"{i + 1}_menu"
            self.__create_menu(menu_name)
        print(f"\n\n{"Data was loaded successfully"}\n\n")
