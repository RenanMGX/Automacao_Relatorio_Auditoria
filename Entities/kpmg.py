from navegador import Navegador as Nav, P, By, Keys, Select
import exceptions
from Entities.dependencies.credenciais import Credential
from Entities.dependencies.config import Config
from time import sleep
import os

class KPMG:
    @property
    def nav(self) -> Nav:
        try:
            return self.__nav
        except AttributeError:
            raise exceptions.NavNotStarted(f"primeiro Inicia o Navegador usando {self.__class__.__name__}.start_nav()")
        
    def __init__(self, *, url:str="") -> None:
        self.__crd:dict = Credential(Config()['credential']['navegador']).load()
        
        if url:
            self.__nav = Nav(url=url)
            
    def start_nav(self, url:str=""):
        try:
            if self.nav:
                print(P("O navegador já está aberto", color='yellow'))
                return
        except:
            self.__nav = Nav()
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
            arquivo:str = max(lista_arquivos, key=os.path.getctime)
            sleep(1)
            if '.crdownload' in arquivo:
                #print(arquivo)
                del lista_arquivos
                del arquivo
                continue
            else:
                return arquivo
        raise Exception("não foi possivel identificar ultimo download")
    
    @staticmethod
    def verificar_arquivos_download(path:str, *,timeout:int=5 * 60, wait:int=0) -> bool:
        if wait > 0:
            sleep(wait)

        if os.path.exists(path):
            for _ in range(timeout):
                exist:bool = False
                for file in os.listdir(path):
                    if '.crdownload' in file:
                        exist = True
                if not exist:
                    sleep(3)
                    return True
                sleep(1)
            return False
        return False
        
    def __login(self) -> None:
        self.nav.get(Config()['url']['default'])
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
            
            print(P("Login Efeturado!", color="green"))
            return
            
        print(P("já está logado!", color='yellow'))

    def extract_modulo_operacional(self):
        self.__limpar_pasta_download()
        self.__login()
        
        self.nav.find_element(By.ID, 'grc-system').click()
        self.nav.find_element(By.XPATH, '//*[@id="menu"]/li/a').click()
        self.nav.find_element(By.XPATH, '//*[@id="ReportsDropdown"]/li[1]/a/span').click()
        
        sleep(1)
        Select(self.nav.find_element(By.ID, 'input-company')).select_by_value("44")
        sleep(1)
        Select(self.nav.find_element(By.ID, 'input-type')).select_by_value("Sox")
        sleep(1)
        Select(self.nav.find_element(By.ID, 'input-calendar')).select_by_value("122")
        
        sleep(1)        
        while "Carregando..." in self.nav.find_element(By.ID, 'filter').text:
            sleep(.25)
        
        sleep(1)  
        self.nav.find_element(By.ID, 'btn-generate-report-database').click()
        
        KPMG.verificar_arquivos_download(self.nav.path_download)
        
        return self.ultimo_download()
    
    def extract_modulo_estrategico(self):
        self.__limpar_pasta_download()
        self.__login()
        
        self.nav.find_element(By.ID, 'erm-system').click()
        self.nav.find_element(By.XPATH, '//*[@id="menu"]/li/a').click()
        self.nav.find_element(By.XPATH, '//*[@id="ReportsDropdown"]/li[2]/a/span').click()
        
        sleep(1)
        Select(self.nav.find_element(By.ID, 'input-calendar')).select_by_value('217')
        
        sleep(1)
        self.nav.find_element(By.ID, 'btn-generate-report-riskanalysis').click()
        
        KPMG.verificar_arquivos_download(self.nav.path_download)
        
        return self.ultimo_download()
        
if __name__ == "__main__":
    pass
