from .correlator import Correlator

def create_correlator(data_x=None, date=None, start_date=None, end_date=None):
    return Correlator(data_x, date, start_date, end_date)
