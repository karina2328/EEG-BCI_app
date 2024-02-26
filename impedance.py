from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.graphics import Color, Ellipse
from kivy.core.window import Window
from neorec import *
from connection import ConnectionPopup

class ImpdPopup(Popup):
    def __init__(self, **kwargs):
        super(ImpdPopup, self).__init__(**kwargs)
        self.layout_im = BoxLayout(orientation='vertical', spacing=10)
        self.fl_layout = BoxLayout(orientation='horizontal', spacing=10, padding=10, size_hint=(1, .1))
        self.values_impd = []
        self.im_eeg = Image(source='EEG_1.png')
        self.title = 'Импеданс электродов'
        self.layout_im.add_widget(self.im_eeg)
        self.btn_check = Button(text='Обновить', on_release=self.redraw, size_hint=(.5, 1), height='500dp')
        self.btn_dsms = Button(text='Закрыть', on_release=self.close, size_hint=(.5, 1), height='500dp')
        self.fl_layout.add_widget(self.btn_check)
        self.fl_layout.add_widget(self.btn_dsms)
        self.layout_im.add_widget(self.fl_layout)
        self.content = self.layout_im


    def close(self, button):
        self.clear_widgets()
        self.dismiss()

    #Fp1, GND, Fp2, T3, F3, Fz, F4, T4, C3, Cz,  C4, P3, Pz, P4, O1, O2

    def get_impedance(self):
        ConnectionPopup.amp.setup(
            mode=NR_MODE_IMPEDANCE,
            rate=NR_RATE_125HZ,
            range=NR_RANGE_mV300
        )
        ConnectionPopup.amp.start()

        imp = None
        imp = ConnectionPopup.amp.readImpedances()
        print(imp)
        return imp

    def on_open(self):
        self.values_impd = self.get_impedance()
        #self.values_impd = [3,34,3,3,2,34,444,4,4,33,5,4,3,33,33,3,3]
        with self.im_eeg.canvas.after:
            positions = [(248, 278), (330, 140), (329, 210), (323, 279), (320, 361),
                         (330, 450), (400, 430), (400, 361), (405, 279), (400, 210),
                         (470, 140), (470, 210), (480, 279), (478, 361), (459, 450),
                         (552, 278), (600, 130)]
            posit = [(self.width*.18, self.height*.47),
                   (self.width*.35, self.height*.32), (self.width*.34, self.height*.39),
                   (self.width*.32, self.height*.47), (self.width*.32, self.height*.56),
                   (self.width*.37, self.height*.66), (self.width*.48, self.height*.63),
                   (self.width*.48, self.height*.56), (self.width*.48, self.height*.47),
                   (self.width*.48, self.height*.39), (self.width*.62, self.height*.32),
                   (self.width*.63, self.height*.39), (self.width*.64, self.height*.47),
                   (self.width*.64, self.height*.56), (self.width*.59, self.height*.66),
                   (self.width*.78, self.height*.47), (self.width*.88, self.height*.29)]
            for i, value_impd in enumerate(self.values_impd):
                #x, y = positions[i]
                x, y = posit[i]
                if value_impd > 50:
                    Color(1, 0, 0)
                elif value_impd > 37.5:
                    Color(1, 0.5, 0)
                elif value_impd > 25:
                    Color(1, 1, 0)
                elif value_impd > 12.5:
                    Color(0.7, 1, 0.1)
                elif value_impd == 0:
                    Color(0, 0, 0)
                else:
                    Color(0, 1, 0)
                #self.radius = Window.size[0]*Window.size[1]*0.000017
                Ellipse(pos=(x, y),
                        size=(self.width / 20, self.width / 20))
                '''Ellipse(pos=(x*1.13-self.radius+160, y*1.1 - self.radius-10),
                        size=(self.width / 20, self.width / 20))'''
                        #size=(self.radius*2, self.radius*2))


    def redraw(self, instance):
        self.dismiss()
        self.open()
        #self.on_open()

