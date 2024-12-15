from csv_processor import CSVProcessor
from json_processor import JSONProcessor
from text_processor import TextProcessor


class FileComparisonTool:
    """Main class to manage file operations."""

    def __init__(self, file_format):
        processors = {'csv': CSVProcessor, 'json': JSONProcessor, 'text': TextProcessor}
        self.processor = processors[file_format]()

    def compare_files(self, file1, file2, output_file):
        differences = self.processor.compare(file1, file2)
        with open(output_file, 'w') as output:
            output.write(f"Comparing files:\n{file1}\n{file2}\n\n")
            output.write('\n'.join(differences))

    def extract_data(self, big_file, input_file, output_file):
        extracted_data = self.processor.extract(big_file, input_file)
        with open(output_file, 'w') as output:
            if isinstance(extracted_data, set):
                output.writelines(extracted_data)
            else:
                output.writelines('\n'.join(map(str, extracted_data)))
