from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.utils import platform

if platform != 'android':
    from kivy.config import Config
    Config.set('input', 'mouse', 'mouse,disable_on_activity')
from kivy.uix.popup import Popup
from channels_ch import ChannelSelectionPopup
from connection import ConnectionPopup
from impedance import ImpdPopup
from dinamic_grafs import DGraph
import kivy
from kivy.core.window import Window
from kivy.utils import platform
from kivy.config import Config
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.button import *

kivy.config.Config.set('graphics', 'resizable', False)


class EEGApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.channels = 16  # количество каналов записи
        self.is_recording = False
        self.edf_writer = None
        self.sample_rate = 1000
        self.eeg_data = []
        self.demo_play = False
        self.bl_popup = None
        self.icon = 'ic_2.png'
        Config.set('graphics', 'resizable', False)
        if platform == 'android':
            Window.maximize()
        else:
            Window.size = (1242 * 0.28, 2208 * 0.28)
            #Window.size = (1344 * 0.6, 756 * 0.6)  # (1920, 1080)
        self.graphs = []
        self.error = False
        self.btn_amp = None
        self.file = None
        self.names_of_channels = ('Fp1', 'GND', 'Fp2', 'T3', 'F3', 'Fz', 'F4', 'T4',
                                  'C3', 'Cz', 'C4', 'P3', 'Pz', 'P4', 'O1', 'O2')
        self.i = 1

    def build(self):
        self.layout = MDBoxLayout(orientation='vertical', md_bg_color=[.184, .192, .251, 1])
        upbuttons = MDBoxLayout(orientation='horizontal', size_hint=(1, .14), padding=13,
                                spacing=10, line_color=[.106, 0.11, .141, 1], line_width=3)
        self.buttons = MDGridLayout(size_hint=(1, .25), cols=2, padding=13, spacing=10, line_color=[.106, 0.11, .141, 1],
                               line_width=1.5)

        self.btn_amp = MDButton(MDButtonText(text='Поиск усилителя',
                                             pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                             theme_text_color="Custom",
                                             text_color=[.184, .192, .251, 1]),
                                style="elevated",
                                theme_width="Custom",
                                on_press=self.show_bluetooth_devices)
        self.btn_hand = MDButton(MDButtonText(text='Поиск протеза',
                                              pos_hint={'center_x': 0.5, 'center_y':0.5},
                                              theme_text_color="Custom",
                                              text_color=[.184, .192, .251, 1]),
                                 theme_width="Custom",
                                 on_press=self.show_bluetooth_devices_hand)
        self.btn_4 = MDButton(MDButtonText(text='Выбор каналов',
                                           pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                           theme_text_color="Custom",
                                           text_color=[.184, .192, .251, 1]),
                              theme_width="Custom",
                              on_press=self.set_4)
        self.btn_record = MDButton(MDButtonText(text='Запись',
                                                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                                theme_text_color="Custom",
                                                text_color=[.184, .192, .251, 1]),
                                   theme_bg_color='Custom',
                                   md_bg_color=[1, 1, 1, .95],
                                   style='filled',
                                   theme_width="Custom",
                                 on_press=self.on_record)
        self.btn_com = MDButton(MDButtonText(text='Команды',
                                             pos_hint={'center_x': 0.5, 'center_y':0.5},
                                             theme_text_color="Custom",
                                             text_color=[.184, .192, .251, 1]),
                                theme_width="Custom",
                                on_press=self.on_record)
        self.btn_impd = MDButton(MDButtonText(text='Импеданс',
                                              pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                              theme_text_color="Custom",
                                              text_color=[.184, .192, .251, 1]),
                                 theme_width="Custom",
                                 on_press=self.show_impd)

        self.btn_start = MDIconButton(icon="play",
                                      style='filled',
                                      on_press=self.start_eeg)

        self.buttons.add_widget(self.btn_4)
        self.buttons.add_widget(self.btn_impd)
        self.buttons.add_widget(self.btn_record)
        upbuttons.add_widget(self.btn_hand)
        upbuttons.add_widget(self.btn_amp)

        self.buttons.add_widget(self.btn_com)
        upbuttons.add_widget(self.btn_start)

        # Макет для графиков ЭЭГ
        self.graph_layout = DGraph(orientation='vertical')
        self.layout.add_widget(upbuttons)
        self.layout.add_widget(self.graph_layout)
        self.layout.add_widget(self.buttons)
        return self.layout

    def show_bluetooth_devices(self, instance):
        try:
            self.bl_popup = ConnectionPopup(size_hint=(.85, .85), auto_dismiss=False, device_type='amp')
            self.bl_popup.open()

        except OSError:
            self.notconnect(ltext='Включите блютуз')
            return

    def start_eeg(self, instance):
        if self.bl_popup.selected_amp_name is not None and (not self.demo_play):
            self.layout.remove_widget(self.graph_layout)
            graph_layout1 = DGraph(orientation='vertical')
            self.layout.add_widget(graph_layout1)
            self.btn_amp._button_text.text = self.bl_popup.selected_amp_name
            self.layout.remove_widget(self.buttons)
            self.layout.add_widget(self.buttons)
            graph_layout1.choose()
        else:
            if not self.demo_play:
                self.graph_layout.demo()
                self.demo_play = True
                self.btn_start.icon = 'pause'
                #self.notconnect()
            else:
                self.graph_layout.stop_demo()
                self.demo_play = False
                self.btn_start.icon = 'play'


    def notconnect(self, ltext='Сначала подключите устройство'):
        l1 = Label(text=ltext)
        cntnt = MDBoxLayout(orientation='vertical')
        cntnt.add_widget(l1)
        popup = Popup(title='Внимание', content=cntnt, size_hint=(.8, .4))
        popup.open()
        popup_close_btn = Button(text='Ок', on_release=popup.dismiss, pos_hint={'x': 0, 'y': 0}, size=(60, 40),
                                 font_size=20)
        cntnt.add_widget(popup_close_btn)

    def show_bluetooth_devices_hand(self, instance):
        pass

    def on_record(self, instance):
        if self.bl_popup.selected_amp_name is not None:
            if not self.is_recording:
                self.is_recording = True
                self.btn_record._button_text.text = 'Стоп'
                self.btn_record._button_text.color = '941010'
                filename = f'data{self.i}.txt'
                self.i += 1
                self.file = open(filename, "w")
                Clock.schedule_interval(self.record_data, 0.1)

            else:
                self.file.close()
                self.is_recording = False
                self.btn_record._button_text.text = 'Запись'
                self.btn_record._button_text.color = [47/255, 49/255, 64/255, 1]

                self.btn_record.md_bg_color = 'white'
                self.is_recording = False
        else:
            self.notconnect()
            # Окончание записи данных и сохранение файла при нажатии на стоп

    def record_data(self, dt):
        if self.is_recording:
            data = []
            data = ConnectionPopup.amp.read(
                indices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                eegcount=ConnectionPopup.amp.CountEeg
            )
            if data:
                self.file.write(str(data)+'\n')

    def set_4(self, instance):
        if self.bl_popup.selected_amp_name is not None:
            channel_selection_popup = ChannelSelectionPopup(
                channels=["Канал " + i for i in self.names_of_channels])  # + str(i) for i in range(1, 17)])
            channel_selection_popup.open()
        else:
            self.notconnect()

    def show_impd(self, instance):
        if self.bl_popup.selected_amp_name is not None:
            impdp = ImpdPopup()
            impdp.open()
        else:
            self.notconnect()

    # функция отключения усилителя при закрытии приложения
    def on_stop(self):
        if ConnectionPopup.amp:
            ConnectionPopup.amp.stop()
            ConnectionPopup.amp.close()
        if self.file:
            self.file.close()


if __name__ == '__main__':
    EEGApp().run()
