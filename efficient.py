import copy
import logging
import time

from ipop import IO
from util import DELTA, ALPHA, PlottingData, process_memory

INFINITY = 10000000000

LOG_LEVEL = logging.INFO

logging.basicConfig(
    level=LOG_LEVEL
)

GLOBAL_MEMORY_ARRAY = []


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

            logging.info(f'm+n={len(first_gene_string) + len(second_gene_string)}')
            logging.info(
                f'efficient_time={plotting_data.time_required}\tmemory_consumed={plotting_data.memory_consumed}')

            self.io.write_to_output(
                name, similarity, new_string_1, new_string_2,
                plotting_data.time_required, plotting_data.memory_consumed,
                algorithm_type='efficient'
            )

            if benchmark:
                break

    def get_similarity(self, first_gene_string, second_gene_string):

        global GLOBAL_MEMORY_ARRAY

        start_time = time.perf_counter_ns()

        first_alignment, second_alignment = Algorithm.dnc(first_gene_string, second_gene_string)

        similarity = Algorithm.calculate_similarity_score(first_alignment, second_alignment)
        logging.debug(f'{first_alignment}\t{second_alignment}')

        end_time = time.perf_counter_ns()
        memory_consumed = max(GLOBAL_MEMORY_ARRAY)
        time_in_ms = (end_time - start_time) / 10 ** 6

        return similarity, first_alignment, second_alignment, PlottingData(
            len(first_gene_string) + len(second_gene_string), time_in_ms,
            memory_consumed)

    @staticmethod
    def dnc(first_gene_string: str, second_gene_string: str):
        first_alignment, second_alignment = '', ''

        if len(first_gene_string) == 0:
            first_alignment = '_' * len(second_gene_string)
            second_alignment = copy.deepcopy(second_gene_string)
        elif len(second_gene_string) == 0:
            first_alignment = copy.deepcopy(first_gene_string)
            second_alignment = '_' * len(first_gene_string)
        elif len(first_gene_string) == 1 or len(second_gene_string) == 1:
            first_alignment, second_alignment = Algorithm.nw(first_gene_string, second_gene_string)
        else:
            first_mid = round(len(first_gene_string) / 2)
            left_score = Algorithm.nw_score(first_gene_string[:first_mid], second_gene_string)
            right_score = Algorithm.nw_score(first_gene_string[first_mid:][::-1],
                                             second_gene_string[::-1])[::-1]

            min_till_now = INFINITY
            min_index = -1
            for index, (ls, rs) in enumerate(zip(left_score, right_score)):
                if ls + rs < min_till_now:
                    min_index = index
                    min_till_now = ls + rs

            left_pair = Algorithm.dnc(first_gene_string[:first_mid],
                                      second_gene_string[:min_index])
            right_pair = Algorithm.dnc(first_gene_string[first_mid:],
                                       second_gene_string[min_index:])

            first_alignment, second_alignment = left_pair[0] + right_pair[0], left_pair[1] + right_pair[1]

        return first_alignment, second_alignment

    @staticmethod
    def nw(first_gene_string, second_gene_string):
        global GLOBAL_MEMORY_ARRAY

        GLOBAL_MEMORY_ARRAY.append(process_memory())

        dp = [[0 for _ in range(len(second_gene_string) + 1)] for _ in range(len(first_gene_string) + 1)]

        for i in range(len(first_gene_string) + 1):
            for j in range(len(second_gene_string) + 1):

                if i == 0:
                    dp[i][j] = DELTA * j
                elif j == 0:
                    dp[i][j] = DELTA * i
                else:
                    dp[i][j] = min(
                        ALPHA[frozenset({first_gene_string[i - 1], second_gene_string[j - 1]})] + dp[i - 1][j - 1],
                        DELTA + dp[i - 1][j],
                        DELTA + dp[i][j - 1]
                    )

        first_string_after_alignment, second_string_after_alignment = Algorithm.get_alignment(first_gene_string,
                                                                                              second_gene_string, dp)

        return first_string_after_alignment, second_string_after_alignment

    def sort_plotting_data_with_problem_size(self):
        self.plotting_data_list.sort(key=lambda x: x.problem_size)

    @classmethod
    def get_alignment(cls, first_gene_string, second_gene_string, dp):
        i, j = len(first_gene_string), len(second_gene_string)
        reversed_first_alignment, reversed_second_alignment = '', ''

        while i > 0 and j > 0:
            if dp[i][j] == ALPHA[frozenset({first_gene_string[i - 1], second_gene_string[j - 1]})] + dp[i - 1][j - 1]:
                reversed_first_alignment += first_gene_string[i - 1]
                reversed_second_alignment += second_gene_string[j - 1]
                i -= 1
                j -= 1
            elif dp[i][j] == DELTA + dp[i][j - 1]:
                reversed_first_alignment += '_'
                reversed_second_alignment += second_gene_string[j - 1]
                j -= 1
            elif dp[i][j] == DELTA + dp[i - 1][j]:
                reversed_first_alignment += first_gene_string[i - 1]
                reversed_second_alignment += '_'
                i -= 1
            else:
                raise Exception("Invalid matching condition")

        while i > 0:
            reversed_first_alignment += first_gene_string[i - 1]
            reversed_second_alignment += '_'
            i -= 1

        while j > 0:
            reversed_first_alignment += '_'
            reversed_second_alignment += second_gene_string[j - 1]
            j -= 1

        return reversed_first_alignment[::-1], reversed_second_alignment[::-1]

    @classmethod
    def nw_score(cls, first_gene_string, second_gene_string):
        even_edits, odd_edits = [DELTA * i for i in range(len(second_gene_string) + 1)], \
                                [0 for _ in range(len(second_gene_string) + 1)]

        current_edits, previous_edits = [], []

        for i in range(1, len(first_gene_string) + 1):
            if i % 2 == 0:
                current_edits = even_edits
                previous_edits = odd_edits
            else:
                current_edits = odd_edits
                previous_edits = even_edits

            current_edits[0] = DELTA * i

            for j in range(1, len(second_gene_string) + 1):
                current_edits[j] = min(
                    ALPHA[frozenset({first_gene_string[i - 1], second_gene_string[j - 1]})] + previous_edits[j - 1],
                    DELTA + current_edits[j - 1],
                    DELTA + previous_edits[j]
                )

        return even_edits if len(first_gene_string) % 2 == 0 else odd_edits

    @classmethod
    def calculate_similarity_score(cls, first_alignment, second_alignment):
        similarity = 0
        assert len(first_alignment) == len(second_alignment)
        for i in range(len(first_alignment)):
            if first_alignment[i] == '_' or second_alignment[i] == '_':
                similarity += DELTA
            else:
                similarity += ALPHA[frozenset({first_alignment[i], second_alignment[i]})]
        return similarity


if __name__ == '__main__':
    algorithm = Algorithm()
    algorithm.run()
