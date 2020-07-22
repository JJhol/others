"""This is the subclass of Transform function for Philippines (APAC division).

We will define transform functions specific to Malaysia here.

Author: Jholman Jaramillo
Last Modified: July 22, 2020
"""

import re

import pandas as pd

from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class ApacPhilippinesTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """

    def __init__(self, config):
        self.config = config
