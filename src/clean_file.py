"""This script cleans Excel, Text, and CSV files by removing a list of bad characters.

When you first run this program it creates a GUI that accepts an input file, output 
folder, and filename. The main function will be called once you click on the
"Clean File" button. All other functions will be called from main.

The cleaned file will be exported to the output folder path designated by the user with
the file extension matching the input file's extension.

Lastly, a pop up message will show the total count of bad characters removed along with
the individual total character counts. The cleaned file will automatically open on your
desktop for review.
"""

import collections
import os
import re
from pathlib import Path

import numpy as np
import pandas as pd
import PySimpleGUI as sg


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
    file_extension = get_file_extension(input_file)
    # read input_file into a Pandas DataFrame
    df = check_file_type(input_file, file_extension)
    # if DataFrame is None then raise exception to user
    # telling them the desired file type
    if df is None:
        raise pd.errors.ParserError(
            "File type must be either Excel, Text as comma or tab delimited, or CSV."
        )
    else:
        # count bad characters and remove bad characters
        counter = count_bad_characters(df, bad_characters)
        df = remove_bad_characters(df, bad_characters)
        df = remove_null_values(df)
        df = strip_leading_and_trailing_chars(df)

        # create output path for exporting cleaned file
        output_path = construct_output_path(output_folder, filename)
        # export DataFrame to a file extension matching the intput file's extension
        output_dataframe(df, output_path, file_extension)

        # show stats of bad characters removed in pop-up message
        display_stats(counter)


def get_file_extension(input_file: os.PathLike) -> str:
    """Splits the file name and extracts the extension.

    Args:
        input_file (os.PathLike): Input file path received from user in the GUI.

    Returns:
        str: File extension.
    """
    return os.path.splitext(input_file)[1].lower()


def check_file_type(
    input_file: os.PathLike, file_extension: str
) -> pd.DataFrame | None:
    """Function for determining what type of file and delimiter is used.

    Args:
        input_file (os.PathLike): Input file path received from user in the GUI.

    Returns:
        pd.DataFrame | None: Dataframe is a 2D labeled data structure with columns.
        Or returns None if file cannot be parsed.
    """

    if file_extension in [".xlsx", ".xls"]:
        # Check if the file is Excel
        try:
            return pd.read_excel(input_file)
        except pd.errors.ParserError:
            pass
    elif file_extension in [".txt", ".csv"]:
        # Check if file is txt or csv
        try:
            return pd.read_csv(input_file, sep=",")
        except pd.errors.ParserError:
            pass
        try:
            return pd.read_csv(input_file, sep="\t")
        except pd.errors.ParserError:
            pass
    else:
        # If none of the checks succeed, return None
        return None


def count_bad_characters(
    df: pd.DataFrame, bad_characters: list[str] = [",", '"', '""', "'"]
) -> dict[str, int]:
    """Count the total amount of bad characters and their occurrences in the DataFrame.

    Args:
        df (pd.DataFrame): 2D labeled data structure with columns.
        bad_characters (list[str]): List of special characters that needs to be removed.
        Defaults to [",", '"', '""', "'"].

    Returns:
        dict[str, int]: Dictionary count of total bad characters
        and total count of each individual character.
    """

    counter = collections.Counter()
    for column in df.columns:
        for char in bad_characters:
            count = df[column].astype(str).str.count(re.escape(char)).sum()
            counter[char] += count
    return counter


def remove_bad_characters(
    df: pd.DataFrame, bad_characters: list[str] = [",", '"', '""', "'"]
) -> pd.DataFrame:
    """Removes bad characters from the Dataframe.

    Args:
        df (pd.DataFrame): 2D labeled data structure with columns.
        bad_characters (list[str]): List of special characters that needs to be removed.
        Defaults to [",", '"', '""', "'"].

    Returns:
        pd.DataFrame: 2D labeled data structure with columns.
    """

    for column in df.columns:
        for char in bad_characters:
            df[column] = df[column].astype(str).str.replace(re.escape(char), "")
    return df


