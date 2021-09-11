# encoding: utf-8

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import matplotlib.dates as dt
from datetime import datetime
from time import mktime, strptime
import os

class TwoPlotsSharedXWidget(FigureCanvasKivyAgg):
    '''Displays two datetimeplots with shared x-axis.

        Attributes:
        The attributes are bound by name to propertis in the kv file. Updating them will automatically update the displayed data in the visualisation
            sourceX (ListProperty):
                list of datetime values for the timeseries
            sourceY (ListProperty):
                list holding two lists of values corresponding with timestamp
            units (ObjectProperty, str):
                list of string. Holding the units of the y-axis.
                Initially set to --.
            titles (ObjectProperty, str):
                list of string. Holding the titles for the plots.
                Initially set to --.
            ax_colors (ObjectProperty, str):
                List, setting the color of the plot.
                Initially set to green.
                Other parameters to change to different colors can be found in the matplotib documentation https://matplotlib.org/2.1.1/api/_as_gen/matplotlib.pyplot.plot.html
            notification  (StringProperty, str):
                Error string. Shows exceptions, like no data available.
                Initially set to --.
    '''

    plt.style.use('dark_background')

    sourceX = ListProperty([])
    sourceY = ListProperty([])
    units = ObjectProperty(['--','--'])
    titles = ObjectProperty(['--','--'])
    ax_colors = ObjectProperty(['g','g'])
    notification = StringProperty('')
    formatter = StringProperty('')
    
    def __init__(self, **kwargs):
        '''__init__ takes the figure the backend is going to work with'''
        super(TwoPlotsSharedXWidget, self).__init__(plt.figure(), **kwargs)
        
    def update_plot(self, *args, **kwargs):
        '''
        reads the latest data, updates the figure and plots it.
        
        Args:
            *args (): not used. For further development.
            **kwargs (): not used. For further development.

        Returns:
            Nothing.
        '''

        #Clear the figure
        myfigure = self.figure
        myfigure.clf()

        axes = myfigure.subplots(2,1, sharex=True)

        #Add the data to the axes and modify their axis
        for n in range(len(axes)):
            if self.sourceY[n]:
                axes[n].plot_date(self.sourceX, self.sourceY[n], self.ax_colors[n], xdate=True)
                axes[n].set_ylabel(self.units[n])
                axes[n].set_title(self.titles[n])
                plt.ylim(min(self.sourceY[n])-2,max(self.sourceY[n])+2)
                axes[n].xaxis.set_major_locator(dt.MonthLocator(bymonth=range(1,13))) #show major ticks with a step width of 1 month
                axes[n].xaxis.set_major_formatter(dt.DateFormatter(self.formatter))

        #the axis labels for the first subplot are made invisible
        plt.setp(axes[0].get_xticklabels(which='both'), visible=False)

        #draw the figure
        myfigure.canvas.draw_idle()

class MyRootLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyRootLayout, self).__init__(**kwargs)

class TwoPlotsSharedXWidgetApp(App):
    def build(self):
        return MyRootLayout()

if __name__ == '__main__':
    TwoPlotsSharedXWidgetApp().run()
