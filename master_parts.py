from flet import (
    AppBar,
    IconButton,
    NavigationBar,
    NavigationBarDestination,
    NavigationBarLabelBehavior,
    Text,
    View,
    icons,
)

from text_controller import about_txt, guide_txt, practice_txt


class Master_Tab_View(View):
    """
    Initializes a Master_View object.

    Args:
        navigation_bar: NavigationBar object for the view.
        app_bar: AppBar object for the view.
    """

    def __init__(self, navigation_bar, app_bar):
        super().__init__()
        self.appbar = app_bar
        self.navigation_bar = navigation_bar


class Master_App_Bar(AppBar):
    def __init__(self, text, icon=icons.SETTINGS_OUTLINED):
        super().__init__()
        self.title = Text(text)
        self.actions = [IconButton(icon=icon, on_click=self.goto_settings)]

    def goto_settings(self, e):
        if e.page.route != "/settings":
            e.page.go("/settings")
        else:
            e.page.views.pop()
            e.page.go(e.page.views[-1].route)


class Master_Navigation_Bar(NavigationBar):
    def __init__(self):
        super().__init__()
        self.adaptive = True
        self.label_behavior = NavigationBarLabelBehavior.ONLY_SHOW_SELECTED
        self.on_change = self.select_tab
        self.selected_index = 1
        self.destinations = [
            NavigationBarDestination(
                icon=icons.BOOK_OUTLINED,
                selected_icon=icons.BOOK,
                label=guide_txt,
            ),
            NavigationBarDestination(
                icon=icons.MENU,
                selected_icon=icons.MENU_OPEN,
                label=practice_txt,
            ),
            NavigationBarDestination(
                icon=icons.INFO_OUTLINED,
                selected_icon=icons.INFO,
                label=about_txt,
            ),
        ]

    def select_tab(self, e):
        if e.control.selected_index == 0:
            e.page.route = "/guide"
        if e.control.selected_index == 1:
            e.page.route = "/practice"
        if e.control.selected_index == 2:
            e.page.route = "/about"
        e.page.update()