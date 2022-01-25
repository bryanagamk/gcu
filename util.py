import json
import sys
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def get_read_input_csv(path):
    import csv

    with open('employee_birthday.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                line_count += 1
        print(f'Processed {line_count} lines.')
    return

def get_spreadsheet(keyfile):
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name(keyfile, scope)

    # authorize the clientsheet 
    client = gspread.authorize(creds)

    # get the instance of the Spreadsheet
    sheet = client.open('categories')

    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)

    return sheet_instance

def get_hipertensi_ref(records_data):
    list_ref = []

    # view the data
    for data in records_data:
        item = {
            "level": data["level_resiko"],
            "riwayat_merokok": data["riwayat_merokok"],
            "riwayat_olahraga": data["riwayat_olahraga"],
            "sistole_min": data["sistole_min"],
            "sistole_max": data["sistole_max"],
            "diastole_min": data["diastole_min"],	
            "diastole_max": data["diastole_max"],
            "ureum_min": data["ureum_min"],
            "ureum_max": data["ureum_max"],
            "kreatinin_min": data["kreatinin_min"],
            "kreatinin_max": data["kreatinin_max"],
            "gpr_min": data["gpr_min"],
            "gpr_max": data["gpr_max"],
        }
        list_ref.append(item)
        
    return list_ref

def item_check_int(item, curr, data, result):
    
    if str(data[f"{item}_max"]) == "max":
        if curr[item] > data[f"{item}_min"]:
            result[f"{item}_lvl"] = 5
    else:
        if curr[item] in range(int(data[f"{item}_min"]), int(data[f"{item}_max"])):
            print(item)
            print(curr[item])
            print(data[f"{item}_min"])
            print(data[f"{item}_max"])
            print("level:", data["level"])
            result[f"{item}_lvl"] = data["level"]
            
    return result

def item_check_float(item, curr, data, result):
    
    if str(data[f"{item}_max"]) == "max":
        if curr[item] > data[f"{item}_min"]:
            result[f"{item}_lvl"] = 5
    else:
        if curr[item] in range(int(data[f"{item}_min"]), int(data[f"{item}_max"])):
            print(item)
            print(curr[item])
            print(data[f"{item}_min"])
            print(data[f"{item}_max"])
            print("level:", data["level"])
            result[f"{item}_lvl"] = data["level"]
            
    return result

def get_level_status(params, curr, ref):
    
    level_status = {
        "sistole_lvl": 0,
        "diastole_lvl": 0,
        "kreatinin_lvl": 0, # belum terhandle
        "gpr_lvl": 0,
        "ureum_lvl": 0,
    }
    
    for data in ref:
        for param in params:
            result = item_check_int(param, curr, data, level_status)
            level_status = result
        
        # dst ..
    
        
    return result


def get_hipertensi_result(params):
    for param in params:
        if params[param] > 0:
            return "Y"
    return "T"

def get_current_status(params, path):

    df = pd.read_csv(path, engine='python', usecols=params)
    # currents = []
    # for row in df.iterrows():
    #     current = row[1]
    #     currents.append(current)

    # print(currents)
    return df