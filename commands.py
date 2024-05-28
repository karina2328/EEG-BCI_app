import bleak
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.popup import Popup
from kivymd.uix.button import *
from connection import ConnectionPopup

class CmdPopup(Popup):
    def __init__(self, **kwargs):
        super(CmdPopup, self).__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=15)
        cmd_layout = MDGridLayout(cols=2, spacing=50, padding=25)
        self.title = 'Выбор команд'
        cmd_button1 = MDButton(MDButtonText(text='Разжать', pos_hint={'center_x': 0.5, 'center_y':0.5}), on_release=self.c1)
        cmd_button2 = MDButton(MDButtonText(text='Сжать', pos_hint={'center_x': 0.5, 'center_y':0.5}), on_release=self.c2)
        cmd_button3 = MDButton(MDButtonText(text='Жест 1', pos_hint={'center_x': 0.5, 'center_y':0.5}), on_release=self.c3)
        cmd_button4 = MDButton(MDButtonText(text='Жест 2', pos_hint={'center_x': 0.5, 'center_y':0.5}), on_release=self.c4)
        cmd_button5 = MDButton(MDButtonText(text='Жест 3', pos_hint={'center_x': 0.5, 'center_y':0.5}), on_release=self.c5)
        cmd_button6 = MDButton(MDButtonText(text='Жест 4', pos_hint={'center_x': 0.5, 'center_y':0.5}), on_release=self.c6)
        cmd_button7 = MDButton(MDButtonText(text='Жест 5', pos_hint={'center_x': 0.5, 'center_y': 0.5}),
                               on_release=self.c3)
        cmd_button8 = MDButton(MDButtonText(text='Жест 6', pos_hint={'center_x': 0.5, 'center_y': 0.5}),
                               on_release=self.c4)
        cmd_button9 = MDButton(MDButtonText(text='Жест 7', pos_hint={'center_x': 0.5, 'center_y': 0.5}),
                               on_release=self.c5)
        cmd_button10 = MDButton(MDButtonText(text='Жест 8', pos_hint={'center_x': 0.5, 'center_y': 0.5}),
                               on_release=self.c6)
        cmd_button11 = MDButton(MDButtonText(text='Жест 9', pos_hint={'center_x': 0.5, 'center_y': 0.5}),
                               on_release=self.c5)
        cmd_button12 = MDButton(MDButtonText(text='Жест 10', pos_hint={'center_x': 0.5, 'center_y': 0.5}),
                                on_release=self.c6)
        cmd_layout.add_widget(cmd_button1)
        cmd_layout.add_widget(cmd_button2)
        cmd_layout.add_widget(cmd_button3)
        cmd_layout.add_widget(cmd_button4)
        cmd_layout.add_widget(cmd_button5)
        cmd_layout.add_widget(cmd_button6)
        cmd_layout.add_widget(cmd_button7)
        cmd_layout.add_widget(cmd_button8)
        cmd_layout.add_widget(cmd_button9)
        cmd_layout.add_widget(cmd_button10)
        cmd_layout.add_widget(cmd_button11)
        cmd_layout.add_widget(cmd_button12)
        btn_dsms = MDButton(MDButtonText(text='Назад',pos_hint={'center_x': 0.5, 'center_y':0.5},
                                              theme_text_color="Custom",
                                              text_color=[.184, .192, .251, 1]), on_release=self.close, theme_width="Custom",size_hint=(1, .2))
        layout.add_widget(cmd_layout)
        layout.add_widget(btn_dsms)
        self.content = layout

        self.uuid_hand = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
    def c1(self,btn):
        self.cmd_for_hand = '80805050ff81815050ff82825050ff83835050ff84845050ff'
        self.send_cmd(self.cmd_for_hand)
    def c2(self,btn):
        self.cmd_for_hand = 'c0c05050ffc1c15050ffc2c25050ffc3c35050ffc4c45050ff'
        self.send_cmd(self.cmd_for_hand)
    def c3(self,btn):
        self.cmd_for_hand = '81815050ffc2c25050ff82826060ff'
        self.send_cmd(self.cmd_for_hand)
    def c4(self,btn):
        self.cmd_for_hand = 'c1c12020ff'
        self.send_cmd(self.cmd_for_hand)
    def c5(self,btn):
        self.cmd_for_hand = '82827070ffc0c01010ff'
        self.send_cmd(self.cmd_for_hand)
    def c6(self,btn):
        self.cmd_for_hand = 'c2c25050ff'
        self.send_cmd(self.cmd_for_hand)
    def send_cmd(self,cmd):
        asyncio.run(send_cmd_to_hand(self.cmd_for_hand)

    async def send_cmd_to_hand(self, cmd):
        async with bleak.BleakClient(ConnectionPopup.selected_device) as client:
            await client.connect()
            ar = bytes.fromhex(cmd)
            await client.write_gatt_char(self.uuid_hand, ar)
            await client.disconnect()
    def close(self, button):
        self.clear_widgets()
        self.dismiss()
