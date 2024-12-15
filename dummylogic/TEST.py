import os
import csv
import json
from difflib import unified_diff


class FileProcessor:
    """
    A utility class for file comparison and data extraction based on file format.
    """

    def __init__(self, file_format):
        self.file_format = file_format

    @staticmethod
    def get_file_format(predefined_choice=None):
        """Determine the file format based on user input."""
        if predefined_choice:
            choice = predefined_choice
        else:
            print("Select file format:")
            print("1. CSV")
            print("2. JSON")
            print("3. Plain Text")
            choice = input("Enter choice (1/2/3): ").strip()

        formats = {'1': 'csv', '2': 'json', '3': 'text'}
        return formats.get(choice, FileProcessor.get_file_format(predefined_choice))

    @staticmethod
    def highlight_differences(text1, text2):
        """Highlight differences between two texts word by word."""
        words1 = text1.split()
        words2 = text2.split()

        highlighted = []
        for w1, w2 in zip(words1, words2):
            if w1 != w2:
                highlighted.append(f"{{{w1}/{w2}}}")
            else:
                highlighted.append(w1)

        # Handle remaining words if lengths differ
        highlighted.extend(words1[len(words2):]) if len(words1) > len(words2) else highlighted.extend(
            words2[len(words1):])

        return ' '.join(highlighted)

    def compare_files(self, file1, file2, output_file):
        """Compare two files and write the differences to an output file."""
        differences = []

        if self.file_format == 'csv':
            with open(file1, 'r') as f1, open(file2, 'r') as f2:
                reader1 = list(csv.reader(f1))
                reader2 = list(csv.reader(f2))
                for row1, row2 in zip(reader1, reader2):
                    differences.append(','.join(self.highlight_differences(a, b) for a, b in zip(row1, row2)))

        elif self.file_format == 'json':
            with open(file1, 'r') as f1, open(file2, 'r') as f2:
                data1 = json.load(f1)
                data2 = json.load(f2)

                diff = unified_diff(
                    json.dumps(data1, indent=2).splitlines(),
                    json.dumps(data2, indent=2).splitlines(),
                    fromfile=file1,
                    tofile=file2,
                )
                differences = list(diff)

        elif self.file_format == 'text':
            with open(file1, 'r') as f1, open(file2, 'r') as f2:
                lines1 = f1.readlines()
                lines2 = f2.readlines()
                for line1, line2 in zip(lines1, lines2):
                    differences.append(self.highlight_differences(line1.strip(), line2.strip()))

        with open(output_file, 'w') as output:
            output.write(f"Comparing files:\n{file1}\n{file2}\n\n")
            output.write('\n'.join(differences))
        print(f"Differences written to {output_file}")

    def extract_data(self, big_file, input_file, output_file):
        """Extract data from a larger file based on input data."""
        if self.file_format == 'csv':
            with open(big_file, 'r') as bf, open(input_file, 'r') as inf, open(output_file, 'w') as out:
                big_reader = list(csv.reader(bf))
                input_reader = list(csv.reader(inf))

                input_keys = {tuple(row) for row in input_reader}
                extracted_rows = [row for row in big_reader if tuple(row) in input_keys]

                writer = csv.writer(out)
                writer.writerows(extracted_rows)

        elif self.file_format == 'json':
            with open(big_file, 'r') as bf, open(input_file, 'r') as inf, open(output_file, 'w') as out:
                big_data = json.load(bf)
                input_data = json.load(inf)

                extracted_data = [item for item in big_data if item in input_data]
                json.dump(extracted_data, out, indent=2)

        elif self.file_format == 'text':
            with open(big_file, 'r') as bf, open(input_file, 'r') as inf, open(output_file, 'w') as out:
                big_lines = set(bf.readlines())
                input_lines = set(inf.readlines())
                extracted_lines = big_lines & input_lines
                out.writelines(extracted_lines)

        print(f"Extracted data written to {output_file}")


class FileComparisonTool:
    """
    Main class to manage user input and execute operations.
    """

    def __init__(self, predefined_choices=None):
        self.predefined_choices = predefined_choices or {}
        self.file_processor = None

    def run(self):
        file_format = FileProcessor.get_file_format(self.predefined_choices.get('file_format'))
        self.file_processor = FileProcessor(file_format)

        operation = self.predefined_choices.get('operation')
        if not operation:
            print("\nChoose operation:")
            print("1. Compare two files")
            print("2. Extract data from a larger file")
            operation = input("Enter choice (1/2): ").strip()

        if operation == '1':
            self.compare_files()
        elif operation == '2':
            self.extract_data()
        else:
            print("Invalid operation choice. Exiting.")

    def compare_files(self):
        file1 = self.predefined_choices.get('file1') or input("Enter path to first file: ").strip()
        file2 = self.predefined_choices.get('file2') or input("Enter path to second file: ").strip()
        output_file = self.predefined_choices.get('output_file') or input("Enter path for output file: ").strip()

        self.file_processor.compare_files(file1, file2, output_file)

    def extract_data(self):
        big_file = self.predefined_choices.get('big_file') or input("Enter path to the larger file: ").strip()
        input_file = self.predefined_choices.get('input_file') or input("Enter path to the input file: ").strip()
        output_file = self.predefined_choices.get('output_file') or input("Enter path for output file: ").strip()

        self.file_processor.extract_data(big_file, input_file, output_file)


if __name__ == "__main__":
    tool = FileComparisonTool()
    tool.run()
