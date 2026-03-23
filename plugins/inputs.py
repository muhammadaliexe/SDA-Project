import csv
import time
import os

def fix_type(val, d_type):
    if d_type == "integer": return int(val)
    if d_type == "float": return float(val)
    return str(val)