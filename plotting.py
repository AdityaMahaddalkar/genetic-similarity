# import matplotlib.pyplot as plt
import os.path

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from util import PlottingData

IMAGE_FOLDER = 'images'


class Plot:
    def __init__(self, plotting_data_list):
        self.problem_sizes = PlottingData.get_all_problem_sizes(plotting_data_list)
        self.time_consumed = PlottingData.get_all_time_values(plotting_data_list)
        self.memory_consumed = PlottingData.get_all_memory_consumed(plotting_data_list)

    def plot(self, type_of_algorithm='basic'):
        fig = make_subplots(rows=1, cols=2,
                            x_title='Size of the Problem')

        fig.add_trace(
            go.Scatter(x=self.problem_sizes, y=self.time_consumed),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(x=self.problem_sizes, y=self.memory_consumed),
            row=1, col=2
        )

        fig['layout']['yaxis']['title'] = 'Time Consumed (in ms)'
        fig['layout']['yaxis2']['title'] = 'Memory Consumed (in KB)'

        fig.update_layout(height=1080, width=1920, title_text='Basic Implementation of Similarity Finding Algorithm')

        fig.write_image(os.path.join(IMAGE_FOLDER, type_of_algorithm + '.png'))
