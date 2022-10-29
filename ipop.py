import os

RESOURCES = "resources"
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
SAMPLE = "sample"


class IO:
    def __init__(self):
        assert os.path.exists(os.path.join(RESOURCES,
                                           INPUT_FOLDER)), "Input folder not found. Please make sure input folder " \
                                                           "exists in ./resources/input "

        self.input_path = os.path.join(RESOURCES, INPUT_FOLDER)
        self.output_path = os.path.join(RESOURCES, OUTPUT_FOLDER)

        if not os.path.isdir(self.output_path):
            os.mkdir(self.output_path)

    def generate_input_file_paths(self):
        file_names = next(os.walk(self.input_path))[-1]
        for name in file_names:
            yield name, os.path.join(self.input_path, name)

    def write_to_output(self, infile_name: str, similarity, new_string_1, new_string_2, time_in_ms, size_in_kb):
        outfile_name = infile_name.replace("in", "out")
        outfile_path = os.path.join(self.output_path, outfile_name)
        with open(outfile_path, 'w') as outfile:
            outfile.write(f'{similarity}\n')
            outfile.write(f'{new_string_1}\n')
            outfile.write(f'{new_string_2}\n')
            outfile.write(f'{time_in_ms}\n')
            outfile.write(f'{size_in_kb}\n')

    @staticmethod
    def transform_file_content_to_input(file_path):
        with open(file_path, 'r') as infile:
            lines = infile.readlines()
            lines = [line.strip() for line in lines]

            first_gene_string = lines[0]

            last_line_of_index_for_first_string = 0
            for line in lines[1:]:
                if line.isalpha():
                    break
                last_line_of_index_for_first_string += 1

            second_gene_string = lines[last_line_of_index_for_first_string + 1]

            for i in range(1, last_line_of_index_for_first_string + 1):
                index = int(lines[i])
                first_gene_string = first_gene_string[:index + 1] + first_gene_string + first_gene_string[index + 1:]

            for i in range(last_line_of_index_for_first_string + 2, len(lines)):
                index = int(lines[i])
                second_gene_string = second_gene_string[:index + 1] + second_gene_string + second_gene_string[
                                                                                           index + 1:]

            return first_gene_string, second_gene_string
