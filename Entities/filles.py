import os
import pandas as pd
from typing import List
from botcity.maestro import * #type: ignore

maestro:BotMaestroSDK|None = BotMaestroSDK()
try:
    execution = maestro.get_execution()
except:
    maestro = None

def concatenar_csv_files(*,list_files:List[str], new_name:str, target_path:str):
    if not new_name.lower().endswith('.json'):
        new_name = f"{new_name}.json"
        
    if not os.path.isdir(target_path):
        raise Exception(f"o caminho '{target_path}' não é uma pasta válida")
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    
    
    files_dfs = []
    for file in list_files:
        if os.path.isfile(file):
            if os.path.exists(file):
                if file.lower().endswith('.csv'):
                    files_dfs.append(pd.read_csv(file, sep=';',skiprows=1, encoding='ISO-8859-1'))
                    # try:
                    #     os.unlink(file)
                    # except:
                    #     pass
    
    #import pdb; pdb.set_trace()
    df = pd.DataFrame()
    for df_temp in files_dfs:
        df = pd.concat([df, df_temp], ignore_index=True)
    
    file_final_path = os.path.join(target_path, new_name)
    #df.to_csv(file_final_path, index=False, sep=';', encoding='utf-8-sig')
    
    df.to_json(file_final_path, orient='records', date_format='iso')
    if pd.read_json(file_final_path).empty:
        err = f"O DataFrame do '{new_name}' está vazio, não foi possivel salvar arquivo"
        print(err)
        
        try:
            raise ValueError(err)
        except Exception as error:
            #import pdb; pdb.set_trace()
            if not maestro is None:
                maestro.error(task_id=int(execution.task_id), exception=error)
            raise error

    return file_final_path

if __name__ == "__main__":
    path = r'R:\Automacao_Relatorio__Auditoria__Isabella\Download_Arquivos'
    files = [os.path.join(path, file) for file in os.listdir(path)]
    
    file_path = concatenar_csv_files(
        list_files=files,
        new_name="modulo_estrategico",
        target_path=path
    )
