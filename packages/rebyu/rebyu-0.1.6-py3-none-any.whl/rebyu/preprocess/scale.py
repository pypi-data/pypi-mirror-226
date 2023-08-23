import numpy as np
from typing import Any, Dict, Tuple, Union

POLARITY_LABEL_3 = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}
POLARITY_LABEL_5 = {0: 'Negative', 1: 'Slightly Negative', 2: 'Neutral', 3: 'Slightly Positive', 4: 'Positive'}


def linear_map(value: Any, n: int = 3, label: Union[Dict, None] = None):
    """ Linearly Scale values into N Categories. Values from -1 to 1.

    :param value: Any value of data
    :param n: Number of Categories
    :param label: (Optional) Cast Unlabelled values into Labelled
    :return: Category (Labelled or Unlabelled)
    """
    interval = 2 / n
    scaled = int((value + 1) // interval)
    category = max(0, min(n-1, scaled))

    if label:
        return label.get(category, category)
    return category


def polarity_threshold_map(
        value: Any,
        threshold: Tuple[int, int] = (-0.05, 0.05),
        label: Union[Dict, None] = POLARITY_LABEL_3):
    """ Polarity Mapping by Threshold (Only 3 Categories)

    :param value: Any value of data
    :param threshold: Negative and Positive Threshold (-0.05, 0.05)
    :param label: (Optional) Cast Unlabelled values into Labelled
    :return: Category (Labelled or Unlabelled)
    """
    neg, pos = min(threshold), max(threshold)

    out = 1  # Neutral
    if value > pos:
        out += 1  # Positive
    if value < neg:
        out -= 1  # Negative

    if label:
        return label.get(out, out)
    return out
