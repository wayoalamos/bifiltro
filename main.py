# code for Isabel Vergara

from bs4 import BeautifulSoup
import requests
import openpyxl

class RowItem:
    def __init__(self):
        self.counter = 0
        self.planta = None
        self.codigo = None
        self.fecha = None
        self.muestra = None
        self.tipo = None
        self.caudal = None
        self.AG = None
        self.DBOs = None
        self.P = None
        self.N = None
        self.NK = None
        self.Nitrato = None
        self.Nitrito2 = None
        self.Ox  = None
        self.SST = None
        self.DQO  = None
        self.CE  = None
        self.CF  = None
        self.pH = None
        self.T  = None
        self.PE  = None
        self.STD  = None

    def print_all(self):
        print("self.counter", self.counter)
        print("self.planta", self.planta)
        print("self.codigo", self.codigo)
        print("self.fecha", self.fecha)
        print("self.muestra", self.muestra)
        print("self.tipo", self.tipo)
        print("self.caudal", self.caudal)
        print("self.AG", self.AG)
        print("self.DBOs", self.DBOs)
        print("self.P", self.P)
        print("self.N", self.N)
        print("self.NK", self.NK)
        print("self.Nitrato", self.Nitrato)
        print("self.Nitrito2", self.Nitrito2)
        print("self.Ox", self.Ox )
        print("self.SST", self.SST)
        print("self.DQO", self.DQO )
        print("self.CE", self.CE )
        print("self.CF", self.CF )
        print("self.pH", self.pH)
        print("self.T", self.T )
        print("self.PE", self.PE )
        print("self.STD", self.STD )

    def in_row_info(self):
        l = []
        l.append(self.planta)
        l.append(self.codigo)
        l.append(self.fecha)
        l.append(self.muestra)
        l.append(self.tipo)
        l.append(self.caudal)
        l.append(self.AG)
        l.append(self.DBOs)
        l.append(self.P)
        l.append(self.N)
        l.append(self.NK)
        l.append(self.Nitrato)
        l.append(self.Nitrito2)
        l.append(self.Ox)
        l.append(self.SST)
        l.append(self.DQO)
        l.append(self.CE)
        l.append(self.CF)
        l.append(self.pH)
        l.append(self.T)
        l.append(self.PE)
        l.append(self.STD)
        return l


def part_of(word, list_of_words):
    index = 0
    for l_word in list_of_words:
        if word in l_word:
            return index
        index += 1
    return -1


url = "http://www.biofiltro.cl/sistema/index.php/admin"
url_informe = "http://www.biofiltro.cl/sistema/index.php/admin/planta_informe"
username = input("username: ")
password = input("password: ")
payload = {"username": username, "password":password}

s = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0'}
response = s.post(url, headers=headers, data=payload)
response = s.get(url_informe, headers=headers)
content = response.content
html = BeautifulSoup(content, "html.parser")
table = html.find("tbody")

details_consts = ['AG(mg/L) = ', 'DBOs(mg/L) = ', 'P(mg/L) = ', 'N(mg/L) = ', 'NK(mg/L) = ', 'Nitrato (mg/l N-NO3) = ', 'Nitrito (mg/l N-NO2) = ', 'Ox (mgO2/l) = ', 'SST(mg/L) = ', 'DQO (mg/l) = ', 'CE (us/cm) = ', 'CF (NMP/100 ml) = ', 'pH = 7,0', 'T (°C) = 18,3', 'PE (mm) = ', 'STD (mg/l) = ']

