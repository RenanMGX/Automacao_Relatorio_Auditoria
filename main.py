from Entities.kpmg import KPMG
from selenium.common.exceptions import SessionNotCreatedException
from patrimar_dependencies.sharepointfolder import SharePointFolders
import shutil
import os
from time import sleep
from botcity.maestro import * #type: ignore
import traceback
from patrimar_dependencies.functions import P

class ExecuteAPP:
    @staticmethod
    def start(*, 
              maestro:BotMaestroSDK|None=None,
              user:str,
              password:str,
              label:str,
              url:str,
              path_target:str,
              headless:bool=True,
              tentativas:int=3
              ):
        for _ in range(tentativas):
            try:
                bot = KPMG(
                    user=user,
                    password=password,
                    url=url,
                    label=label,
                    maestro=maestro,
                    headless=headless
                )
            except SessionNotCreatedException:
                pass
            except Exception as error:
                print(traceback.format_exc())
                import pdb; pdb.set_trace()
                print(P(f"tentativa {_+1} de {tentativas} ao abrir o navegador falhou: {error}", color='red'))
                if _ >= (tentativas - 1):
                    raise error
                sleep(5)
                
        
        

        path_target = SharePointFolders(path_target).value
        
        for _ in range(tentativas):
            try:
                bot.extract_modulo_operacional(path_target=path_target) #type: ignore
            except Exception as error:
                print(P(f"Erro na tentativa {_+1} de {tentativas} do modulo operacional: {error}", color='red'))
                if _ >= (tentativas - 1):
                    print(traceback.format_exc())
                    if not maestro is None:
                        maestro.error(task_id=int(maestro.get_execution().task_id), exception=error)    
                    raise error
                else:
                    sleep(5)
         
        for _ in range(tentativas):
            try:
                bot.extract_modulo_estrategico(path_target=path_target) #type: ignore
            except Exception as error:
                print(P(f"Erro na tentativa {_+1} de {tentativas} do modulo estrategico: {error}", color='red'))
                if _ >= (tentativas - 1):
                    print(traceback.format_exc())
                    if not maestro is None:
                        maestro.error(task_id=int(maestro.get_execution().task_id), exception=error)              
                    raise error
                else:
                    sleep(5)
        
        bot.close_nav() #type: ignore
    
if __name__ == "__main__":
    from patrimar_dependencies.credenciais_botcity import CredentialBotCity
    
    crd = CredentialBotCity(login="#", key="#").get_credential("KPMG")
    
    
    ExecuteAPP.start(
        user=crd['user'],
        password=crd['password'],
        label="KPMG",
        url="https://krast.kpmg.com.br",
        path_target=r"RPA - Dados\Relatorios Auditoria\KPMG",
        headless=False
    )
    
    