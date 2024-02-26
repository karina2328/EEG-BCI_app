from kivy.uix.boxlayout import BoxLayout
from kivy_grafs import Graph, MeshLinePlot
from connection import ConnectionPopup
from channels_ch import ChannelSelectionPopup
from kivy.clock import Clock
import random

class DGraph(BoxLayout):
    def __init__(self, **kwargs):
        super(DGraph, self).__init__(**kwargs)
        self.plots = []
        self.graphs = []
        self.ymax=230
        self.show_graphs = True
        self.channels = None
        self.names_of_channels = ('Fp1', 'GND', 'Fp2', 'T3', 'F3', 'Fz', 'F4', 'T4',
                                  'C3', 'Cz', 'C4', 'P3', 'Pz', 'P4', 'O1', 'O2')
        for i in range(4):
            self.graph = Graph(tick_color=[169/255, 179/255, 181/255, .6], border_color=[169/255, 179/255, 181/255, .6], label_options={'color': [169/255, 179/255, 181/255, 1]},
                               xlabel='time', ylabel='U (mV)', x_ticks_minor=.05, x_ticks_major=20, y_ticks_major=100, draw_border=False,
                               y_grid_label=True, x_grid_label=False, padding=2, x_grid=False, y_grid=True, xmin=-0,
                               xmax=12, ymin=-230, ymax=self.ymax, font_size=20, background_color=[67/255, 70/255, 92/255, .9]) #[.8, .8, .8, 1])
            self.plot = MeshLinePlot(color=[.27, 0.99, 0.75, 1])
            self.plots.append(self.plot)
            self.add_widget(self.graph)
            self.graph.add_plot(self.plot)
            self.graphs.append(self.graph)

            # попробовать изменить размер графиков

    def choose(self):
        self.channels = ChannelSelectionPopup(channels=["Канал " + i for i in self.names_of_channels])
        self.channels.open()
        self.ch_indices = self.channels.selected_indices
        for graph in self.graphs:
            self.plot = MeshLinePlot(color=[.27, 0.99, 0.75, 1])
            graph.add_plot(self.plot)
        Clock.schedule_interval(self.update_graphs, 0.3)

    def demo(self):
        #if self.show_graphs:
        Clock.schedule_interval(self.demo_update, 0.3)

    def stop_demo(self):
        #self.show_graphs = False
        Clock.unschedule(self.demo_update)
        #self.plots=[]
        '''for graph in self.graphs:
            for plot in graph.plots:
                graph.remove_plot(plot)
                graph._clear_buffer()'''


    def demo_update(self,dt):

        data1 = [random.uniform(-230, 170) for i in range(200)]
        data2 = [random.uniform(-230, 170) for i in range(200)]
        data3 = [random.uniform(-230, 270) for i in range(200)]
        data4 = [random.uniform(-230, 170) for i in range(200)]
        data = [data1, data2, data3, data4]
        for i, graph in enumerate(self.plots):
            graph.points = [(idx, value) for idx, value in enumerate(data[i])]
            for idx, value in enumerate(data[i]):
                if value > self.graph.ymax:
                    self.graph.ymax = value

        '''for p in graph.points[1]:
            if p > self.graph.ymax:
                self.graph.ymax = int(p)
            elif p < self.graph.ymin:
                self.graph.ymin = int(p)'''

    def update_graphs(self, dt):
        eeg = []
        eeg = ConnectionPopup.amp.read(
            indices=self.ch_indices,
            eegcount=ConnectionPopup.amp.CountEeg
        )

        '''eeg = None
        while eeg is None:
            eeg = ConnectionPopup.amp.read(
                indices=self.ch_indices,
                eegcount=4
            )'''
        if len(self.ch_indices) == 4:
            print(eeg)
            # Generate random data (replace with actual data from the device)
            '''data1 = [random.uniform(0, 20) for i in range(100)]
            data2 = [random.uniform(0, 20) for i in range(100)]
            data3 = [random.uniform(0, 20) for i in range(100)]
            data4 = [random.uniform(0, 20) for i in range(100)]'''
            data1 = eeg[0][0]
            data2 = eeg[0][1]
            data3 = eeg[0][2]
            data4 = eeg[0][3]

            data = [data1, data2, data3, data4]

            for i, graph in enumerate(self.plots):
                graph.points = [(idx, value) for idx, value in enumerate(data[i])]
                for p in graph.points[1]:
                    if p>self.graph.ymax:
                        self.graph.ymax=int(p)
                    elif p<self.graph.ymin:
                        self.graph.ymin=int(p)


