"""This module creates the GUI.

This module is meant to be imported into the main.py file. The gui function 
will be called from the main.py file."""


import os
from pathlib import Path

import main as m
import PySimpleGUI as sg


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
                m.main(
                    input_file=values["-IN-"],
                    output_folder=values["-OUT-"],
                    filename=values["-FILENAME-"],
                )
    window.close()


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


if __name__ == "__main__":
    gui()
