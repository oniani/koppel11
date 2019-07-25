"""
Filename: koppel11.py
Original Authors: Jakob Koehler and Tolga Buz

Rewritten and reformatted by David Oniani
Date: 2019-07-24 09:24:02 PM
E-mail: onianidavid@gmail.com

License:
    The code is licensed under GNU General Public License v3.0.
    Please read the LICENSE file in this distribution for details
    regarding the licensing of this code.

Description:
    This is an implementation/reproduction of the paper
    "Authorship attribution in the wild" by Moshe Koppel,
    Jonathan Schler, and Shlomo Argamon.

    For more information, see the paper: https://bit.ly/2K22ACM
"""

import math
import random
import argparse
import jsonhandler


# length of feature list
FEATURE_LENGTH = 20000

# Minimum size of doc (increases precision, decreases recall if many small docs)
MINLEN = 0

# Less than 500 words in the training data is not attributed
MINTRAINLEN = 500

# Size of n-gram
NGRAM_SIZE = 4

# Number of k-repetitions
REPETITIONS = 100

# Score threshold (needed for open set)
THRESHOLD = 0


def create_vector(string):
    """Creates a vector out of a string.

    Gets a string (e.g. Book), splits it into and
    returns a vector with all possible n-grams/features.
    """
    vec = {}
    words = string.split()

    for word in words:
        if len(word) <= NGRAM_SIZE:
            add(vec, word)
        else:
            for i in range(len(word) - NGRAM_SIZE + 1):
                add(vec, word[i : i + NGRAM_SIZE])

    return vec


def add(vector, ngram):
    """Adds n-grams to the vector.

    Adds n-grams to our featurelist-vector, if is
    not included yet (containing all possible
    n-grams/features).
    """
    if ngram in vector:
        vector[ngram] += 1
    else:
        vector[ngram] = 1


def select_features(vec):
    """Selects most frequent features.

    Selects the x most frequent n-grams/features
    (x=FEATURE_LENGTH) to avoid a (possibly) too
    big featurelist.
    """
    return sorted(vec, key=vec.get, reverse=True)[
        : min(len(vec), FEATURE_LENGTH)
    ]


def create_feature_map(string, features):
    """Creates a feature map.

    Creates feature map that only saves
    the features that actually appear more
    frequently than 0. Thus, the featurelis
    tneeds less memory and can work faster.
    """
    fmap = {}
    vec = create_vector(string)

    for ngram in features:
        if ngram in vec:
            fmap[ngram] = vec[ngram]

    return fmap


def cosine_similarity(vec_x, vec_y):
    """Calculates the cosine similary of two vectors.

    Calculates cosine similarity of two vectors vec_x and vec_y.
    Formula: cosine(X, Y) = (X * Y)/(|X|*|Y|)
    """
    sim_prod = 0.0
    len_x = 0
    len_y = 0

    for ngram in vec_x:
        len_x += vec_x[ngram] ** 2

    for ngram in vec_y:
        len_y += vec_y[ngram] ** 2

    len_x = math.sqrt(len_x)
    len_y = math.sqrt(len_y)

    for ngram in vec_x:
        if ngram in vec_y:
            sim_prod += vec_x[ngram] * vec_y[ngram]

    return sim_prod / (len_x * len_y)


def minmax(vec_x, vec_y):
    """Calculates the minmax similarity of two vectors.

    Calculates minmax similarity of two vectors vec_x and vec_y.
    Formula: minmax(X, Y) = sum(min(Xi, Yi))/sum(max(Xi, Yi))

    This baseline method will be used for further evaluation.
    """
    minsum = 0
    maxsum = 0

    for ngram in vec_x:
        if ngram in vec_y:
            # ngram is in both vectors
            minsum += min(vec_x[ngram], vec_y[ngram])
            maxsum += max(vec_x[ngram], vec_y[ngram])
        else:
            # ngram only in vec_x
            maxsum += vec_x[ngram]

    for ngram in vec_y:
        if ngram not in vec_x:
            # ngram only in vec_y
            maxsum += vec_y[ngram]

    if maxsum == 0:
        return 0

    return float(minsum) / maxsum


def training(string):
    """Returns a feature list of the vector from the string.

    Turns a given string into a n-gram vector
    and returns its feature list.
    """
    print("Training...")
    vec = create_vector(string)
    print("Selecting features...")
    feature_list = select_features(vec)
    print("Done!")
    return feature_list


def test_sim(vec_x, vec_y, feature_list, func):
    """Returns the similarity value of two vectors.

    Args: two vectors, a featurelist and func
    (to decide whether to use cosine or minmax similarity).

    Uses create_feature_map and cosine_similarity or minmax and
    returns the similarity value of the two vectors.
    """
    feature_map_x = create_feature_map(vec_x, feature_list)
    feature_map_y = create_feature_map(vec_y, feature_list)

    if func == 0:
        return cosine_similarity(feature_map_x, feature_map_y)

    return minmax(feature_map_x, feature_map_y)


def get_random_string(string, length):
    """Returns a random part of a string.

    Returns a random part of a string s
    that has a given length.
    """
    words = string.split()
    random_part = random.randint(0, len(words) - length)
    return "".join(words[random_part : random_part + length])


def main():
    """The main function."""
    parser = argparse.ArgumentParser(
        description="PPM approach according to Koppel11"
    )

    parser.add_argument("-i", action="store", help="path to corpus directory")
    parser.add_argument("-o", action="store", help="path to output directory")

    args = vars(parser.parse_args())

    corpusdir = args["i"]
    outputdir = args["o"]

    if corpusdir is None or outputdir is None:
        parser.print_help()
        return

    candidates = jsonhandler.candidates
    unknowns = jsonhandler.unknowns
    jsonhandler.loadJson(corpusdir)
    jsonhandler.loadTraining()

    texts = {}
    corpus = ""
    print("Loading texts for training...")
    deletes = []

    for cand in candidates:
        texts[cand] = ""
        for file in jsonhandler.trainings[cand]:
            texts[cand] += jsonhandler.getTrainingText(cand, file)
            print(f"Text {file} read")

        if len(texts[cand].split()) < MINTRAINLEN:
            del texts[cand]
            deletes.append(cand)
        else:
            corpus += texts[cand]

    newcands = []
    for cand in candidates:
        if cand not in deletes:
            newcands.append(cand)

    candidates = newcands
    words = [len(texts[cand].split()) for cand in texts]
    minwords = min(words)
    print(minwords)

    feature_list = training(corpus)
    authors = []
    scores = []

    for file in unknowns:
        print(f"Testing {file}")
        utext = jsonhandler.getUnknownText(file)
        ulen = len(utext.split())

        if ulen < MINLEN:
            authors.append("None")
            scores.append(0)
        else:
            wins = [0] * len(candidates)
            textlen = min(ulen, minwords)
            print(textlen)
            ustring = "".join(utext.split()[:textlen])

            for _ in range(REPETITIONS):
                rfl = random.sample(feature_list, len(feature_list) // 2)
                sims = []
                for cand in candidates:
                    candstring = get_random_string(texts[cand], textlen)
                    sims.append(test_sim(candstring, ustring, rfl, 1))
                wins[sims.index(max(sims))] += 1

            score = max(wins) / float(REPETITIONS)

            if score >= THRESHOLD:
                authors.append(candidates[wins.index(max(wins))])
                scores.append(score)
            else:
                authors.append("None")
                scores.append(score)

    print("Storing answers...")
    jsonhandler.storeJson(outputdir, unknowns, authors, scores)
    print("Done!")


if __name__ == "__main__":
    main()
