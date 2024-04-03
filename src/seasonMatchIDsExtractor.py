"""
seasonMatchIDsExtractor.py

Usage:
    python seasonMatchIDsExtractor.py <inputJsonFile> <outputFile>

This script takes an input JSON file representing a football season, extracts the competition ID, season ID, season name,
and match IDs, then writes these data to an output text file. The output file will contain the competition ID on the first line,
the season ID on the second line, the season name on the third line, and all match IDs separated by commas on the fourth line.
"""

import json
import sys

def extractMatchIDsFromSeason(jsonFilePath, outputFilePath):
    try:
        #Load the JSON data from the file
        with open(jsonFilePath, 'r', encoding='utf-8') as file:
            season_data = json.load(file) #season_data is a list of dictionaries reprsenting the json data for a season

        #Extract necessary information
        competition_id = season_data[0]['competition']['competition_id']
        competition_name = season_data[0]['competition']['competition_name']
        season_id = season_data[0]['season']['season_id']
        season_name = season_data[0]['season']['season_name']
        match_ids = [str(match['match_id']) for match in season_data]

        #Write the extracted data to the output file
        with open(outputFilePath, 'w', encoding='utf-8') as file:
            file.write(f"{competition_id}\n") #Write competition ID
            file.write(f"{competition_name}\n") #Write competition name
            file.write(f"{season_id}\n") #Write season ID
            file.write(f"{season_name}\n") #Write season name
            file.write(",".join(match_ids)) #Write match IDs, separated by commas

        print(f"Data extracted successfully to {outputFilePath}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    #Ensure correct usage
    if len(sys.argv) != 3:
        print("Usage: python seasonMatchIDsExtractor.py <input_json_file> <output_file>")
        sys.exit(1)

    inputJsonFile = sys.argv[1] #The first argument is the input JSON file path
    outputTextFile = sys.argv[2] #The second argument is the output file path

    #Call the function with the provided arguments
    extractMatchIDsFromSeason(inputJsonFile, outputTextFile)

