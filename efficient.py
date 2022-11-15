import logging
import time

from ipop import IO
from util import DELTA, ALPHA, process_memory, PlottingData

LOG_LEVEL = logging.DEBUG

logging.basicConfig(
    level=LOG_LEVEL
)


class Algorithm:
    def __init__(self):
        self.io = IO()
        self.plotting_data_list = []

    def run(self, benchmark=False):
        for name, file_path in self.io.generate_input_file_paths():
            first_gene_string, second_gene_string = self.io.transform_file_content_to_input(file_path)
            similarity, new_string_1, new_string_2, plotting_data = self.get_similarity(first_gene_string,
                                                                                        second_gene_string)
            self.plotting_data_list.append(plotting_data)

            logging.debug(f'Similarity={similarity}')
            logging.debug(f'Plotting data={plotting_data}')

            if benchmark:
                break

    def get_similarity(self, first_gene_string, second_gene_string):
        start_time = time.perf_counter_ns()

        dp = [[0 for _ in range(2)] for _ in range(len(first_gene_string) + 1)]

        for i in range(len(first_gene_string) + 1):
            dp[i][0] = i * DELTA

        for j in range(1, len(second_gene_string) + 1):
            dp[0][1] = j * DELTA
            for i in range(1, len(first_gene_string) + 1):
                dp[i][1] = min(
                    ALPHA[frozenset({first_gene_string[i - 1], second_gene_string[j - 1]})] + dp[i - 1][0],
                    DELTA + dp[i - 1][1],
                    DELTA + dp[i][0]
                )

            for i in range(1, len(first_gene_string) + 1):
                dp[i][0] = dp[i][1]

        end_time = time.perf_counter_ns()
        memory_consumed = process_memory()
        time_in_ms = (end_time - start_time) / 10 ** 6

        return dp[len(first_gene_string)][1], None, None, PlottingData(len(first_gene_string), time_in_ms,
                                                                       memory_consumed)

    def sort_plotting_data_with_problem_size(self):
        self.plotting_data_list.sort(key=lambda x: x.problem_size)


if __name__ == '__main__':
    algorithm = Algorithm()
    algorithm.run()
