#----------------------LIBRARIES AND DIRECTORIES----------------------------------------

import csv
import pprint
import os
import glob
import pandas as pd
import numpy as np
import re
import requests

import copy
import itertools

from pandas import read_csv
from importlib.machinery import SourceFileLoader
from zipfile import ZipFile
from io import BytesIO, StringIO

path_wcpd = '/Users/gd/GitHub/WorldCarbonPricingDatabase/_dataset/data'
path_ghg = '/Users/gd/OneDrive - rff/documents/research/projects/ecp/ecp_dataset/source_data/ghg_inventory/raw'
path_aux_data = '/Users/gd/OneDrive - rff/documents/research/projects/ecp/ecp_dataset'

ecp_general = SourceFileLoader('general_func', path_dependencies+'/ecp_v3_gen_func.py').load_module()
ecp_cov_fac = SourceFileLoader('coverage_factors', path_dependencies+'/ecp_v3_coverageFactors.py').load_module()
ecp_inv_nat = SourceFileLoader('inventory_nat', path_dependencies+'/inventory_preproc_nat.py').load_module()
ecp_inv_subnat = SourceFileLoader('inventory_nat', path_dependencies+'/inventory_preproc_subnat.py').load_module()
ecp_inv_share = SourceFileLoader('inventory_share_func', path_dependencies+'/ecp_v3_inventory_share_func.py').load_module()
ecp_coverage = SourceFileLoader('coverage', path_dependencies+'/ecp_v3_coverage.py').load_module()
ecp_cur_conv = SourceFileLoader('currency_conversion', path_dependencies+'/ecp_v3_currConversion.py').load_module()
ecp_overlap = SourceFileLoader('overlap', path_dependencies+'/ecp_v3_overlap.py').load_module()
ecp_wav = SourceFileLoader('average', path_dependencies+'/ecp_v3_weightedAverage.py').load_module()
ecp_sec_em = SourceFileLoader('average', path_dependencies+'/ecp_v3_aggSec.py').load_module()