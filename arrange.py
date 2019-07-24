"""
Filename: arrange.py
Date: 2019-07-23 07:03:14 PM
Author: David Oniani
E-mail: onianidavid@gmail.com

License:
    The code is licensed under GNU General Public License v3.0.
    Please read the LICENSE file in this distribution for details
    regarding the licensing of this code.

Description:
    Arrange Ad Text from CSV text in 3 folders.
"""

import json
import os
import random
import shutil

import pandas as pd


def main() -> None:
    """The main function."""
    # Remove 'data' directory if it exists
    if os.path.isdir("./data"):
        shutil.rmtree("./data")

    # Make directories
    os.mkdir("./data")
    os.chdir("./data")

    os.mkdir("./candidate2015")
    os.mkdir("./candidate2016")
    os.mkdir("./candidate2017")
    os.mkdir("./unknown")
    os.mkdir("./unknown_list")
    os.mkdir("./unknown_list/candidate2015")
    os.mkdir("./unknown_list/candidate2016")
    os.mkdir("./unknown_list/candidate2017")

    # Read CSV files
    year_2015 = pd.read_csv(
        "../by-year/year-2015.csv", na_filter=False, thousands=","
    )
    year_2016 = pd.read_csv(
        "../by-year/year-2016.csv", na_filter=False, thousands=","
    )
    year_2017 = pd.read_csv(
        "../by-year/year-2017.csv", na_filter=False, thousands=","
    )

    # Get the data
    ad_text_2015 = year_2015["Ad Text"]
    ad_text_2016 = year_2016["Ad Text"]
    ad_text_2017 = year_2017["Ad Text"]

    # Write the data
    # There will be 500 per category since there are 618 in 2015
    for index, text in enumerate(ad_text_2015):
        if index > 499:
            with open(
                os.path.join(
                    "./unknown_list/candidate2015", f"unknown{index - 500}.txt"
                ),
                "w",
            ) as file:
                file.write(f"{text}\n")
        else:
            with open(
                os.path.join("./candidate2015", f"known{index}.txt"), "w"
            ) as file:
                file.write(f"{text}\n")

    for index, text in enumerate(ad_text_2016):
        if index > 499:
            with open(
                os.path.join(
                    "./unknown_list/candidate2016", f"unknown{index - 500}.txt"
                ),
                "w",
            ) as file:
                file.write(f"{text}\n")
        else:
            with open(
                os.path.join("./candidate2016", f"known{index}.txt"), "w"
            ) as file:
                file.write(f"{text}\n")

    for index, text in enumerate(ad_text_2017):
        if index > 499:
            with open(
                os.path.join(
                    "./unknown_list/candidate2017", f"unknown{index - 500}.txt"
                ),
                "w",
            ) as file:
                file.write(f"{text}\n")
        else:
            with open(
                os.path.join("./candidate2017", f"known{index}.txt"), "w"
            ) as file:
                file.write(f"{text}\n")

    # Randomized copying for testing
    ground_truth = []

    for j in range(10):
        shutil.copy(
            f"./unknown_list/candidate2015/unknown{j}.txt", "./unknown"
        )
        ground_truth.append(
            {"unknown-text": f"unknown{j}.txt", "true-author": "candidate2015"}
        )

    for j in range(10, 20):
        shutil.copy(
            f"./unknown_list/candidate2016/unknown{j}.txt", "./unknown"
        )
        ground_truth.append(
            {"unknown-text": f"unknown{j}.txt", "true-author": "candidate2016"}
        )

    for j in range(20, 30):
        shutil.copy(
            f"./unknown_list/candidate2017/unknown{j}.txt", "./unknown"
        )
        ground_truth.append(
            {"unknown-text": f"unknown{j}.txt", "true-author": "candidate2017"}
        )

    os.chdir("..")
    with open("ground-truth.json", "w") as file:
        json.dump({"ground_truth": ground_truth}, file, indent=2)
        file.write("\n")


if __name__ == "__main__":
    main()
