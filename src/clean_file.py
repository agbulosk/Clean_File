"""This module contains functions to clean files.

Module is imported into the main.py file where functions will be called
from the main function."""

import collections
import os
import re
from pathlib import Path

import numpy as np
import pandas as pd
import PySimpleGUI as sg


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


def output_dataframe(df: pd.DataFrame, output_path: Path, file_extension: str) -> None:
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
