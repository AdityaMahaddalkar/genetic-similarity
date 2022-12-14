import logging
import time

from ipop import IO
from util import DELTA, ALPHA, process_memory, PlottingData

LOGGING_LEVEL = logging.INFO

logging.basicConfig(
    level=LOGGING_LEVEL
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

            logging.debug(f'First string={first_gene_string}'
                          f'\tSecond string={second_gene_string}'
                          f'\tSimilarity={similarity}')
            logging.debug(plotting_data)

            logging.info(f'm+n={len(first_gene_string) + len(second_gene_string)}')
            logging.info(f'basic_time={plotting_data.time_required}\tmemory_consumed={plotting_data.memory_consumed}')

            self.io.write_to_output(name, similarity, new_string_1, new_string_2,
                                    plotting_data.time_required, plotting_data.memory_consumed, algorithm_type='basic')

            if benchmark:
                return

    @staticmethod
    def generate_new_strings_from(string_1, string_2, dp):
        reverse_of_new_string_1, reverse_of_new_string_2 = "", ""
        i, j = len(string_1), len(string_2)

        while i > 0 and j > 0:
            if dp[i - 1][j - 1] + ALPHA[frozenset({string_1[i - 1], string_2[j - 1]})] == dp[i][j]:
                reverse_of_new_string_1 += string_1[i - 1]
                reverse_of_new_string_2 += string_2[j - 1]
                i -= 1
                j -= 1
            elif dp[i - 1][j] + DELTA == dp[i][j]:
                reverse_of_new_string_1 += string_1[i - 1]
                reverse_of_new_string_2 += "_"
                i -= 1
            elif dp[i][j - 1] + DELTA == dp[i][j]:
                reverse_of_new_string_1 += "_"
                reverse_of_new_string_2 += string_2[j - 1]
                j -= 1
            else:
                raise Exception("Invalid matching condition")

        while i > 0:
            reverse_of_new_string_1 += string_1[i]
            reverse_of_new_string_2 += '_'
            i -= 1

        while j > 0:
            reverse_of_new_string_1 += '_'
            reverse_of_new_string_2 += string_2[j]
            j -= 1

        return reverse_of_new_string_1[::-1], reverse_of_new_string_2[::-1]

    def get_similarity(self, string_1, string_2):
        start_time = time.perf_counter_ns()

        dp = [[0 for _ in range(len(string_2) + 1)] for _ in range(len(string_1) + 1)]

        for i in range(1, len(string_1) + 1):
            dp[i][0] = i * DELTA

        for i in range(1, len(string_2) + 1):
            dp[0][i] = i * DELTA

        for i in range(1, len(string_1) + 1):
            for j in range(1, len(string_2) + 1):
                dp[i][j] = min(ALPHA[frozenset({string_1[i - 1], string_2[j - 1]})] + dp[i - 1][j - 1],
                               DELTA + dp[i - 1][j], DELTA + dp[i][j - 1])

        new_string_1, new_string_2 = self.generate_new_strings_from(string_1, string_2, dp)

        end_time = time.perf_counter_ns()
        time_in_ms = (end_time - start_time) / 10 ** 6
        memory_consumed = process_memory()
        similarity = dp[len(string_1)][len(string_2)]

        return similarity, new_string_1, new_string_2, PlottingData(len(string_1) + len(string_2), time_in_ms,
                                                                    memory_consumed)

    def sort_plotting_data_with_problem_size(self):
        self.plotting_data_list.sort(key=lambda x: x.problem_size)


if __name__ == '__main__':
    algorithm = Algorithm()
    algorithm.run()
