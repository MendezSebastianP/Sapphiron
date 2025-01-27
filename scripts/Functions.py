from typing import Dict, Union
import copy
import numpy as np
import matplotlib.pyplot as plt
import random

INITIAL_VALUES = {'score': 1000, 'streak': 0, 'right_count': 0, 'wrong_count': 0}
INITIAL_N_VERBS = 10

base_scores = {id:INITIAL_VALUES.copy() for id in range(1, INITIAL_N_VERBS + 1)}


def score_to_prob(scores: Dict[int, Dict[str, Union[float, int]]]) -> Dict[int, float]:
    """
    Converts a dictionary of scores into normalized probabilities.

    Args:
        scores (Dict): A dictionary where each key has an inner dictionary with 'score'.

    Returns:
        Dict: A dictionary with probabilities as values.
    """
    
    total_score = sum(item['score'] for item in scores.values())
    return {key: value['score'] / total_score for key, value in scores.items()}


def next_verb(scores: Dict[int, Dict[str, Union[float, int]]]) -> np.int64:
    """
    Chooses the next verb based on probability derived from scores.

    Args:
        scores (Dict): A dictionary of scores.

    Returns:
        int: The selected verb key.
    """
    prob = score_to_prob(scores)
    return np.random.choice(list(prob.keys()), p=list(prob.values()))



def simulation_plot_verb(scores: Dict[int, Dict[str, Union[float, int]]], n: int) -> None:
    """
    Simulates verb selection and plots the results.

    Args:
        scores (Dict): A dictionary of scores.
        n (int): Number of iterations in the simulation.

    Returns:
        None
    """
    count_selections = {key: 0 for key in scores}  # Initialize counts

    # Simulate verb selection
    for _ in range(n):
        verb_choose = next_verb(scores)
        count_selections[verb_choose] += 1

    # Create plot
    plt.figure(figsize=(12, 6))

    # Plot simulation results
    plt.subplot(1, 2, 1)
    plt.bar(
        count_selections.keys(),
        count_selections.values(),
        edgecolor='black',
        color='skyblue',
        alpha=0.7
    )
    plt.title("Simulation Results")
    plt.xlabel("Verb Key")
    plt.ylabel("Selection Count")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Plot real probabilities
    probabilities = score_to_prob(scores)
    plt.subplot(1, 2, 2)
    plt.bar(
        probabilities.keys(),
        probabilities.values(),
        edgecolor='black',
        color='orange',
        alpha=0.7
    )
    plt.title("Real Probabilities")
    plt.xlabel("Verb Key")
    plt.ylabel("Probability")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()


def verbs_session(scores: Dict[int, Dict[str, Union[float, int]]], n: int) -> list:
    """
    Selects a set number of verbs for a training session.

    Args:
        scores (Dict): A dictionary of scores.
        n (int): Number of verbs to select.

    Returns:
        list: A list of selected verb keys.
    """
    temp_scores = copy.deepcopy(scores)
    selected_verbs = []
    for _ in range(n):
        verb_choose = next_verb(temp_scores)
        selected_verbs.append(verb_choose)
        del temp_scores[verb_choose]
    return selected_verbs


def right_answer(score: float, streak: int) -> float:
    """
    Adjusts the score for a correct answer, considering the current streak.

    Args:
        score (float): The current score.
        streak (int): The current streak count.

    Returns:
        float: The adjusted score.
    """
    return score * (0.7 ** streak)


def wrong_answer(score: float, rank: int, n: int = 1000) -> float:
    """
    Adjusts the score for an incorrect answer, considering rank.

    Args:
        score (float): The current score.
        rank (int): The rank of the verb.
        n (int): Total number of verbs (default is 1000).

    Returns:
        float: The adjusted score.
    """
    a1 = 1.2 + ((n - rank + 1) / (n - 1))
    return score * a1


def next_level_check(scores: Dict[int, Dict[str, Union[float, int]]], level_treshhold: float = 0.6) -> bool:
    next_level_counter = sum(1 for value in scores.values() if value['score'] <= 700)
    if next_level_counter / len(scores.keys()) >= level_treshhold:
        return True
    else: 
        return False
        

def update_verbs(scores: Dict[int, Dict[str, Union[float, int]]], verb_unlock: int = 3) -> Dict[int, Dict[str, Union[float, int]]]:
    if next_level_check(scores):
        last_verb = max(scores.keys())
        for _ in range(verb_unlock):
            last_verb += 1
            scores[last_verb] = INITIAL_VALUES.copy()
    return None


def test_session(
    base_scores: Dict[int, Dict[str, Union[float, int]]],
    plot: bool = False,
    tries: int = 10,
    accuracy: float = 1,
) -> Dict[int, Dict[str, Union[float, int]]]:
    """
    Simulates a test session with adjustable parameters.

    Args:
        scores (Dict): A dictionary of scores.
        plot (bool): verb scores bar plot
        tries (int): Number of tries in the session.
        accuracy (float): The user's accuracy rate.
        verb_unlock (int): Number of new verbs unlocked after a session.

    Returns:
        Dict: Updated dictionary of scores.
    """
    scores = copy.deepcopy(base_scores)
    for _ in range(tries):
        verb = next_verb(scores)
        if random.random() < accuracy:
            scores[verb]['streak'] += 1
            scores[verb]['right_count'] += 1
            scores[verb]['score'] = right_answer(scores[verb]['score'], scores[verb]['streak'])
            update_verbs(scores)
        else:
            scores[verb]['streak'] = 0
            scores[verb]['wrong_count'] += 1
            scores[verb]['score'] = wrong_answer(scores[verb]['score'], rank=verb)

    if plot is True:
        results_iter = [values['score']for values in scores.values()]
        plt.bar(scores.keys(), results_iter)
        plt.xticks(ticks=range(1,len(scores.keys())))
        plt.title('Verb results - Histogram')
        plt.xlabel('Verb Range')
        plt.ylabel('Score')
        plt.show()

    return scores


def test_session_simulation(
    n: int,
    base_scores: Dict[int, Dict[str, Union[float, int]]],
    plot: bool = True
) -> None:
    """
    Simulates multiple user sessions and provides statistical summaries and visualizations.

    Args:
        n (int): Number of simulations.
        scores (Dict): A dictionary of scores.
        plot: (str): score_hist

    Returns:
        None
    """
    # Run simulations
    simulations = [test_session(base_scores) for _ in range(n)]

    scores_hist = {}
    scores_by_iter = []
    for simulation in simulations:
        for id, value in simulation.items():
            if value['score'] in list(scores_hist.keys()):
                scores_hist[value['score']] += 1
            else:
                scores_hist[value['score']] = 1
    

    if plot:
        plt.pie(x= list(scores_hist.values()), labels=list(scores_hist.keys()), autopct='%1.1f%%')
        plt.show()

    return simulations

test_session_simulation(100, base_scores)


def next_scores(
    results: Dict[int, Dict[str, Union[float, int]]],
    scores: Dict[int, Dict[str, Union[float, int]]]
) -> Dict[int, float]:
    """
    Calculates new scores based on the results.

    Args:
        results (Dict): A dictionary of results.
        scores (Dict): A dictionary of original scores.

    Returns:
        Dict: A dictionary with updated scores.
    """
    new_scores = {}
    for key, value in scores.items():
        if results[key]['streak'] > 0:
            new_scores[key] = right_answer(value['score'], value['streak'])
        else:
            new_scores[key] = wrong_answer(value['score'], key, len(scores))
    return new_scores
