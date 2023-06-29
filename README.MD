<!-- ABOUT THE PROJECT -->
## About The Project

This project is meant to clean customer files of bad characters including commas, single double quotes, double double quotes, apostrophes, and leading and trailing characters. Files must have the following extensions: Excel file (.xls, .xlsx), Text files (.txt), and CSV files (.csv). If it's a text file it must be comma or tab delimited.

### Built With

* Python

<!-- GETTING STARTED -->
## Getting Started

1. Download the clean_file.py and requirements.txt files to a project folder.
2. When you run clean_file.py, a GUI will come up where you can select the individual file you want to clean, an output folder, and a new filename.
3. Once the program is complete, you will get a pop-up message confirming the cleaning process is done and the file will open on your desktop for your review.
4. Stats of total bad characters and individual character counts will display to show how many characters were removed from the file.

Files:
* clean.py - Main python file that contains the source code.
* requirements.txt - Contains a list of libraries and their versions which you will need installed to run this program. You might be prompted to upgrade these modules so follow the instructions in your terminal window accordingly.

### Installation

Install the required libraries to run this script by running this command ```pip install -r requirements.txt``` in your IDE's terminal window.