import json
from difflib import unified_diff
from base_processor import FileProcessor


class JSONProcessor(FileProcessor):
    """Processor for JSON file operations."""

    def compare(self, file1, file2):
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)
            return list(unified_diff(
                json.dumps(data1, indent=2).splitlines(),
                json.dumps(data2, indent=2).splitlines(),
                fromfile=file1,
                tofile=file2
            ))

    def extract(self, big_file, input_file):
        with open(big_file, 'r') as bf, open(input_file, 'r') as inf:
            big_data = json.load(bf)
            input_data = json.load(inf)
            return [item for item in big_data if item in input_data]
