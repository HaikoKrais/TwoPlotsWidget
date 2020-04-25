from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty
import json
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import matplotlib.dates as dt
from datetime import datetime
from time import gmtime, asctime, strftime, mktime, strptime


class TwoPlotsWidget(FigureCanvasKivyAgg):

    plt.style.use('dark_background')
    
    timestamp = []
    temperature = []
    humidity = []
    units = ObjectProperty(['--','--'])
    titles = ObjectProperty(['--','--'])
    ax_colors = ObjectProperty(['g','g'])
    notification = StringProperty('')

    def __init__(self, **kwargs):
        '''__init__ takes the figure the backend is going to work with'''
        super(TwoPlotsWidget, self).__init__(plt.gcf(), **kwargs)

    def update_plot(self, *args, **kwargs):
        '''reads the latest data, updates the figure and plots it'''

        #Read the data to show from a file and store it
        with open('graph.json', 'r') as read_file:
            data = json.load(read_file)

        #clear previous data
        self.timestamp.clear()
        self.temperature.clear()
        self.humidity.clear()

        for index in data:
            self.timestamp.append(datetime.fromtimestamp(mktime(strptime(index['time_code'],'%Y-%m-%d %H:%M:%S'))))
            self.temperature.append(float(index['temperature']))
            self.humidity.append(float(index['humidity']))

        data = [self.temperature, self.humidity]

        #Clear the figure
        myfigure = plt.gcf()
        myfigure.clf()

        axes = myfigure.subplots(2,1, sharex=True)

        #Add the data to the axes and modify their axis
        for n in range(len(axes)):
            axes[n].plot_date(self.timestamp, data[n], self.ax_colors[n], xdate=True)             
            axes[n].set_ylabel(self.units[n])
            axes[n].set_title(self.titles[n])
            plt.ylim(min(data[n])-2,max(data[n])+2)
            axes[n].xaxis.set_minor_locator(dt.HourLocator(byhour=range(0,24,12)))   #show minor ticks with a step width of 12 hours
            axes[n].xaxis.set_minor_formatter(dt.DateFormatter('%H:%M'))
            axes[n].xaxis.set_major_locator(dt.DayLocator(bymonthday=range(0,31,1))) #show major ticks witha step widht of 1 day
            axes[n].xaxis.set_major_formatter(dt.DateFormatter('%d-%B'))
            axes[n].xaxis.set_tick_params(which='major', pad=15)                     #set spacing between major and minor labels

        #the axis labels for the first subplot are made invisible
        plt.setp(axes[0].get_xticklabels(which='both'), visible=False)

        #draw the figure
        myfigure.canvas.draw_idle()

class MyRootLayout(BoxLayout):
    pass

class MyWidgetApp(App):
    def build(self):
        return MyRootLayout()

if __name__ == '__main__':
    MyWidgetApp().run()
