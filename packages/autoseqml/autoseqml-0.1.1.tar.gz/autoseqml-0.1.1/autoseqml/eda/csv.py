import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .eda import EDA

class CSV(EDA):
    def __init__(self, file, graph_path=''):
        super().__init__(file, graph_path)
        