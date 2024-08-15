from contextlib import suppress
from enum import StrEnum

from django import template
from django.http import Http404

from menu_app.models import MenuItem

register = template.Library()


class TreeType(StrEnum):
    top = "top"
    child = "child"


def parse_tree(
    tree: dict[str, str | MenuItem | None],
    node: str,
    path: list[str] | None = None,
    depth_tree_name: str = "",
) -> str:
    if path is None:
        path = []
    position = path[:]
    if isinstance(tree, dict):
        for key, value in tree.items():
            position.append(key)
            if node == key:
                path = position
                return path
            elif value.get(depth_tree_name):
                parse_tree(value, node, path)
            else:
                with suppress(IndexError):
                    position.pop()
                continue


def update_deep_nested_dict(
    nested_dict: dict,
    keys: list[str],
    new_value: dict[str, str | MenuItem | None],
) -> None:
    if len(keys) == 1:
        nested_dict[keys[0]] = new_value
    else:
        key = keys[0]
        if nested_dict and key in nested_dict:
            update_deep_nested_dict(nested_dict[key], keys[1:], new_value)


def build_menu_tree_item(
    menu_items: list[MenuItem],
    main_menu_slug: str,
    tree_type: TreeType,
    sub_path: str = None,
) -> dict[str, str | MenuItem | None]:
    menu_tree = {}
    for menu_item in menu_items:
        match tree_type:
            case TreeType.top:
                path = f"{main_menu_slug}/{menu_item.slug}"
            case TreeType.child:
                path = f"{main_menu_slug}/{"/".join(sub_path)}/{menu_item.slug}"
            case _:
                path = ""
        menu_tree[menu_item.slug] = {
            "menu_item": menu_item,
            "path": path,
            "sub_tree": None,
        }
    return menu_tree


@register.inclusion_tag("menu_app/menu.html")
def draw_menu_helper(
    main_menu_slug: str | None = None,
    sub_menu_slugs: list[str] | str | None = None,
) -> dict[str, dict[str, str | MenuItem | None]]:
    def build_menu_sub_tree(
        sub_menu_slugs: list[str],
        menu_tree: dict[str, str | MenuItem | None],
        current_path: list[str] | None = None,
    ) -> dict[str, str | MenuItem | None]:
        if not sub_menu_slugs:
            return menu_tree
        slug = sub_menu_slugs.pop(0)
        current_childs = list(all_menu_items.filter(parent__slug=slug))

        if not current_childs:
            return menu_tree
        try:
            current_parent = all_menu_items.filter(slug=slug)[0]
        except IndexError:
            raise Http404("Page not found") from None
        try:
            path = parse_tree(
                menu_tree,
                current_parent.slug,
                current_path,
                depth_tree_name="sub_tree",
            )

            childs_trees = build_menu_tree_item(
                menu_items=current_childs,
                main_menu_slug=main_menu_slug,
                tree_type=TreeType.child,
                sub_path=path,
            )

            update_deep_nested_dict(
                menu_tree, path + ["sub_tree"], childs_trees
            )
        except ValueError:
            raise Http404("Page not found") from None

        return build_menu_sub_tree(
            sub_menu_slugs=sub_menu_slugs,
            menu_tree=childs_trees,
            current_path=path,
        )

    all_menu_items = MenuItem.objects.filter(menu__slug=main_menu_slug)
    top_menu_items = list(all_menu_items.filter(parent=None))

    menu_tree = build_menu_tree_item(
        menu_items=top_menu_items,
        main_menu_slug=main_menu_slug,
        tree_type=TreeType.top,
    )

    current_path = []

    return {
        "menu": build_menu_sub_tree(
            sub_menu_slugs=sub_menu_slugs,
            menu_tree=menu_tree,
            current_path=current_path,
        )
    }
