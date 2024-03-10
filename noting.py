from calendar import c
import concurrent.futures
import openpyxl
import dart_fss as dart
import os
from openpyxl import load_workbook
import pandas as pd
import csv
from dart_fss import (get_corp_list)
import matplotlib.pyplot as plt
from datetime import date, timedelta
import csv
import time
import pickle
import sys
from multiprocessing import Process,Pool

c= [1,2,3,4,5,6,7,8,9,10]
d={1: 'apple', 2: 'ball'}


for a, b in d:
    print(a,b)