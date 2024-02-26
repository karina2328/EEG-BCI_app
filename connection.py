from functools import partial
from kivy.uix.button import Button
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.popup import Popup
import asyncio
from neorec import *
from bleak import BleakScanner


class ConnectionPopup(Popup):
    amp = NeoRec()
    def __init__(self, device_type, **kwargs):
        super(ConnectionPopup, self).__init__(**kwargs)
        self.devices = []
        self.title = "Выберите устройство"
        self.selected_amp_name = None
        self.selected_hand_name = None
        self.selected_device = None
        self.channels = 4
        self.err = False
        self.device_type = device_type
        self.selected_amp_addr = None
        self.selected_hand_addr = None
        self.text = ''
        self.channel_indices = []


        # Вертикальный BoxLayout для размещения кнопок устройств
        layout0 = MDBoxLayout(orientation='vertical', spacing=3)
        self.layout1_1 = MDBoxLayout(orientation='vertical', spacing=3)

        # Создаем кнопки для каждого устройства и добавляем их в layout
        if self.device_type == 'amp':
            asyncio.run(self.create_btns())  # функция для создания кнопок в первом лэйауте ниже
        elif self.device_type == 'hand':
            self.create_btns_h()

        layout0.add_widget(self.layout1_1)
        layout1_2 = MDBoxLayout(orientation='horizontal', spacing=3)

        # Создаем кнопку "Подключить"
        connect_btn = Button(text='Подключить', size_hint=(1, None), height='40dp')
        connect_btn.bind(on_release=self.connect_device)
        layout1_2.add_widget(connect_btn)

        close_btn = Button(text='Закрыть', size_hint=(1, None), height='40dp', on_release=self.close)

        # Создаем кнопку "Обновить"
        refresh_btn = Button(text='Обновить', size_hint=(1, None), height='40dp')
        refresh_btn.bind(on_release=self.refresh_devices)
        layout1_2.add_widget(refresh_btn)
        layout0.add_widget(layout1_2)
        layout1_2.add_widget(close_btn)

        self.content = layout0  # Размещаем layout в контенте

    def close(self, instance):
        self.clear_widgets()
        self.dismiss()

    def refresh_devices(self, instance):
        self.layout1_1.clear_widgets()
        asyncio.run(self.create_btns())

    def create_btns_h(self):
        pass

    async def create_btns(self):
        scanner = BleakScanner()
        await scanner.start()
        await asyncio.sleep(5)
        await scanner.stop()
        self.devices = scanner.discovered_devices
        for device in self.devices:
            if device.name:
                btn = Button(text=str(device.name), size_hint=(1, None), height='40dp')
                btn.bind(on_release=partial(self.select_device, name=device.name, addr=device.address))
                self.layout1_1.add_widget(btn)

    def select_device(self, instance, name, addr):
        # Выделяем выбранное устройство другим цветом
        for device_btn in self.layout1_1.children:
            if device_btn.__class__.__name__ == 'Button':
                device_btn.background_color = (1, 1, 1, 1)  # Сбрасываем цвет всех кнопок
        instance.background_color = (0, 1, 0, 1)
        if self.device_type == 'amp':
            self.selected_amp_name = name
            self.selected_amp_addr = addr
            #print(self.selected_amp_name, self.selected_amp_addr)
        elif self.device_type == 'hand':
            self.selected_hand_name = name
            self.selected_hand_addr = addr

            print(self.selected_hand_name, self.selected_hand_addr)

    def connect_device(self, instance):
        if self.device_type == 'amp':
            try:
                self.selected_device = self.selected_amp_addr
                if self.selected_device is not None:
                    self.amp.open()
                    self.amp.setup(
                        mode=NR_MODE_DATA,
                        rate=NR_RATE_250HZ,
                        range=NR_RANGE_mV300
                    )
                    self.amp.start()
                    self.channel_indices = [i for i in range(self.amp.CountEeg)]  #self.channel_indices = np.arange(0, self.amp.CountEeg)
                    print(type(self.channel_indices))
                    self.clear_widgets()
                    self.dismiss()
                    #Clock.schedule_interval(self.graph_layout.update_graphs, 0.3)

                    #EEGApp.reading_eeg()
                    '''eeg = None
                    while eeg is None:
                        eeg = self.amp.read(
                            indices=channel_indices,
                            eegcount=len(channel_indices)
                        )
                    print(eeg)'''


                    #self.amp.stop()
            except:
                print("Подключиться не удалось")
                self.err = True

        elif self.device_type == 'hand':
            self.selected_device = self.selected_hand_addr