def get_table_info(table, date):
    table_list = []
    row_counter = 0
    should_continue = True
    for row in table.find_all("tr"):
        if not should_continue:
            break
        row_counter += 1
        rowitem = RowItem()
        rowitem.counter = row_counter

        td_counter = 0
        for td in row.find_all("td"):
            for row_content in td.stripped_strings:
                if td_counter == 0:
                    rowitem.planta = row_content
                if td_counter == 1:
                    rowitem.codigo = row_content
                if td_counter == 2:
                    rowitem.fecha = row_content
                    if not is_more_recent(row_content, date):
                        should_continue = False
                if td_counter == 3:
                    rowitem.muestra = row_content
                if td_counter == 4:
                    rowitem.tipo = row_content
                if td_counter == 5:
                    rowitem.caudal = row_content    
            if td_counter == 6:
                details = td.a["data-content"]
                details = details.split("<br>")
                for detail in details:
                    #print(detail)
                    short_detail = detail.split("=")[0].rstrip()
                    new_detail = detail.split("=")[1].rstrip().lstrip()
                    ind = part_of(short_detail, details_consts)
                    if ind != -1:
                        if ind == 0:
                            rowitem.AG = new_detail
                        if ind == 1:
                            rowitem.DBOs = new_detail
                        if ind == 2:
                            rowitem.P = new_detail
                        if ind == 3:
                            rowitem.N = new_detail
                        if ind == 4:
                            rowitem.NK = new_detail
                        if ind == 5:
                            rowitem.Nitrato = new_detail
                        if ind == 6:
                            rowitem.Nitrito2 = new_detail
                        if ind == 7:
                            rowitem.Ox  = new_detail
                        if ind == 8:
                            rowitem.SST  = new_detail
                        if ind == 9:
                            rowitem.DQO  = new_detail
                        if ind == 10:
                            rowitem.CE  = new_detail
                        if ind == 11:
                            rowitem.CF  = new_detail
                        if ind == 12:
                            rowitem.pH = new_detail
                        if ind == 13:
                            rowitem.T  = new_detail
                        if ind == 14:
                            rowitem.PE  = new_detail
                        if ind == 15:
                            rowitem.STD  = new_detail
                    else:
                        # print(short_detail)
                        print("esto no deberia pasar :(")
                        print("alguna informacion de muestras no se puede parsear")
                        print("especificamente es la fila con esta info")
                        print(rowitem.planta, rowitem.codigo, rowitem.fecha)

            td_counter += 1
        if should_continue:
            table_list.append(rowitem)
    return table_list, should_continue

def get_all_info(date):
    all_info = []
    i = -1
    while True:
        i+= 1
        url_new = url_informe + "/index/" + str(40*i) + "?"
        response = s.get(url_new, headers=headers)
        content = response.content
        html = BeautifulSoup(content, "html.parser")
        table = html.find("tbody")
        table_list, should_continue = get_table_info(table, date)
        all_info += table_list
        if not should_continue:
            break
    return all_info
        
def getsCSV(table_list):
    workbook = openpyxl.Workbook() # create workbook element
    workbook_active = workbook.active

    # excel headers
    header=["planta", "codigo", "fecha", "muestra", "tipo", "caudal", "AG", "DBOs", "P", "N", "NK", "Nitrato", "Nitrito2", "Ox", "SST", "DQO", "CE", "CF", "pH", "T", "PE", "STD"]
    workbook_active.append(header)
    for item in table_list:
        workbook_active.append(item.in_row_info())

    workbook.save("sample.xlsx")

    return openpyxl.writer.excel.save_virtual_workbook(workbook)

def is_more_recent(date1, date2):
    #return true if date1 is more recent than date2
    def get_date(date):
        day, month, year = date.split("-")
        return int(day), int(month), int(year)
        
    day1, month1, year1 = get_date(date1)
    day2, month2, year2 = get_date(date2)
    if year1 < year2:
        return False
    if year1 > year2:
        return True
    if month1 < month2:
        return False
    if month1 > month2:
        return True
    if day1 < day2:
        return False
    if day1 > day2:
        return True
    return True
    

date = input("ingresa fecha en fortmato DD-MM-YYYY: ")
table_list = get_all_info(date)
getsCSV(table_list)
print(len(table_list))