"""
Filename: arrange.py
Date: 2019-07-25 10:16:28 PM
Author: David Oniani
E-mail: onianidavid@gmail.com

License:
    The code is licensed under GNU General Public License v3.0.
    Please read the LICENSE file in this distribution for details
    regarding the licensing of this code.

Description:
    Generate data and meta files for koppel11 authorship
    attribution algorithm.
"""


import json
import os
import shutil

from typing import List
from pandas import read_csv


# Constants
DATA_2015 = "../by-year/year-2015.csv"
DATA_2016 = "../by-year/year-2016.csv"
DATA_2017 = "../by-year/year-2017.csv"

FILENAME_2015 = "candidate2015"
FILENAME_2016 = "candidate2016"
FILENAME_2017 = "candidate2017"


def dottify(textlist: List[str]) -> List[str]:
    """Add dot at the end of the entries.

    Put the dot at the end of every
    Facebook post text if there is
    not one already.

    NOTE: This is done in-place.
    """
    for index, text in enumerate(textlist):
        if text == "":
            pass
        elif text[-1] != ".":
            textlist[index] += ". "


def normalize(textlist: List[str]) -> List[str]:
    """Normalize the text.

    Each file should have a text-length
    of 500 words. This is important as
    the paper demonstrated the highest
    accuracy with this constraint.

    NOTE: Words have to be comprised
          of alphanumeric characters only.
    """
    textlist = [
        "".join(filter(lambda x: x.isalpha() or x == " ", text))
        for text in textlist
    ]

    normalized = []
    acc = ""
    for text in textlist:
        if len(text.split()) >= 500:
            normalized.append(text)
        else:
            acc += f" {text}"
            if len(acc.split()) >= 500:
                normalized.append(acc)
                acc = ""

    return normalized


def write_organized(
    textlist: List[str], directory: str, prefix: str, known: bool = True
) -> None:
    """Write text to files.

    Generate text chunks for the training.
    Each text chunk must have at least 500
    characters.
    """
    ground_truth = []
    unknown_texts = []

    if known:
        for index, text in enumerate(textlist):
            with open(
                os.path.join(directory, f"{prefix}-known{index}.txt"), "w"
            ) as file:
                file.write(f"{text}\n")
    else:
        for index, text in enumerate(textlist):
            with open(
                os.path.join(directory, f"{prefix}-unknown{index}.txt"), "w"
            ) as file:
                file.write(f"{text}\n")

            ground_truth.append(
                {
                    "unknown-text": f"{prefix}-unknown{index}.txt",
                    "true-author": "candidate2017",
                }
            )

            unknown_texts.append(
                {"unknown-text": f"{prefix}-unknown{index}.txt"}
            )

        os.rename(directory, "unknown")

        with open("meta-file.json", "w") as file:
            json.dump(
                {
                    "folder": "unknown",
                    "language": "EN",
                    "encoding": "UTF8",
                    "candidate-authors": [
                        {"author-name": "candidate2015"},
                        {"author-name": "candidate2016"},
                        {"author-name": "candidate2017"},
                    ],
                    "unknown-texts": unknown_texts,
                },
                file,
                indent=2,
            )
            file.write("\n")

        with open("ground-truth.json", "w") as file:
            json.dump({"ground-truth": ground_truth}, file, indent=2)
            file.write("\n")


def main() -> None:
    """The main function."""
    # Remove 'data' directory if it exists
    print("Removing previously created directories if they exist...")
    if os.path.isdir("./data"):
        shutil.rmtree("./data")
    print("Done!")

    # Make directories
    print("Making directories...")
    os.mkdir("./data")
    os.chdir("./data")

    os.mkdir(FILENAME_2015)
    os.mkdir(FILENAME_2016)
    os.mkdir(FILENAME_2017)
    print("Done!")

    # Read CSV files
    print("Reading CSV files...")
    year_2015 = read_csv(DATA_2015, na_filter=False, thousands=",")
    year_2016 = read_csv(DATA_2016, na_filter=False, thousands=",")
    year_2017 = read_csv(DATA_2017, na_filter=False, thousands=",")
    print("Done!")

    # Get the data and randomize it
    print("Getting out the text data and randomizing it...")
    ad_text_2015 = year_2015["Ad Text"].sample(frac=1)
    ad_text_2016 = year_2016["Ad Text"].sample(frac=1)
    ad_text_2017 = year_2017["Ad Text"].sample(frac=1)
    print("Done!")

    # Add dots
    print("Adding dots...")
    dottify(ad_text_2015)
    dottify(ad_text_2016)
    dottify(ad_text_2017)
    print("Done!")

    # Normalize
    print("Normalizing the dataset...")
    normalized_2015 = normalize(ad_text_2015)
    normalized_2016 = normalize(ad_text_2016)
    normalized_2017 = normalize(ad_text_2017)
    print("Done!")

    # Write
    print("Creating new files, writing the data, and generating meta files...")
    write_organized(normalized_2015, FILENAME_2015, prefix="2015")
    write_organized(normalized_2016, FILENAME_2016, prefix="2016")
    write_organized(normalized_2017, FILENAME_2017, prefix="2017", known=False)
    print("Done!")


if __name__ == "__main__":
    main()
