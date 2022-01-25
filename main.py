# importing the required libraries
from oauth2client.service_account import ServiceAccountCredentials
import util

if __name__ == '__main__':
    sheet_instance = util.get_spreadsheet("key.json")
    records_data = sheet_instance.get_all_records()
    ref_data = util.get_hipertensi_ref(records_data)
    
    # ambil dari csv input
    current_hipertensi_item = {
        "sistole": 110,
        "diastole": 80,
        "kreatinin": 2.2,
        "gpr": 70,
        "ureum": 30,
    }
    
    # parameter penyakit
    params = ['sistole', 'diastole', 'kreatinin', 'gpr', 'ureum', 'riwayat_merokok', 'riwayat_olahraga']
    params_scale = ['sistole', 'diastole', 'kreatinin', 'gpr', 'ureum']
    
    # get current status dynamic (belum)
    # path = "sample_input.csv"
    # current_items = util.get_current_status(params, path)
    
    level_status = util.get_level_status(params_scale, current_hipertensi_item, ref_data)
    print(level_status)
    
    # diagnose 
    hipertensi_result = util.get_hipertensi_result(level_status)
    print(hipertensi_result)
            