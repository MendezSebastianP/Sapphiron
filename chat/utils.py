import pandas as pd
import numpy as np
import os

from django.conf import settings

scores = {
    1: 450,
    2: 120,
    3: 890,
    4: 345,
    5: 760,
    6: 230,
    7: 980,
    8: 540,
    9: 670,
    10: 310
}


def score_to_prob(scores):
    """
    Converts a dictionary of scores into probabilities by normalizing the values.

    Args:
        scores (dict): Dictionary with keys as IDs and values as scores.

    Returns:
        dict: Dictionary with keys as IDs and values as probabilities.
    """
    prob = {}
    sum_scores = sum(scores.values())
    for key, value in scores.items():
        prob[key] = value / sum_scores
    return (prob)


def next_verb(scores):
    """
    Simulates verb selection based on scores and plots results against the original scores.

    Args:
        scores (dict): Dictionary with keys as IDs and values as scores.
        n (int): Number of simulation iterations.

    Returns:
        None
    """
    prob = score_to_prob(scores)
    verb_choose = np.random.choice(list(prob.keys()), p=list(prob.values()))
    return (verb_choose)


def next_random_verb(df: pd.DataFrame) -> str:
    """
    Returns a random verb from the list of 1000 verbs.

    Returns:
        str: Random verb.
    """
    verb_sample = df.sample(1).iloc[0]
    verb_es = verb_sample['ES']
    verb_fr = verb_sample['FR']
    return f'El verbo es: {verb_es} y en francés es: {verb_fr}'


def get_csv_response(user_message):
    csv_path = os.path.join(settings.BASE_DIR, 'chat', 'data', '1000verbs.csv')
    response = None

    df = pd.read_csv(csv_path)

    response = next_random_verb(df)

    if not response:
        response = "No matching response found."
    return response