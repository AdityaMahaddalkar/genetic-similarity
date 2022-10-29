import psutil

DELTA = 30
ALPHA = {
    frozenset({"A", "A"}): 0, frozenset({"C", "C"}): 0,
    frozenset({"G", "G"}): 0, frozenset({"T", "T"}): 0,
    frozenset({"A", "C"}): 110, frozenset({"A", "G"}): 48, frozenset({"A", "T"}): 94,
    frozenset({"C", "G"}): 118, frozenset({"C", "T"}): 48, frozenset({"G", "T"}): 110
}


def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed


class PlottingData:
    def __init__(self, problem_size, time_required, memory_consumed):
        self.problem_size = problem_size
        self.time_required = time_required
        self.memory_consumed = memory_consumed

    @staticmethod
    def get_all_problem_sizes(plotting_data_list):
        return [plotting_data.problem_size for plotting_data in plotting_data_list]

    @staticmethod
    def get_all_time_values(plotting_data_list):
        return [plotting_data.time_required for plotting_data in plotting_data_list]

    @staticmethod
    def get_all_memory_consumed(plotting_data_list):
        return [plotting_data.memory_consumed for plotting_data in plotting_data_list]

    def __str__(self):
        return f'Problem size={self.problem_size}\tTime={self.time_required} ms\tMemory={self.memory_consumed} kb'

    def __repr__(self):
        return f'Problem size={self.problem_size}\tTime={self.time_required} ms\tMemory={self.memory_consumed} kb'
