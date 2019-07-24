"""
Filename: accuracy.py
Date: 2019-07-24 12:46:35 AM
Author: David Oniani
E-mail: onianidavid@gmail.com

License:
    The code is licensed under GNU General Public License v3.0.
    Please read the LICENSE file in this distribution for details
    regarding the licensing of this code.

Description:
    Check the accuracy of predicted authorship attribution.
"""

import json


def main():
    """The main function"""
    # Get the data
    with open("./data/ground-truth.json") as file:
        ground_truth = json.load(file)["ground_truth"]

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
                {answers[number]["unknown_text"]: answers[number]["score"]}
            )
            hit += 1
        else:
            scores.append(
                {answers[number]["unknown_text"]: -answers[number]["score"]}
            )

    # Get the prediction accuracy
    prediction_accuracy = hit / len(answers) * 100

    # Get the prediction score
    prediction_score = 0
    for score in scores:
        prediction_score += list(score.values())[0]

    # Print out the results
    print(f"Prediction accuracy: {prediction_accuracy:.2f}%")
    print(f"Prediction score:    {prediction_score:.2f}")
    print(f"Number of samples:   {len(ground_truth)}")


if __name__ == "__main__":
    main()
