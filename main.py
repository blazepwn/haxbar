from fabric import Application
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.datetime import DateTime
from fabric.widgets.wayland import WaylandWindow as Window

from widgets.net import LocalIP, VpnIP 

class StatusBar(Window):
    def __init__(self):
        super().__init__(layer="top", anchor="left top right", exclusivity="auto", name="haxbar")

        left = Box(
            children=[
                Label(text="", css_classes=["nf","arch"]),  
                LocalIP(),
                VpnIP(),
            ],
            css_classes=["row"],
        )

        self.children = CenterBox(
            left_children=left,      
            center_children=[],     
            right_children=DateTime()  
        )

if __name__ == "__main__":
    Application("haxbar", StatusBar()).run()
