import pandas as pd
import csv
import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
file_path_orginal = os.path.join(ROOT_DIR,'files','original')
file_path_transformed = os.path.join(ROOT_DIR,'files','transformed')

def main():
    energy_details = pd.read_csv(os.path.join(file_path_orginal,'energydetails.csv'))
    iex_details = pd.read_csv(os.path.join(file_path_orginal,'iex.csv'))
    item_header_dict = {}

    for column in (energy_details.columns):
        for i in range(len(energy_details[column])):
            item = energy_details[column][i].split()
            item_unit = item[1]
            energy_details[column][i] = int(item[0])

        item_header_dict[column]= column+'('+item_unit+')'
        energy_details.rename(columns =item_header_dict,inplace=True)
        energy_details.to_csv(os.path.join(file_path_transformed,'transformed_energy_details.csv'),index=False)
main()