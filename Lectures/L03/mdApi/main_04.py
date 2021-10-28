from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem,OneLineAvatarListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons

from nflApi import GetSchedule

KV = '''
<ListItemWithCheckbox>:

    IconLeftWidget:
        icon: root.icon

    RightCheckbox:

<listItemWithHelmets>:
    ImageLeftWidget:
        
    

MDBoxLayout:

    ScrollView:

        MDList:
            id: scroll
'''

class listItemWithHelmets(OneLineAvatarListItem):
    '''custom something'''

class ListItemWithCheckbox(OneLineAvatarIconListItem):
    '''Custom list item.'''

    icon = StringProperty("android")


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    '''Custom right container.'''


class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        data =  GetSchedule()
        icons = list(md_icons.keys())
        for game in data:
            helmet = game['team_data']['home']['image']
            self.root.ids.scroll.add_widget(
                #ListItemWithCheckbox(text=f"{game['home']}", icon=icon)
                listItemWithHelmets(text=f"{game['home']}", source=helmet)
            )


MainApp().run()