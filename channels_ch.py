from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup


class ChannelSelectionPopup(Popup):
    def __init__(self, channels, **kwargs):
        super(ChannelSelectionPopup, self).__init__(**kwargs)
        self.title = 'Выбор каналов'
        self.layout = BoxLayout(orientation="vertical", spacing=10)
        self.layout_gr = GridLayout(cols=4, spacing=10)
        self.selected_channels = []
        self.selected_indices = []  # массив с индексами выбранных каналов
        self.data = [[]]

        for channel in channels:
            channel_button = Button(text=channel, on_release=self.toggle_channel, font_size=20)
            self.layout_gr.add_widget(channel_button)

        confirm_button = Button(text="OK", on_release=self.confirm_selection, size_hint=(1, .2), font_size=25)
        self.layout.add_widget(self.layout_gr)
        self.layout.add_widget(confirm_button)
        self.content = self.layout

    def toggle_channel(self, button):
        if "[\/] " not in button.text:
            channel_name = button.text.replace('Канал ', '')
            if len(self.selected_channels) < 4:
                self.selected_channels.append(channel_name)
                #for i in self.selected_channels:
                if channel_name == 'Fp1':
                    self.selected_indices.append(1)
                if channel_name == 'Fp2':
                    self.selected_indices.append(2)
                if channel_name == 'F3':
                    self.selected_indices.append(3)
                if channel_name == 'F4':
                    self.selected_indices.append(4)
                if channel_name == 'C3':
                    self.selected_indices.append(5)
                if channel_name == 'C4':
                    self.selected_indices.append(6)
                if channel_name == 'P3':
                    self.selected_indices.append(7)
                if channel_name == 'P4':
                    self.selected_indices.append(8)
                if channel_name == 'O1':
                    self.selected_indices.append(9)
                if channel_name == 'O2':
                    self.selected_indices.append(10)
                if channel_name == 'T3':
                    self.selected_indices.append(11)
                if channel_name == 'T4':
                    self.selected_indices.append(12)
                if channel_name == 'Fz':
                    self.selected_indices.append(13)
                if channel_name == 'Cz':
                    self.selected_indices.append(14)
                if channel_name == 'Pz':
                    self.selected_indices.append(15)
                if channel_name == 'GND':
                    self.selected_indices.append(16)
                button.text = "[\/] " + channel_name
                button.background_color = (0, 1, 1, 1)
            else:
                print("Выбрано максимальное количество каналов")
        else:
            button.text = button.text.replace("[\/] ", "")
            self.selected_channels.remove(button.text)  # массив с именами выбранных каналов
            if button.text == 'Fp1':
                self.selected_indices.remove(1)
            if button.text == 'Fp2':
                self.selected_indices.remove(2)
            if button.text == 'F3':
                self.selected_indices.remove(3)
            if button.text == 'F4':
                self.selected_indices.remove(4)
            if button.text == 'C3':
                self.selected_indices.remove(5)
            if button.text == 'C4':
                self.selected_indices.remove(6)
            if button.text == 'P3':
                self.selected_indices.remove(7)
            if button.text == 'P4':
                self.selected_indices.remove(8)
            if button.text == 'O1':
                self.selected_indices.remove(9)
            if button.text == 'O2':
                self.selected_indices.remove(10)
            if button.text == 'T3':
                self.selected_indices.remove(11)
            if button.text == 'T4':
                self.selected_indices.remove(12)
            if button.text == 'Fz':
                self.selected_indices.remove(13)
            if button.text == 'Cz':
                self.selected_indices.remove(14)
            if button.text == 'Pz':
                self.selected_indices.remove(15)
            if button.text == 'GND':
                self.selected_indices.remove(16)
            button.background_color = (1, 1, 1, 1)


        self.channel_indices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]


        print(self.selected_channels)
        print(self.selected_indices)  # массив выбранных индексов

    def confirm_selection(self, button):
        if len(self.selected_channels) == 4:
            for selected_channel in self.selected_channels:
                print("Выбран канал:", selected_channel)
            self.clear_widgets()
            self.dismiss()
        else:
            print("Выберите 4 канала")
