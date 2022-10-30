from calendar import c
import pandas as pd
import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
file_path_orginal = os.path.join(ROOT_DIR,'files','original')
file_path_transformed = os.path.join(ROOT_DIR,'files','transformed')

def iex_to_csv(iex_details):
    iex_header_dict = {'DATE :':'DATE'}
    for column in iex_details.columns.values[1:5]:
        for i in range(len(iex_details[column])):
            item_split = iex_details[column][i].split()
            item_number = item_split[0]
            item_unit = ''.join(item_split[1:])
            iex_details[column][i]=float(item_number)
        iex_header_dict[column] = column+'('+item_unit+')'
    
    for column in iex_details.columns.values[5:]:
        for i in range(len(iex_details[column])):
            item_split_unit = iex_details[column][i].split(') ')
            item_unit = item_split_unit[-1]
            item_number_list = item_split_unit[0].split('(')
            item_number_list= item_number_list[1].split('. ')
            iex_details[column][i] = float(item_number_list[1])
        iex_header_dict[column] = column+'[in '+item_number_list[0]+' '+item_unit+']'
    iex_details.rename(columns =iex_header_dict,inplace=True)
    iex_details.to_csv(os.path.join(file_path_transformed,'transformed_iex_details.csv'),index=False)


def energy_details_to_csv(energy_details):
    energy_header_dict = {}
    for column in (energy_details.columns):
        for i in range(len(energy_details[column])):
            item = energy_details[column][i].split()
            item_unit = item[1]
            energy_details[column][i] = int(item[0])

        energy_header_dict[column]= column+'('+item_unit+')'
    energy_details.rename(columns =energy_header_dict,inplace=True)
    energy_details.to_csv(os.path.join(file_path_transformed,'transformed_energy_details.csv'),index=False)

def main():
    energy_details = pd.read_csv(os.path.join(file_path_orginal,'energydetails.csv'))
    iex_details = pd.read_csv(os.path.join(file_path_orginal,'iex.csv'))
    energy_details_to_csv(energy_details)
    iex_to_csv(iex_details)
    
# main()