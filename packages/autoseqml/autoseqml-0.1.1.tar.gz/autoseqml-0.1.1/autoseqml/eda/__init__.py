from .csv import CSV
from .txt import TXT
from ..utils import check_ext

def EDA(file, graph_path=''):
    if not check_ext(file): return 'file extension unacceptable'

    ext = file.split('.')[-1]
    if ext=='csv':
        return CSV(file,graph_path)
    elif ext=='txt':
        return TXT(file,graph_path)
