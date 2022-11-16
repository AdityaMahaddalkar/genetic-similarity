import efficient


def test_sample():
    algorithm = efficient.Algorithm()

    for name, file_path in algorithm.io.generate_sample(file_type='input'):
        first_gene_string, second_gene_string = algorithm.io.transform_file_content_to_input(file_path)

        similarity, new_string_1, new_string_2, _ = algorithm.get_similarity(first_gene_string,
                                                                             second_gene_string)

        sample_output_file_path = file_path.replace('input', 'output')

        with open(sample_output_file_path, 'r') as infile:
            lines = infile.readlines()
            lines = list(map(lambda x: x.strip(), lines))

            expected_similarity = int(lines[0])
            expected_first_string = lines[1]
            expected_second_string = lines[2]

            assert similarity == expected_similarity
            assert new_string_1 == expected_first_string
            assert new_string_2 == expected_second_string
