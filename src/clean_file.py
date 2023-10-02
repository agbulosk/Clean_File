"""This module contains functions to clean files.

Module is imported into the main.py file where functions will be called
from the main function."""

import collections
import os
import re
import string
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
import PySimpleGUI as sg


class CleanFile:
    def __init__(self, input_file: os.PathLike) -> None:
        self.input_file = input_file
        self.bad_characters = [",", '"', '""', "'"]
        self.bad_special_characters = ["\n", "\r", "\t", "\x0b", "\x0c"]

    def clean_df(self) -> Tuple[pd.DataFrame, dict[str, int]]:
        """
        Main function for cleaning individual Excel or txt or csv files.

        Calls all other functions.

        Only accepts Excel files (.xls, .xlsx) or Text files (.txt)
        that are comma or tab delimited or CSV files (.csv)

        Raises:
            pd.errors.ParserError: Unaccepted file extension.

        Returns:
            Tuple of Dataframe, Dictionary of count of bad characters.
        """

        # get file extension and load input file into Pandas DataFrame
        file_extension = self.get_file_extension(self.input_file)
        df = self.load_dataframe(self.input_file, file_extension)

        # Raise exception if incorrect File Type was used
        if df is None:
            raise pd.errors.ParserError(
                "File type must be either Excel, Text as comma or tab delimited, or CSV."
            )

        # count bad characters and remove bad characters
        counter = self.count_bad_characters(
            df, self.bad_characters, self.bad_special_characters
        )
        df = self.remove_bad_characters(df, self.bad_characters)
        df = self.remove_null_values(df)
        df = self.strip_leading_and_trailing_chars(df)
        df = self.remove_special_characters_from_df(df, self.bad_special_characters)
        return df, counter

    def get_file_extension(self, input_file: os.PathLike) -> str:
        """Splits the file name and extracts the extension.

        Args:
            input_file (os.PathLike): Input file path received from user in the GUI.

        Returns:
            str: File extension.
        """
        return Path(input_file).suffix.lower()

    def load_dataframe(
        self, input_file: os.PathLike, file_extension: str
    ) -> pd.DataFrame | None:
        """Loads the input file into a Pandas DataFrame.

        Args:
            input_file (os.PathLike): Input file path received from user in the GUI.
            file_extension (str): File extension of the input file.
        Returns:
            pd.DataFrame | None: Dataframe is a 2D-labeled data structure with columns.
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
        self,
        df: pd.DataFrame,
        bad_characters: list[str] = [",", '"', '""', "'"],
        bad_special_characters: list[str] = ["\n", "\r", "\t", "\x0b", "\x0c"],
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
        all_bad_characters = bad_characters + bad_special_characters
        for column in df.columns:
            for char in all_bad_characters:
                if char in bad_special_characters:
                    count = df[column].astype(str).str.count(re.escape(char)).sum()
                    counter[rf"{char!r}"] += count
                else:
                    count = df[column].astype(str).str.count(re.escape(char)).sum()
                    counter[re.escape(char)] += count
        return counter

    def remove_bad_characters(
        self, df: pd.DataFrame, bad_characters: list[str] = [",", '"', '""', "'"]
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

    def remove_null_values(self, df: pd.DataFrame) -> pd.DataFrame:
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

    def strip_leading_and_trailing_chars(self, df: pd.DataFrame) -> pd.DataFrame:
        """Removes all leading and trailing characters from DataFrame.

        Args:
            df (pd.DataFrame): 2D labeled data structure with columns.

        Returns:
            pd.DataFrame: 2D labeled data structure with columns.
        """

        for column in df.columns:
            df[column] = df[column].astype(str).str.strip()
        return df

    def remove_special_characters(
        self,
        text: pd.DataFrame.columns,
        bad_special_characters,
    ) -> str:
        """
        Function for removing non-printable characters and other bad special characters. For use in the
        remove_special_characters_from_df function.

        Args:
            text: The values from each column will be passed into this argument.
            bad_special_characters: ["\n", "\r", "\t", "\x0b", "\x0c"]

        Returns: Cleaned text.
        """

        printable_chars = set(string.printable)
        pattern = "[" + re.escape("".join(bad_special_characters)) + "]"
        cleaned_text = re.sub(
            pattern, "", "".join(char for char in text if char in printable_chars)
        )
        return cleaned_text

    def remove_special_characters_from_df(
        self,
        df: pd.DataFrame,
        bad_special_characters: list[str] = ["\n", "\r", "\t", "\x0b", "\x0c"],
    ) -> pd.DataFrame:
        """
        Removes all bad special characters by using the remove_special_characters function.

        Args:
            df: Pandas DataFrame.
            bad_special_characters: ["\n", "\r", "\t", "\x0b", "\x0c"]

        Returns: Pandas Dataframe.
        """

        df = df.applymap(
            lambda x: self.remove_special_characters(x, bad_special_characters)
        )
        return df

    def construct_output_path(self, output_folder: os.PathLike, filename: str) -> Path:
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

    def output_dataframe(self, df: pd.DataFrame, output_path: Path) -> None:
        """Output the dataframe to the file extension matching the input file's extension.

        Args:
            df (pd.DataFrame): 2D labeled data structure with columns.
            output_path (os.PathLike): Output file path combining the output folder path and
            new filename. No extension included.
        """

        file_extension = self.get_file_extension(self.input_file)
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

    def display_stats(self, counter: dict[str, int]) -> None:
        """Create pop up message with stats of total bad characters
        and individual character counts.

        Args:
            counter (dict[str, int]): Dictionary count of total bad characters
            and total count of each individual character.
        """

        message = f"Total count of bad characters: {sum(counter.values())}\n\n"
        message += "Individual character counts:\n"
        for char, count in counter.items():
            message += rf"Character '{char!r}': {count}" + "\n"
        sg.popup_no_titlebar(message)
