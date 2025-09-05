from Entities.kpmg import KPMG
from patrimar_dependencies.sharepointfolder import SharePointFolders
import shutil
import os
from time import sleep
from botcity.maestro import * #type: ignore
import traceback

class ExecuteAPP:
    @staticmethod
    def start(*, 
              maestro:BotMaestroSDK|None=None,
              user:str,
              password:str,
              label:str,
              url:str,
              path_target:str,
              headless:bool=True
              ):
        
        bot = KPMG(
            user=user,
            password=password,
            url=url,
            label=label,
            maestro=maestro,
            headless=headless
        )
        
        #bot.start_nav(headless=headless)
        
        #path_target:str = f'C:\\Users\\{getuser()}\\PATRIMAR ENGENHARIA S A\\RPA - Documentos\\RPA - Dados\\Relatorios Auditoria\\KPMG'
        path_target = SharePointFolders(path_target).value
        
        try:
            path = bot.extract_modulo_operacional(path_target=path_target)
            # if os.path.exists(path):
            #     op_target_path = os.path.join(path_target, 'modulo_operacional.csv')
            #     os.unlink(op_target_path)
                
            #     shutil.copy2(path, op_target_path)
            #     sleep(1)
            #     shutil.copy2(path, op_target_path)
            #     sleep(1)
            #     shutil.copy2(path, op_target_path)
            # else:
            #     if not maestro is None:
            #         maestro.new_log_entry(
            #             activity_label="alimentar_relatorio_auditoria",
            #             values={
            #                 "texto": f"o arquivo do modulo operacional não foi encontrado {path}"
            #             }
            #         )                
                
        except Exception as error:
            print(traceback.format_exc())
            if not maestro is None:
                maestro.error(task_id=int(maestro.get_execution().task_id), exception=error)              
        
        try:
            path = bot.extract_modulo_estrategico(path_target=path_target)
            # if os.path.exists(path):
            #     es_target_path = os.path.join(path_target, 'modulo_estrategico.csv')
            #     os.unlink(es_target_path)

            #     shutil.copy2(path, es_target_path)
            #     sleep(1)
            #     shutil.copy2(path, es_target_path)
            #     sleep(1)
            #     shutil.copy2(path, es_target_path)
            # else:
            #     if not maestro is None:
            #         maestro.new_log_entry(
            #             activity_label="alimentar_relatorio_auditoria",
            #             values={
            #                 "texto": f"o arquivo do modulo estrategico não foi encontrado {path}"
            #             }
            #         )                
                
        except Exception as error:
            print(traceback.format_exc())
            if not maestro is None:
                maestro.error(task_id=int(maestro.get_execution().task_id), exception=error)              
        
        bot.close_nav()
    
if __name__ == "__main__":
    from patrimar_dependencies.credenciais_botcity import CredentialBotCity
    
    crd = CredentialBotCity(login="grupopatrimar", key="GRU_HTBO7WB9GS25VFRFW6JN").get_credential("KPMG")
    
    
    ExecuteAPP.start(
        user=crd['user'],
        password=crd['password'],
        label="KPMG",
        url="https://krast.kpmg.com.br",
        path_target=r"RPA - Dados\Relatorios Auditoria\KPMG",
        headless=False
    )
    
    