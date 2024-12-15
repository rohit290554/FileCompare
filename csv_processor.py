import csv
from base_processor import FileProcessor


class CSVProcessor(FileProcessor):
    """Processor for CSV file operations."""

    def compare(self, file1, file2):
        differences = []
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            reader1 = list(csv.reader(f1))
            reader2 = list(csv.reader(f2))
            for row1, row2 in zip(reader1, reader2):
                differences.append(','.join(self.highlight_differences(a, b) for a, b in zip(row1, row2)))
        return differences

    def extract(self, big_file, input_file):
        with open(big_file, 'r') as bf, open(input_file, 'r') as inf:
            big_reader = list(csv.reader(bf))
            input_reader = list(csv.reader(inf))
            input_keys = {tuple(row) for row in input_reader}
            return [row for row in big_reader if tuple(row) in input_keys]
