from navegador import Navegador as Nav, P, By, Keys, Select
import exceptions
from time import sleep
import os
import random
import string
from botcity.maestro import * # type: ignore
from patrimar_dependencies.credenciais_botcity import CredentialBotCity
from .filles import concatenar_csv_files

class KPMG:
    @property
    def nav(self) -> Nav:
        try:
            return self.__nav
        except AttributeError:
            raise exceptions.NavNotStarted(f"primeiro Inicia o Navegador usando {self.__class__.__name__}.start_nav()")
        
    def __init__(self, *, user:str, password:str, label:str, url:str, maestro:BotMaestroSDK|None=None, headless:bool=True) -> None:
        self.__crd:dict = {"user": user, "password": password, "label": label}
        self.url:str = url
        self.__maestro:BotMaestroSDK|None = maestro
        self.start_nav(headless=headless)
        self.nav.get(self.url)
        self.nav.get(self.url)
        # if url:
        #     self.__nav = Nav(url=url)
            
    def start_nav(self, url:str="", headless:bool=True):
        try:
            if self.nav:
                print(P("O navegador já está aberto", color='yellow'))
                return
        except:
            self.__nav = Nav(headless=headless)
            if url:
                self.nav.get(url)
    
    def close_nav(self):
        try:
            self.nav.close()
        except:
            pass
        try:
            del self.__nav
        except:
            pass
        
    def __limpar_pasta_download(self):
        for file in os.listdir(self.nav.path_download):
            file = os.path.join(self.nav.path_download, file)
            if os.path.isfile(file):
                os.unlink(file)
    
    def ultimo_download(self) -> str:
        for _ in range(60):
            sleep(1)
            lista_arquivos:list = [os.path.join(self.nav.path_download, file) for file in os.listdir(self.nav.path_download)]
            if lista_arquivos:
                arquivo:str = max(lista_arquivos, key=os.path.getctime)
                sleep(1)
                if arquivo.lower().endswith('.crdownload'):
                    #print(arquivo)
                    del lista_arquivos
                    del arquivo
                    continue
                else:
                    return arquivo
            else:
                sleep(1)
        raise Exception("não foi possivel identificar ultimo download")
    
    @staticmethod
    def verificar_arquivos_download(path:str, *,timeout:int=5 * 60, wait:int=0) -> bool:
        if wait > 0:
            sleep(wait)

        if os.path.exists(path):
            for _ in range(timeout):
                exist:bool = False
                for file in os.listdir(path):
                    if file.lower().endswith('.crdownload'):
                        exist = True
                if not exist:
                    sleep(3)
                    return True
                sleep(1)
            return False
        return False
        
    def __login(self) -> None:
        self.nav.get(self.url)
        if self.nav.find_element(By.ID, 'Username'):
            self.nav.find_element(By.ID, 'Username').send_keys(self.__crd['user'])
            self.nav.find_element(By.ID, 'Password').send_keys(self.__crd['password'])
            self.nav.find_element(By.ID, 'Password').send_keys(Keys.RETURN)
            try:
                if (alert:=self.nav.find_element(By.ID, 'alert', timeout=2, wait_before=3).text):
                    raise exceptions.Alert(alert)
            except exceptions.Alert as err:
                raise exceptions.Alert(err)
            except Exception:
                pass
            
            sleep(1)
            try:
                if not self.__maestro is None:
                    self.nav.find_element(By.ID, 'ActualPassword', timeout=5).send_keys(self.__crd['password'])
                    
                    new_password = ""
                    for _ in range(60):
                        new_password:str = KPMG.create_new_password(num=14)
                        self.nav.find_element(By.ID, 'NewPassword').send_keys(new_password)
                        
                        sleep(1)
                        if "Senha muito forte" in self.nav.find_element(By.ID, 'password-score').text:
                            break
                        self.nav.find_element(By.ID, 'NewPassword').clear()
                        if _ == 59:
                            raise Exception("não foi possivel criar uma senha forte")
                        
                    self.nav.find_element(By.ID, 'ConfirmPassword').send_keys(new_password)
                    self.nav.find_element(By.ID, 'alter-password').click()
                    
                    sleep(1)
                    try:
                        self.nav.find_element(By.ID, 'ActualPassword', timeout=2)
                        raise Exception("não foi possivel alterar a senha")
                    except exceptions.ElementNotFound:
                        # crd = Credential(Config()['credential']['navegador'])
                        # crd.save(user=self.__crd['user'], password=new_password)
                        self.__maestro.update_credential(label=self.__crd['label'], key="password", new_value=new_password)
                        self.__crd['password'] = new_password
                        
                else:
                    print("Não foi possivel criar uma nova senha pq o maestro não foi isntanciado")
                    
                    
                
            except:
                pass
            
            print(P("Login Efeturado!", color="green"))
            return
            
        print(P("já está logado!", color='yellow'))
        #import pdb; pdb.set_trace()

    def extract_modulo_operacional(self, *, path_target:str, tentativas:int=3) -> str:
        if tentativas <= 0:
            tentativas = 1
        for _ in range(tentativas):
            try:
                self.__limpar_pasta_download()
                self.__login()
                
                #import pdb;pdb.set_trace()
                
                self.nav.find_element(By.ID, 'grc-system').click()
                self.nav.find_element(By.XPATH, '//*[@id="menu"]/li/a').click()
                self.nav.find_element(By.XPATH, '//*[@id="ReportsDropdown"]/li[1]/a/span').click()
                
                sleep(1)
                Select(self.nav.find_element(By.ID, 'input-company')).select_by_value("44")
                sleep(1)
                Select(self.nav.find_element(By.ID, 'input-type')).select_by_value("Sox")
                sleep(2)
                s_options = Select(self.nav.find_element(By.ID, 'input-calendar')).options
                s_options = [x for x in s_options if not 'Selecione o ciclo' == x.text]
                
                files = []
                for option in s_options:
                    sleep(1)
                    option.click()
                    
                    sleep(1)        
                    while "Carregando..." in self.nav.find_element(By.ID, 'filter').text:
                        sleep(.25)
                    
                    sleep(2)  
                    self.nav.find_element(By.ID, 'btn-generate-report-database').click()
                    
                    sleep(10)
                    #KPMG.verificar_arquivos_download(self.nav.path_download)
                    files.append(self.ultimo_download())
                    sleep(1)
                
                file_path = concatenar_csv_files(
                    list_files=files,
                    new_name="modulo_operacional",
                    target_path=path_target   
                )
                return file_path
            except Exception as error:
                print(f"tentativa {_+1} de {tentativas} falhou: {error}")
                if _ >= (tentativas - 1):
                    raise error
                
        return ""
    
    def extract_modulo_estrategico(self, *, path_target:str, tentativas:int=3) -> str:
        if tentativas <= 0:
            tentativas = 1
        for _ in range(tentativas):
            try:
                self.__limpar_pasta_download()
                self.__login()
                
                self.nav.find_element(By.ID, 'erm-system').click()
                self.nav.find_element(By.XPATH, '//*[@id="menu"]/li/a').click()
                self.nav.find_element(By.XPATH, '//*[@id="ReportsDropdown"]/li[2]/a/span').click()
                
                s_options = Select(self.nav.find_element(By.ID, 'input-calendar')).options
                s_options = [x for x in s_options if not 'Selecione o ciclo' == x.text]
                
                files = []
                for option in s_options:
                    option.click()
                
                    sleep(2)
                    self.nav.find_element(By.ID, 'btn-generate-report-riskanalysis').click()
                    
                    sleep(10)
                    #KPMG.verificar_arquivos_download(self.nav.path_download)
                    files.append(self.ultimo_download())
                    sleep(1)
                
                file_path = concatenar_csv_files(
                    list_files=files,
                    new_name="modulo_estrategico",
                    target_path=path_target
                )
                return file_path
            except Exception as error:
                print(f"tentativa {_+1} de {tentativas} falhou: {error}")
                if _ >= (tentativas - 1):
                    raise error
                
        return ""
                

    @staticmethod
    def create_new_password(num:int=15) -> str:
        base_letters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(base_letters) for _ in range(num))
        
if __name__ == "__main__":
    pass
