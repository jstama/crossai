import os
import json
import re


def extract_csv_info(filename):
    # Define the regex pattern to capture all
    # occurrences of the pattern "label_start_end"
    pattern = (
        r'(01a|01b|01c|01d|02a|02b|02c|03a|03b|03c|null|null_plus|rest)_'
        r'(\d+)_(\d+)'
    )

    # Use re.findall to find all matches
    matches = re.findall(pattern, filename)

    if matches:
        # Process all matches
        data = []
        for label, start, end in matches:
            start, end = int(start), int(end)
            if start < end:  # To ensure valid ranges
                data.append({
                    "label": label,
                    "type": "samples",
                    "start": start,
                    "end": end
                })
        return data
    else:
        print(f"Pattern not found in filename: {filename}")
        return None


def convert_csv_to_json(csv_path):
    if os.path.isdir(csv_path):
        # Iterate over each class directory
        for class_dir in os.listdir(csv_path):
            class_path = os.path.join(csv_path, class_dir)
            if os.path.isdir(class_path):
                # List files in each class directory
                for file in os.listdir(class_path):
                    if file.endswith(".csv"):
                        json_data = extract_csv_info(file)
                        json_filename = os.path.splitext(file)[0] + ".json"
                        json_path = os.path.join(class_path, json_filename)

                        try:
                            with open(json_path, 'w') as json_file:
                                json.dump(json_data, json_file, indent=4)
                        except Exception as e:
                            print(f"Error processing file {file}: {e}")

        print("Conversion completed successfully.")

    elif os.path.isfile(csv_path) and csv_path.endswith(".csv"):
        # Convert a single CSV file
        json_data = extract_csv_info(os.path.basename(csv_path))
        json_filename = os.path.splitext(
            os.path.basename(csv_path)
            )[0] + ".json"
        json_path = os.path.join(os.path.dirname(csv_path), json_filename)

        try:
            with open(json_path, 'w') as json_file:
                json.dump(json_data, json_file, indent=4)
            print("Converted single file successfully.")
        except Exception as e:
            print(f"Error processing file {csv_path}: {e}")

    else:
        print("Invalid input. Provide a valid directory or CSV file path.")
