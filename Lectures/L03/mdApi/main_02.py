from kivy.lang import Builder

from kivymd.app import MDApp

KV = '''
<StarButton@MDIconButton>
    icon: "star"
    on_release: self.icon = "star-outline" if self.icon == "star" else "star"


MDScreen:

    MDCard:
        orientation: "vertical"
        size_hint: .5, None
        height: box_top.height + box_bottom.height
        focus_behavior: True
        ripple_behavior: True
        pos_hint: {"center_x": .5, "center_y": .5}

        MDBoxLayout:
            id: box_top
            spacing: "20dp"
            adaptive_height: True

            FitImage:
                source: "/Users/macbookair/album.jpeg"
                size_hint: .3, None
                height: text_box.height

            MDBoxLayout:
                id: text_box
                orientation: "vertical"
                adaptive_height: True
                spacing: "10dp"
                padding: 0, "10dp", "10dp", "10dp"

                MDLabel:
                    text: "Ride the Lightning"
                    theme_text_color: "Primary"
                    font_style: "H5"
                    bold: True
                    adaptive_height: True

                MDLabel:
                    text: "July 27, 1984"
                    adaptive_height: True
                    theme_text_color: "Primary"

        MDSeparator:

        MDBoxLayout:
            id: box_bottom
            adaptive_height: True
            padding: "10dp", 0, 0, 0

            MDLabel:
                text: "Rate this album"
                adaptive_height: True
                pos_hint: {"center_y": .5}
                theme_text_color: "Primary"

            StarButton:
            StarButton:
            StarButton:
            StarButton:
            StarButton:
'''


class Test(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)


Test().run()