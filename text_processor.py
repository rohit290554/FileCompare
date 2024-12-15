from base_processor import FileProcessor

class TextProcessor(FileProcessor):
    """Processor for text file operations."""

    def compare(self, file1, file2):
        differences = []
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()
            for line1, line2 in zip(lines1, lines2):
                differences.append(self.highlight_differences(line1.strip(), line2.strip()))
        return differences

    def extract(self, big_file, input_file):
        with open(big_file, 'r') as bf, open(input_file, 'r') as inf:
            big_lines = set(bf.readlines())
            input_lines = set(inf.readlines())
            return big_lines & input_lines
