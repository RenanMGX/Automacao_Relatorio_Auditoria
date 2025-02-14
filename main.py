from Entities.kpmg import KPMG
from Entities.dependencies.arguments import Arguments
from Entities.dependencies.config import Config
from Entities.dependencies.sharepointfolder import SharepointFolders, getuser
from Entities.dependencies.logs import Logs, traceback
import shutil
import os
from time import sleep


class Execute:
    @staticmethod
    def start():
        bot = KPMG()
        
        bot.start_nav()
        
        path_target:str = f'C:\\Users\\{getuser()}\\PATRIMAR ENGENHARIA S A\\RPA - Documentos\\RPA - Dados\\Relatorios Auditoria\\KPMG'
        
        try:
            path = bot.extract_modulo_operacional()
            if os.path.exists(path):
                shutil.copy2(path, os.path.join(path_target, 'modulo_operacional.csv'))
            else:
                Logs().register(status='Report', description=f"o arquivo do modulo operacional não foi encontrado {path}")
        except Exception as err:
            Logs().register(status='Report', description=str(err), exception=traceback.format_exc())
        
        try:
            path = bot.extract_modulo_estrategico()
            if os.path.exists(path):
                shutil.copy2(path, os.path.join(path_target, 'modulo_estrategico.csv'))
            else:
                Logs().register(status='Report', description=f"o arquivo do modulo estrategico não foi encontrado {path}")
        except Exception as err:
            Logs().register(status='Report', description=str(err), exception=traceback.format_exc())
        
        bot.close_nav()
    
if __name__ == "__main__":
    Arguments({
        'start': Execute.start
    })
    