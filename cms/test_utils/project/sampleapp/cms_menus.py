from django.urls import NoReverseMatch, reverse
from django.utils.translation import gettext_lazy as _

from cms.menu_bases import CMSAttachMenu
from cms.test_utils.project.sampleapp.models import Category
from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool


class SampleAppMenu(Menu):

    def get_nodes(self, request):
        nodes = []
        for cat in Category.objects.all():
            n = NavigationNode(cat.name, cat.get_absolute_url(), cat.pk, cat.parent_id, "sampleapp")
            nodes.append(n)
        try:
            n = NavigationNode(_('sample root page'), reverse('sample-root'), 1)
            n2 = NavigationNode(_('sample settings page'), reverse('sample-settings'), 2)
            n3 = NavigationNode(_('sample account page'), reverse('sample-account'), 3)
            n4 = NavigationNode(_('sample my profile page'), reverse('sample-profile'), 4, 3)
            nodes.append(n)
            nodes.append(n2)
            nodes.append(n3)
            nodes.append(n4)

class StaticMenu2(StaticMenu):
    name = _("Static Menu2")


menu_pool.register_menu(StaticMenu2)


class StaticMenu3(StaticMenu):
    name = _("Static Menu3")


menu_pool.register_menu(StaticMenu3)


class StaticMenu4(CMSAttachMenu):
    name = _("Static Menu4")

    def get_nodes(self, request):
        nodes = []
        nodes.append(NavigationNode('static fresh', '/static/fresh/', 'static fresh'))
        nodes.append(NavigationNode('sample2-root', reverse('sample2-root'), 'sample2-root'))
        return nodes


menu_pool.register_menu(StaticMenu4)
