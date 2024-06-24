# This file is part of Nomerin Aitashy.
#
# Nomerin Aitashy is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# Nomerin Aitashy is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Nomerin Aitashy. If not, see <https://www.gnu.org/licenses/>.

import asyncio
import configparser

import aiofiles
import flet as ft
from flet import icons

from main_tab_views import (
    AboutTabView,
    GuideTabView,
    PracticeTabView,
    RootTabView,
    SettingsTabView,
)
from master_parts import MasterAppBar, MasterNavigationBar


class TextController:
    def __init__(self):
        self._config = None

    async def load_config(self):
        async with aiofiles.open(
            "language.properties", mode="r", encoding="utf-8"
        ) as f:
            content = await f.read()

        config = configparser.ConfigParser()
        config.read_string(content)
        self._config = config

    def get(self, name: str, locale: str = "en_US") -> str:
        if not self._config:
            raise ValueError(
                "Configuration not loaded. Please load the configuration before calling get."
            )
        if not name or not locale:
            raise ValueError("Name and locale cannot be empty.")

        if not self._config.has_section(locale):
            raise ValueError(f"No section '{locale}' found in language file.")
        if not self._config.has_option(locale, name):
            raise ValueError(f"No option '{name}' found in '{locale}' section.")

        return self._config.get(locale, name).encode("utf-8").decode("unicode_escape")


class Controller:
    def __init__(self, page: ft.Page, text_controller: TextController):
        self.__page = page
        self._config = None
        self.text_controller = text_controller
        self.navigation_bar = MasterNavigationBar(text_controller)

    async def _route_guide(self):
        # TODO Better route management ex "/lesson1" -> "/guide/lesson1" and so on
        self.__page.views.clear()
        self.__page.views.append(
            GuideTabView(
                text_controller=self.text_controller,
                navigation_bar=MasterNavigationBar(self.text_controller),
                app_bar=MasterAppBar(self.text_controller.get("guide_txt")),
            )
        )

    async def _route_practice(self):
        # TODO Better route management ex "/level1 " -> "/practice/level1" and so on
        self.__page.views.clear()
        self.__page.views.append(
            PracticeTabView(
                text_controller=self.text_controller,
                navigation_bar=MasterNavigationBar(self.text_controller),
                app_bar=MasterAppBar(self.text_controller.get("practice_txt")),
            )
        )

    async def _route_about(self):
        self.__page.views.clear()
        self.__page.views.append(
            AboutTabView(
                text_controller=self.text_controller,
                navigation_bar=MasterNavigationBar(self.text_controller),
                app_bar=MasterAppBar(self.text_controller.get("about_txt")),
            )
        )

    async def _route_setting(self):
        self.__page.views.append(
            SettingsTabView(
                text_controller=self.text_controller,
                navigation_bar=MasterNavigationBar(self.text_controller),
                app_bar=MasterAppBar(
                    self.text_controller.get("settings_txt"), icons.SETTINGS
                ),
            )
        )

    async def _route_root(self):
        # TODO Don't apper root page if start button pressed by user
        self.__page.views.clear()
        self.__page.views.append(
            RootTabView(
                text_controller=self.text_controller,
                app_bar=MasterAppBar(self.text_controller.get("welcome_txt")),
            )
        )

    async def routechange(self, e: ft.RouteChangeEvent):
        if e.route == "/":
            await self._route_root()
        elif e.route.startswith("/guide"):
            await self._route_guide()
        elif e.route.startswith("/about"):
            await self._route_about()
        elif e.route.startswith("/practice"):
            await self._route_practice()
        elif e.route.startswith("/settings"):
            await self._route_setting()
        else:
            self.__page.go("/")
        self.__page.update()

    async def view_pop(self, view):
        self.__page.views.pop()
        top_view = self.__page.views[-1]
        self.__page.go(top_view.route)


if __name__ == "__main__":
    text_controller = TextController()
    asyncio.run(text_controller.load_config())
    print(text_controller.get("welcome_txt"))
