# type: ignore

import numpy as np
import pandas as pd
from pyparsing import col
from data.data_sets import LLM2, kw_read_csv, kw_to_csv, sep
import os, dotenv, util.utils as utils
from pathlib import Path

from data.columns import SPEC, PART, CODE, BLOC

dotenv.load_dotenv()
ev = dict(os.environ)  # FILE=ev['FILESYSTEM']

import pandas as pd


df_micro = pd.read_csv(micro_jan2018)  # 4351x443
df_clndx = pd.read_csv(clndx_jan2018)  # 4351x50
df_txt = pd.merge(df_micro,df_clndx, how="inner", on="Specimen") # 4351x492

df_txt.to_csv("merged.csv", index=False)
