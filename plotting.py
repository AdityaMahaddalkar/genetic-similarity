# import matplotlib.pyplot as plt
import os.path

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import basic
import efficient
from util import PlottingData

IMAGE_FOLDER = 'images'
BENCHMARK = False


class Plot:
    def __init__(self, basic_plotting_data_list, efficient_plotting_data_list):
        self.problem_sizes = PlottingData.get_all_problem_sizes(basic_plotting_data_list)
        self.basic_time_consumed = PlottingData.get_all_time_values(basic_plotting_data_list)
        self.basic_memory_consumed = PlottingData.get_all_memory_consumed(basic_plotting_data_list)

        self.efficient_time_consumed = PlottingData.get_all_time_values(efficient_plotting_data_list)
        self.efficient_memory_consumed = PlottingData.get_all_memory_consumed(efficient_plotting_data_list)

    def plot(self, plot_name='plot'):
        fig = make_subplots(rows=1, cols=2,
                            x_title='Size of the Problem')

        line = {
            'shape': 'spline',
            'smoothing': 1.0,
        }

        fig.add_trace(
            go.Scatter(x=self.problem_sizes, y=self.basic_time_consumed,
                       name='Time Consumed for Basic Algorithm',
                       line=line),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(x=self.problem_sizes, y=self.efficient_time_consumed,
                       name='Time Consumed for Efficient Algorithm',
                       line=line),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(x=self.problem_sizes, y=self.basic_memory_consumed,
                       name='Memory Consumed for Basic Algorithm',
                       line=line),
            row=1, col=2
        )

        fig.add_trace(
            go.Scatter(x=self.problem_sizes, y=self.efficient_memory_consumed,
                       name='Memory Consumed for Efficient Algorithm',
                       line=line),
            row=1, col=2
        )

        fig['layout']['yaxis']['title'] = 'Time Consumed (in ms)'
        fig['layout']['yaxis2']['title'] = 'Memory Consumed (in KB)'

        fig.update_layout(height=1080 / 1.5, width=1920 / 1.2,
                          title_text='Basic vs Efficient Sequence Alignment Algorithms',
                          title_font_size=18,
                          font_family='Helvetica')

        fig.write_image(os.path.join(IMAGE_FOLDER, plot_name + '.png'))
        fig.write_image(os.path.join(IMAGE_FOLDER, plot_name + '.svg'))

        fig.show()

    def plot_time_vs_problem_size(self):
        fig = go.Figure()

        line = {
            'shape': 'spline',
            'smoothing': 1.0,
        }

        fig.add_trace(
            go.Scatter(x=self.problem_sizes, y=self.basic_time_consumed,
                       name='Time Consumed for Basic Algorithm',
                       line=line),
        )

        fig.add_trace(
            go.Scatter(x=self.problem_sizes, y=self.efficient_time_consumed,
                       name='Time Consumed for Efficient Algorithm',
                       line=line),
        )

        fig.update_layout(height=1080 / 1.5, width=1920 / 1.5,
                          title_text='Basic vs Efficient Time Consumed',
                          title_font_size=18,
                          font_family='Helvetica',
                          yaxis_title='Time Consumed (in milliseconds)',
                          xaxis_title='Problem Size')

        fig.write_image(os.path.join(IMAGE_FOLDER, 'time_vs_problem_size.png'))

    def plot_memory_vs_problem_size(self):
        fig = go.Figure()

        line = {
            'shape': 'spline',
            'smoothing': 1.0,
        }

        fig.add_trace(
            go.Scatter(x=self.problem_sizes, y=self.basic_memory_consumed,
                       name='Memory Consumed for Basic Algorithm',
                       line=line),

        )

        fig.add_trace(
            go.Scatter(x=self.problem_sizes, y=self.efficient_memory_consumed,
                       name='Memory Consumed for Efficient Algorithm',
                       line=line),

        )

        fig.update_layout(height=1080 / 1.5, width=1920 / 1.5,
                          title_text='Basic vs Efficient Memory Consumed',
                          title_font_size=18,
                          font_family='Helvetica',
                          yaxis_title='Memory Consumed (in bytes)',
                          xaxis_title='Problem Size')

        fig.write_image(os.path.join(IMAGE_FOLDER, 'memory_vs_problem_size.png'))


if __name__ == '__main__':
    basic_algorithm = basic.Algorithm()
    efficient_algorithm = efficient.Algorithm()

    basic_algorithm.run(benchmark=BENCHMARK)
    efficient_algorithm.run(benchmark=BENCHMARK)

    basic_algorithm.sort_plotting_data_with_problem_size()
    efficient_algorithm.sort_plotting_data_with_problem_size()

    plot = Plot(basic_algorithm.plotting_data_list, efficient_algorithm.plotting_data_list)
    plot.plot()

    plot.plot_time_vs_problem_size()
    plot.plot_memory_vs_problem_size()
