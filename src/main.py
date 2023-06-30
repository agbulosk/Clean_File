"""This script cleans Excel, Text, and CSV files by removing a list of bad characters.

The clean_file.py and GUI.py modules are imported to this main file. The clean_file.py
contains function definitions that carry out the cleaning process. The GUI.py module
creates the graphical user interface which calls the main function in main.py.

When you first run this program it creates a GUI that accepts an input file, output 
folder, and filename. The main function will be called once you click on the
"Clean File" button. All other functions will be called from main.

The cleaned file will be exported to the output folder path designated by the user with
the file extension matching the input file's extension.

Lastly, a pop up message will show the total count of bad characters removed along with
the individual total character counts. The cleaned file will automatically open on your
desktop for review.
"""

import os

import GUI
import pandas as pd

import clean_file as cf


def main(input_file: os.PathLike, output_folder: os.PathLike, filename: str) -> None:
    """Main function for cleaning individual Excel or txt or csv files.

    Calls all other functions.

    Only accepts Excel files (.xls, .xlsx) or Text files (.txt)
    that are comma or tab delimited or CSV files (.csv)

    Args:
        input_file (os.PathLike): Input file path received from user in the GUI.
        output_folder (os.PathLike): Destination folder path received from user
        in the GUI.
        filename (str): New filename for cleaned file.

    Raises:
        pd.errors.ParserError: File extension must be (.xls, .xlsx, .txt, .csv).
        Text files must be comma or tab delimited.
    """

    # list of common bad characters that cause issues for Extract, Transform, Load (ETL)
    bad_characters = [",", '"', '""', "'"]
    # Extract file extension
    file_extension = cf.get_file_extension(input_file)
    # read input_file into a Pandas DataFrame
    df = cf.load_dataframe(input_file, file_extension)
    # if DataFrame is None then raise exception to user
    # telling them the desired file type
    if df is None:
        raise pd.errors.ParserError(
            "File type must be either Excel, Text as comma or tab delimited, or CSV."
        )
    else:
        # count bad characters and remove bad characters
        counter = cf.count_bad_characters(df, bad_characters)
        df = cf.remove_bad_characters(df, bad_characters)
        df = cf.remove_null_values(df)
        df = cf.strip_leading_and_trailing_chars(df)

        # create output path for exporting cleaned file
        output_path = cf.construct_output_path(output_folder, filename)
        # export DataFrame to a file extension matching the intput file's extension
        cf.output_dataframe(df, output_path, file_extension)

        # show stats of bad characters removed in pop-up message
        cf.display_stats(counter)


if __name__ == "__main__":
    # calling the GUI function will call the main function
    # once the user clicks the "Clean File" button
    GUI.gui()
