from file_tool import FileComparisonTool


def main():
    file_format = input("Select file format (csv/json/text): ").strip()
    tool = FileComparisonTool(file_format)

    operation = input("Choose operation: 1. Compare 2. Extract: ").strip()
    if operation == '1':
        file1 = input("Enter path to the first file: ").strip()
        file2 = input("Enter path to the second file: ").strip()
        output_file = input("Enter output file path: ").strip()
        tool.compare_files(file1, file2, output_file)
    elif operation == '2':
        big_file = input("Enter path to the larger file: ").strip()
        input_file = input("Enter path to the input file: ").strip()
        output_file = input("Enter output file path: ").strip()
        tool.extract_data(big_file, input_file, output_file)


if __name__ == "__main__":
    main()
