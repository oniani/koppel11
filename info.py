"""
Filename: info.py
Date: 2019-07-24 12:46:35 AM
Author: David Oniani
E-mail: onianidavid@gmail.com

License:
    The code is licensed under GNU General Public License v3.0.
    Please read the LICENSE file in this distribution for details
    regarding the licensing of this code.

Description:
    Get the basic statistics.
"""

import json
import os


def main():
    """The main function"""
    # Get the data
    with open("./data/ground-truth.json") as file:
        ground_truth = json.load(file)["ground-truth"]

    with open("./results/answers.json") as file:
        answers = json.load(file)["answers"]

    # Make sure they are of the same size
    assert len(answers) == len(ground_truth)

    # Get the scores
    scores = []
    hit = 0
    for number, _ in enumerate(answers):
        if answers[number]["author"] == ground_truth[number]["true-author"]:
            scores.append(
                {answers[number]["unknown_text"]: 2 * answers[number]["score"]}
            )
            hit += 1
        else:
            scores.append(
                {answers[number]["unknown_text"]: answers[number]["score"]}
            )

    # Get the number of samples
    testing_samples = len(ground_truth)
    training_samples = len(os.listdir("./data/candidate2015")) + len(
        os.listdir("./data/candidate2016")
    )

    # Get the prediction accuracy
    prediction_accuracy = hit / testing_samples * 100

    # Get the prediction score
    prediction_score = 0
    for score in scores:
        prediction_score += list(score.values())[0]
    prediction_accuracy_average = prediction_score / testing_samples * 100
    prediction_score *= 10 / (3 * testing_samples)

    # Print out the results
    print(f"Number of testing samples:     {testing_samples}")
    print(f"Number of training samples:    {training_samples}")
    print(f"Prediction accuracy (average): {prediction_accuracy_average}")
    print(f"Prediction accuracy:           {prediction_accuracy:.2f}%")
    print(f"Prediction score:              {prediction_score:.2f}/10")


if __name__ == "__main__":
    main()