def remove_null_values(df: pd.DataFrame) -> pd.DataFrame:
    """Removes NaN and NaT values from the Dataframe.

    Args:
        df (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: 2D labeled data structure with columns.
    """

    # replace nan and NaT values with np.nan
    df.replace(["nan", "NaT"], np.nan, inplace=True)
    # replace np.nan values with an empty character
    df.fillna("", inplace=True)
    return df


def strip_leading_and_trailing_chars(df: pd.DataFrame) -> pd.DataFrame:
    """Removes all leading and trailing characters from DataFrame.

    Args:
        df (pd.DataFrame): 2D labeled data structure with columns.

    Returns:
        pd.DataFrame: 2D labeled data structure with columns.
    """

    for column in df.columns:
        df[column] = df[column].astype(str).str.strip()
    return df


def construct_output_path(output_folder: os.PathLike, filename: str) -> os.PathLike:
    """Constructs a path object of output file path.

    Args:
        output_folder (os.PathLike): Destination folder path received from user
        in the GUI.
        filename (str): New filename for cleaned file.

    Returns:
        os.pathlike: Output file path combining the output folder path and
        new filename. No extension included.
    """

    return Path(output_folder, filename)


def output_dataframe(
    df: pd.DataFrame, output_path: os.PathLike, file_extension: str
) -> None:
    """Output the dataframe to the file extension matching the input file's extension.

    Args:
        df (pd.DataFrame): 2D labeled data structure with columns.
        output_path (os.PathLike): Output file path combining the output folder path and
        new filename. No extension included.
        file_extension (str): File extension of the input file.
    """

    if file_extension in [".xlsx", ".xls"]:
        # Output to Excel file
        df.to_excel(output_path.with_suffix(".xlsx"), index=False)
        # double click file to open on desktop
        os.startfile(output_path.with_suffix(".xlsx"))
    elif file_extension in [".txt", ".csv"]:
        # Output to text file
        df.to_csv(output_path.with_suffix(".txt"), index=False, sep="\t")
        # double click file to open on desktop
        os.startfile(output_path.with_suffix(".txt"))
    else:
        print(f"Unsupported file type: {file_extension}")


def display_stats(counter: dict[str, int]) -> None:
    """Create pop up message with stats of total bad characters
    and individual character counts.

    Args:
        counter (dict[str, int]): Dictionary count of total bad characters
        and total count of each individual character.
    """

    message = f"Total count of bad characters: {sum(counter.values())}\n\n"
    message += "Individual character counts:\n"
    for char, count in counter.items():
        message += f"Character '{char}': {count}\n"
    sg.popup_no_titlebar(message)


def is_valid_path(filepath: os.PathLike) -> bool:
    """Validate path from user exists

    Args:
        filepath (os.PathLike): Valid filepath.

    Returns:
        bool: True or False.
    """

    if filepath and Path(filepath).exists():
        return True
    sg.popup_error("Filepath not correct")
    return False


def gui() -> None:
    """Function to create GUI and call main function."""

    sg.theme("DarkBlue3")  # Add a touch of color
    # All the stuff inside your window.
    layout = [
        [
            sg.Text("Input File: "),
            sg.Input(key="-IN-"),
            sg.FileBrowse(),
        ],
        [sg.Text("Output Folder: "), sg.Input(key="-OUT-"), sg.FolderBrowse()],
        [sg.Text("New Filename: "), sg.Input(key="-FILENAME-")],
        [sg.Exit(), sg.Button("Clean File")],
    ]

    # Create the Window
    window = sg.Window("Clean File", layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if (
            event == sg.WIN_CLOSED or event == "Cancel"
        ):  # if user closes window or clicks cancel
            break
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == "Clean File":  # button for running main function
            if (is_valid_path(values["-IN-"])) and (is_valid_path(values["-OUT-"])):
                main(
                    input_file=values["-IN-"],
                    output_folder=values["-OUT-"],
                    filename=values["-FILENAME-"],
                )
    window.close()


if __name__ == "__main__":
    gui()
