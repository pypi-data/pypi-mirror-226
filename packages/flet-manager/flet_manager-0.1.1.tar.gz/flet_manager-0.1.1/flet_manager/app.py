#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from flet_core import Page, AppView
from flet_runtime import app as flet_app


class App:
    title: str
    page: Page

    def __init__(self, title: str, main_view: type, **kwargs):
        self.title = title
        self.main_view_class = main_view
        self.main_view = None
        flet_app(target=self.start, view=AppView.FLET_APP_WEB, **kwargs)

    async def view_pop(self, view):
        self.page.views.pop()
        await self.page.update_async()

    async def view_change(self, view=None, back=False):
        if not self.page.views:
            view_next = await self.main_view.get()
            self.page.views.append(view_next)
        elif back:
            self.page.views.pop()
        else:
            view_next = await view.get()
            self.page.views.append(view_next)

        await self.page.go_async(self.page.views[-1].route)
        await self.page.update_async()

    async def start(self, page: Page):
        self.page = page
        self.page.on_view_pop = self.view_pop

        self.page.title = self.title

        self.main_view = self.main_view_class(app=self)
        self.page.views.clear()
        await self.view_change()
