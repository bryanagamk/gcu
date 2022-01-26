import json
import sys
import gspread
import pandas as pd
import numpy as np
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
                print(
                    f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                line_count += 1
        print(f'Processed {line_count} lines.')
    return


def get_spreadsheet(keyfile):
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

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


def item_check(item, curr, data, result):

    if str(data[f"{item}_max"]) == "max":
        if curr[item] > data[f"{item}_min"]:
            result[f"{item}_lvl"] = 5
    else:
        print(item)
        print(curr[item])
        print(float(data[f"{item}_min"]))
        print(float(data[f"{item}_max"]))
        total = np.arange(float(data[f"{item}_min"]), float(
            data[f"{item}_max"]), 0.1)
        # convert to float16
        dataset = np.linspace(float(data[f"{item}_min"]), float(data[f"{item}_max"]), len(
            total), endpoint=False, retstep=False, dtype=np.float16)

        value = np.where(dataset == curr[item])

        if len(value[0]) == 0:
            print("level [none]: -")
            return result

        print("level [updated]:", data["level"])
        result[f"{item}_lvl"] = data["level"]

    return result


def get_level_status(params, curr, ref):

    level_status = {
        "sistole_lvl": 0,
        "diastole_lvl": 0,
        "kreatinin_lvl": 0,
        "gpr_lvl": 0,
        "ureum_lvl": 0,
    }

    for data in ref:
        for param in params:
            result = item_check(param, curr, data, level_status)
            level_status = result

        # dst ..

    return result


def get_hipertensi_result(params):
    for param in params:
        if params[param] > 0:
            return "Y"
    return "T"


def get_current_status(params, path):

    data = pd.read_csv(path, engine='python', usecols=params)
    df = pd.DataFrame(data)
    list_dict = []

    for index, row in list(df.iterrows()):
        list_dict.append(dict(row))

    return list_dict


def pre_processing_data(params):  # belum selesai
    print(type(params))
    list_items = []
    list_key = []
    list_value = []
    for index, param_dict in params:
        for key, value in param_dict.items():
            item = {
                # "index": index,
                "name": key,
                "value": value,
                "type": 0
            }
            # list_key.append(key)
            # list_value.append(value)

    # for p in params:
    #     index = p['index']
    #     item = {
    #         "index": index,
    #         "name": list_key[index],
    #         "value": list_value[index],
    #         "type": 0,
    #     }
    #     list_items.append(item)
    # # print(list_key)
    # print(list_items)
