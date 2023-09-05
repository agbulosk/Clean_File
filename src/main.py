"""This script cleans Excel, Text, and CSV files by removing a list of bad characters.

The clean_file.py and GUI.py modules are imported to this main file. The clean_file.py
contains function definitions that carry out the cleaning process. The GUI.py module
creates the graphical user interface which calls the main function in main.py.

When you first run this program it creates a GUI that accepts an input file, output 
folder, and filename. The main function will be called once you click on the
"Clean File" button. All other functions will be called from main.

The cleaned file will be exported to the output folder path designated by the user with
the file extension matching the input file's extension.

Lastly, a pop-up message will show the total count of bad characters removed along with
the individual total character counts. The cleaned file will automatically open on your
desktop for review.
"""

import os

import GUI
import clean_file as cf


def main(input_file: os.PathLike, output_folder: os.PathLike, filename: str) -> None:
    """Main function for calling methods from the CleanFile class in clean_file module.
    Also calls the gui method from the GUI module.

    Args:
        input_file (os.PathLike): Input file path received from user in the GUI.
        output_folder (os.PathLike): Destination folder path received from user
        in the GUI.
        filename (str): New filename for cleaned file.
    """

    # Create a CleanFile instance and perform the cleaning
    file = cf.CleanFile(input_file)
    clean_df, counter = file.clean_df()

    # export cleaned DataFrame and display stats in pop-up window
    output_path = file.construct_output_path(output_folder, filename)
    file.output_dataframe(clean_df, output_path)
    file.display_stats(counter)


if __name__ == "__main__":
    # calling the GUI function will call the main function once the user clicks the "Clean File" button
    GUI.gui()
