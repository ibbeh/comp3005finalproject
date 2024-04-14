import os
import sys

def delete_unlisted_json_files(csv_file_path, json_files_directory):
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            all_match_ids = file.read().strip().split(',')

        for filename in os.listdir(json_files_directory):
            if filename.endswith('.json'):
                match_id = filename.split('.')[0]

                if match_id not in all_match_ids:
                    os.remove(os.path.join(json_files_directory, filename))
                    print(f"Deleted {filename}")

        print("Cleanup complete.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python deleteMatches.py <path_to_allMatches.csv> <path_to_json_files_directory>")
        sys.exit(1)

    csv_file_path = sys.argv[1]
    json_files_directory = sys.argv[2]

    delete_unlisted_json_files(csv_file_path, json_files_directory)
