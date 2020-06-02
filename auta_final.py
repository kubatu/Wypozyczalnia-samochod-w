
from __future__ import unicode_literals
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#import pymysql as db
import mysql.connector as db

database = db.connect(host='db.zut.edu.pl',user='sm44494',passwd='DEqmPb3j',database='sm44494')
cursor= database.cursor()
def is_float(value):
  try:
    float(value)
    return True
  except:
    return False
def is_int(value):
  try:
    int(value)
    return True
  except:
    return False

class Wypozyczalnia(QWidget):

    rePos = QPoint
    def f_on_wybor(self,index):
        self.info=''
        self.__cur_select=index
        for i in range(3,len(self.dostepne[index])):
            self.info+=str(self.dostepne[index][i])
            self.info+="\n"
        self.e_wyp_sam_info.setText(self.info)
    
    def f_wyp_sam(self):
        self.newWindow()
        layout=QGridLayout()
        self.dostepne=[]
        self.wybor=QComboBox()
        backBtn=QPushButton('WSTECZ')
        okBtn=QPushButton('OK')
        backBtn.clicked.connect(self.backToInterface)
        self.e_wyp_sam_info=QLabel('')
        self.box_klient_id=QLineEdit('')
        self.warning_wyp_sam=QLabel('ID Klienta')
        self.wybor.currentIndexChanged.connect(self.f_on_wybor)
        cursor.execute('SELECT * FROM Samochody WHERE Status ="Dostepny" ')
        self.row=cursor.fetchone()
        while self.row is not None:
            self.dostepne.append(self.row)
            self.row=cursor.fetchone()
        for i in self.dostepne:
            self.wybor.addItem(i[4]+" "+i[3])
        layout.addWidget(self.wybor,2,2,1,1)
        layout.addWidget(QLabel('Wybierz pojazd'),2,1,1,1)
        layout.addWidget(backBtn,4,1,1,1)
        layout.addWidget(self.warning_wyp_sam,3,1,1,1)
        layout.addWidget(self.e_wyp_sam_info,1,1,1,1)
        layout.addWidget(self.box_klient_id,3,2,1,1)
        layout.addWidget(okBtn,4,2,1,1)
        okBtn.clicked.connect(self.f_wyb_sam_ok)
        self.setLayout(layout)
        self.show()

    def f_wyb_sam_ok(self): 
        wynik=0
        if is_int(self.box_klient_id.text()) and int(self.box_klient_id.text())>0:
            cursor.execute("SELECT * FROM Użytkownicy WHERE ID_uzytkownika="+self.box_klient_id.text())
            for i in cursor:
                wynik+=1
                dane=(i[0],i[3],i[4])
            if(wynik==1):
                self.warning_wyp_sam.setText('ID wypożyczającego')
                self.close()
                self.newWindow()
                layout=QGridLayout()
                e_wyp_sam_info_klient=QLabel(str(dane[0])+'\n'+str(dane[1])+'\n'+str(dane[2]))
                backBtn=QPushButton('WSTECZ')
                okBtn=QPushButton('OK')
                
                self.cena_box=QLineEdit()
                self.e_cena=QLabel('CENA')
                backBtn.clicked.connect(self.f_back_to_wyp_sam)
                okBtn.clicked.connect(self.wyp_sam_done)


                layout.addWidget(self.e_wyp_sam_info,1,1,1,1)
                layout.addWidget(e_wyp_sam_info_klient,1,2,1,1)
                layout.addWidget(self.e_cena,2,1,1,1)
                layout.addWidget(self.cena_box,2,2,1,1)
                layout.addWidget(backBtn,3,1,1,1)
                layout.addWidget(okBtn,3,2,1,1)
                self.setLayout(layout)
                self.show()
            else:
                self.warning_wyp_sam.setText('ID wypożyczającego nie znalezione w bazie')

    def f_back_to_wyp_sam(self):
        self.close()
        self.f_wyp_sam()

    def wyp_sam_done(self):
        if is_float(self.cena_box.text()) and float(self.cena_box.text())>0:
            cursor.execute("UPDATE Samochody SET Status='Wypozyczony' WHERE ID_samochodu="+str(self.dostepne[self.__cur_select][0]))
            cursor.execute("INSERT INTO Wypozyczenia(Data_wypozyczenia,Cena,ID_uzytkownika,ID_samochodu) VALUES (CURDATE(),"+self.cena_box.text()+","+self.box_klient_id.text()+','+str(self.dostepne[self.__cur_select][0])+")")
            database.commit()
            self.backToInterface()
        else:
            self.e_cena.setText('CENA JEST\nNIEPOPRAWNA!')


    def closeEvent(self, QCloseEvent):
        self.rePos = self.pos()

    def dodajSamochodFun(self):
        cursor.execute('SELECT max(ID_samochodu) FROM Samochody')
        id = cursor.fetchone()[0]
        if id == None:
            id = 1
        else:
            id += 1
        
        values = "VALUES(" + str(id) + ",\'" #ID
        values += str(self.samochodList[0].text()) + "\',\'" #nrrejestracyjny
        values += "Dostepny\',\'" #status
        values += str(self.samochodList[1].text()) + "\',\'" #model
        values += str(self.samochodList[2].text()) + "\'," #marka
        values += str(self.samochodList[3].text()) + "," #przebieg
        values += str(self.samochodList[4].text()) + ",\'" #iloscmiejsc
        values += str(self.samochodList[5].text()) + "\'," #kolor
        values += str(self.samochodList[6].text()) + "," #rocznik
        values += str(self.samochodList[7].text()) + "," #mocsilnika
        values += str(self.samochodList[8].text()) + ",\'" #pojemnosc
        values += str(self.samochodList[9].text()) + "\',\'" #skrzynia
        values += str(self.samochodList[10].text()) + "\',\'" #paliwo
        values += str(self.samochodList[11].text()) + "\',\'" #kraj
        values += str(self.samochodList[12].text()) + "\')" #nadwozie
        sql = "INSERT INTO Samochody " + values

        try:
            cursor.execute(sql)
            database.commit()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Udalo się dodać samochód!")
            msg.setWindowTitle("Informacja")
            msg.exec_()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Wystąpił błąd podczas dodawania!")
            msg.setWindowTitle("Błąd")
            msg.exec_()
            return

    def dodajSamochod(self):

        self.newWindow()
        layout = QGridLayout()
        self.samochodList = []

        nrrejestracyjny = QLineEdit()
        #status = QLineEdit()
        model = QLineEdit()
        marka = QLineEdit()
        przebieg = QLineEdit()
        iloscmiejsc = QLineEdit()
        kolor = QLineEdit()
        rocznik = QLineEdit()
        moc = QLineEdit()
        pojemnosc = QLineEdit()
        skrzynia = QLineEdit()
        paliwo = QLineEdit()
        kraj = QLineEdit()
        typnadwozia = QLineEdit()

        layout.addWidget(nrrejestracyjny,4,1,1,2)
        layout.addWidget(QLabel("Numer rejestracyjny"),4,0,1,1)
        #layout.addWidget(status,4,1,1,2)
        #layout.addWidget(QLabel("Status"),4,0,1,1)
        layout.addWidget(model,5,1,1,2)
        layout.addWidget(QLabel("Model"),5,0,1,1)
        layout.addWidget(marka,6,1,1,2)
        layout.addWidget(QLabel("Marka"),6,0,1,1)
        layout.addWidget(przebieg,7,1,1,2)
        layout.addWidget(QLabel("Przebieg"),7,0,1,1)
        layout.addWidget(iloscmiejsc,8,1,1,2)
        layout.addWidget(QLabel("Ilość miejsc"),8,0,1,1)
        layout.addWidget(kolor,9,1,1,2)
        layout.addWidget(QLabel("Kolor"),9,0,1,1)
        layout.addWidget(rocznik,10,1,1,2)
        layout.addWidget(QLabel("Rocznik"),10,0,1,1)
        layout.addWidget(moc,11,1,1,2)
        layout.addWidget(QLabel("Moc silnika"),11,0,1,1)
        layout.addWidget(pojemnosc,12,1,1,2)
        layout.addWidget(QLabel("Pojemność silnika"),12,0,1,1)
        layout.addWidget(skrzynia,13,1,1,2)
        layout.addWidget(QLabel("Skrzynia biegów"),13,0,1,1)
        layout.addWidget(paliwo,14,1,1,2)
        layout.addWidget(QLabel("Rodzaj paliwa"),14,0,1,1)
        layout.addWidget(kraj,15,1,1,2)
        layout.addWidget(QLabel("Kraj"),15,0,1,1)
        layout.addWidget(typnadwozia,16,1,1,2)
        layout.addWidget(QLabel("Typ nadwozia"),16,0,1,1)

        self.samochodList.append(nrrejestracyjny)
        self.samochodList.append(model)
        self.samochodList.append(marka)
        self.samochodList.append(przebieg)
        self.samochodList.append(iloscmiejsc)
        self.samochodList.append(kolor)
        self.samochodList.append(rocznik)
        self.samochodList.append(moc)
        self.samochodList.append(pojemnosc)
        self.samochodList.append(skrzynia)
        self.samochodList.append(paliwo)
        self.samochodList.append(kraj)
        self.samochodList.append(typnadwozia)

        dodajBtn = QPushButton("DODAJ")
        cofnijBtn = QPushButton("Cofnij")

        layout.addWidget(dodajBtn,17,1,1,2)
        layout.addWidget(cofnijBtn,18,0,1,3)

        dodajBtn.clicked.connect(self.dodajSamochodFun)
        cofnijBtn.clicked.connect(self.backToInterface)

        self.setLayout(layout)
        self.show()


    def updateChoosedDate(self):
        self.dataValue.setText(self.calendar.selectedDate().toString("yyyy-MM-dd"))

    def chooseDate(self):
        self.window = QWidget()
        self.calendar = QCalendarWidget()
        self.calendar.setMinimumDate(QDate(2020, 1, 1))
        self.calendar.setMaximumDate(QDate(3000, 1, 1))

        self.calendar.clicked[QDate].connect(self.updateChoosedDate)

        self.layoutDate = QGridLayout()
       
        self.layoutDate.addWidget(self.calendar)

        self.window.setLayout(self.layoutDate)
        self.window.setFixedSize(500,500)
        moveRight = QPoint(self.rePos.x()+500,self.rePos.y())
        self.window.move(moveRight)
        self.window.setWindowTitle("Kalendarz")
        self.window.show()

    def onWybor(self,index):
        self.__cur_select = index

    def zatwierdzProtokolFun(self):
        cursor.execute('SELECT max(ID_szkody) FROM Protokoly_szkod')
        id = cursor.fetchone()[0]
        if id == None:
            id = 1
        else:
            id += 1

        sql = 'INSERT INTO Protokoly_szkod VALUES (' + str(id) + ',\'' + str(self.dataValue.text()) + '\',\''
        sql += str(self.protokolList[1].toPlainText()) + '\',' + str(self.protokolList[0].text()) + ',' + str(self.protokolList[2][self.__cur_select][4]) + ',' + str(self.protokolList[2][self.__cur_select][5]) + ')'
        try:
            cursor.execute(sql)
            database.commit()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Udalo się dodać protokół!")
            msg.setWindowTitle("Informacja")
            msg.exec_()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Wystąpił błąd podczas dodawania!")
            msg.setWindowTitle("Błąd")
            msg.exec_()
            return


    def dodajProtokol(self):

        self.newWindow()
        layout = QGridLayout()

        self.protokolList = []

        cenaNaprawy = QLineEdit()
        cenaNaprawy.setAlignment(Qt.AlignCenter) 
        cenaNaprawyLabel = QLabel("Cena naprawy: ")
        rodzajSzkody = QTextEdit()
        rodzajSzkodyOpis = QLabel("Opis szkody: ")
        rodzajSzkodyOpis.setAlignment(Qt.AlignCenter) 
        data = QLabel("Wybierz date szkody")
        self.dataValue = QPushButton("- nie wybrano daty -")
        zatwierdzProtokolBtn = QPushButton("DODAJ")
        spacer = QSpacerItem(1,30)

        wypozyczenia=[]
        wybor= QComboBox()
        wyborLabel = QLabel("Wybierz wypożyczenie")
        wybor.currentIndexChanged.connect(self.onWybor)
        sql = "SELECT Data_wypozyczenia, login, nr_rejestracyjny, Wypozyczenia.ID_Uzytkownika, Wypozyczenia.ID_samochodu, ID_wypozyczenia FROM Wypozyczenia "
        sql += "INNER JOIN Użytkownicy ON Wypozyczenia.ID_Uzytkownika = Użytkownicy.ID_Uzytkownika "
        sql += "INNER JOIN Samochody ON Wypozyczenia.ID_samochodu = Samochody.ID_samochodu "

        cursor.execute(sql)
        row=cursor.fetchone()
        while row is not None:
            wypozyczenia.append(row)
            row=cursor.fetchone()
        for i in wypozyczenia:
            wybor.addItem("Data: " + i[0].strftime("%Y-%m-%d") + " Login: " + i[1] + " - " + i[2])
            
        layout.addWidget(data , 0 , 0)
        layout.addWidget(self.dataValue , 0 , 1, 1, 2)
        layout.addWidget(cenaNaprawyLabel, 1 , 0 )
        layout.addWidget(cenaNaprawy, 1, 1)
        layout.addWidget(rodzajSzkody, 2, 1, 2, 2)
        layout.addWidget(rodzajSzkodyOpis, 2, 0, 2, 1)
        layout.addWidget(wybor, 4, 1, 1 , 2)
        layout.addWidget(wyborLabel, 4, 0)
        layout.addItem(spacer, 5, 1)
        layout.addWidget(zatwierdzProtokolBtn, 6, 1, 1, 2)
        layout.addItem(spacer, 7, 1)

        cofnijBtn = QPushButton("Cofnij")
        cofnijBtn.resize(cofnijBtn.sizeHint())

        cofnijBtn.clicked.connect(self.backToInterface)
        zatwierdzProtokolBtn.clicked.connect(self.zatwierdzProtokolFun)
        self.dataValue.clicked.connect(self.chooseDate)

        self.protokolList.append(cenaNaprawy)
        self.protokolList.append(rodzajSzkody)
        self.protokolList.append(wypozyczenia)
        layout.addWidget(cofnijBtn, 8, 0, 1, 4)
        self.setLayout(layout)
        self.show()
    
    def zatwierdzOddajFun(self):

        if(str(self.dataValue.text()) == "- nie wybrano daty -"):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Nie wybrano daty!")
            msg.setWindowTitle("Błąd")
            msg.exec_()
            return

        sql = 'UPDATE Wypozyczenia SET Data_oddania = \'' + str(self.dataValue.text()) + '\' WHERE ID_wypozyczenia = ' + str(self.wypozyczenia[self.__cur_select][0])
        try:
            cursor.execute(sql)
            database.commit()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Wystąpił błąd podczas oddawania!")
            msg.setWindowTitle("Błąd")
            msg.exec_()
            return

        sql = 'UPDATE Samochody SET Status = \'Dostepny\' WHERE ID_samochodu = ' + str(self.wypozyczenia[self.__cur_select][1])

        try:
            cursor.execute(sql)
            database.commit()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Udalo się doddać samochód!")
            msg.setWindowTitle("Informacja")
            msg.exec_()
            sql = "SELECT ID_wypozyczenia, Wypozyczenia.ID_samochodu, login, nr_rejestracyjny, Wypozyczenia.ID_Uzytkownika FROM Wypozyczenia "
            sql += "INNER JOIN Samochody ON Wypozyczenia.ID_samochodu = Samochody.ID_samochodu "
            sql += "INNER JOIN Użytkownicy ON Wypozyczenia.ID_Uzytkownika = Użytkownicy.ID_Uzytkownika WHERE Status = \'Wypozyczony\'"

            self.wybor.clear()
            self.wypozyczenia = []
            cursor.execute(sql)
            row=cursor.fetchone()
            while row is not None:
                self.wypozyczenia.append(row)
                row=cursor.fetchone()
            for i in self.wypozyczenia:
                self.wybor.addItem("ID(" + str(i[0]) + ") Login: " + i[2] + " - " + i[3])
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Wystąpił błąd podczas oddawania!")
            msg.setWindowTitle("Błąd")
            msg.exec_()
            return

    def onWyborOddajFun(self,index):
        self.__cur_select = index
        cursor.execute('SELECT ID_uzytkownika, Imie, Nazwisko, Email, Nr_telefonu FROM Użytkownicy WHERE ID_Uzytkownika = '+ str(self.wypozyczenia[self.__cur_select][4]))
        row=cursor.fetchone()
        self.infoUserText.setText("ID(" + str(row[0]) + ") \n" + str(row[1]) + "  " + str(row[2]) + " \nE-mail: " + str(row[3]) + "\nTelefon: " + str(row[4]))
        cursor.execute('SELECT ID_samochodu, NR_rejestracyjny, Model, Marka, Rocznik FROM Samochody WHERE ID_samochodu = '+ str(self.wypozyczenia[self.__cur_select][1]))
        row=cursor.fetchone()
        self.infoCarText.setText("ID(" + str(row[0]) + ") \nRejestracja: " + str(row[1]) + "\nMarka: " + str(row[3]) + "\nModel: " + str(row[2]) + "\nRocznik: " + str(row[4]))

    def oddajSamochod(self):

        self.newWindow()
        layout = QGridLayout()

        data = QLabel("Wybierz date oddania")
        self.dataValue = QPushButton("- nie wybrano daty -")
        zatwierdzOddajBtn = QPushButton("ODDAJ")
        spacer = QSpacerItem(1,75)
        infoUser = QLabel("Informacje o kliencie")
        self.infoUserText = QLabel()
        infoUser.setAlignment(Qt.AlignCenter)
        self.infoUserText.setAlignment(Qt.AlignCenter)
        infoCar = QLabel("Informacje o samochodze")
        self.infoCarText = QLabel()
        infoCar.setAlignment(Qt.AlignCenter)
        self.infoCarText.setAlignment(Qt.AlignCenter)

        self.wypozyczenia=[]
        self.wybor= QComboBox()
        wyborLabel = QLabel("Wybierz zamowienie")
        self.wybor.currentIndexChanged.connect(self.onWyborOddajFun)
        sql = "SELECT ID_wypozyczenia, Wypozyczenia.ID_samochodu, login, nr_rejestracyjny, Wypozyczenia.ID_Uzytkownika FROM Wypozyczenia "
        sql += "INNER JOIN Samochody ON Wypozyczenia.ID_samochodu = Samochody.ID_samochodu "
        sql += "INNER JOIN Użytkownicy ON Wypozyczenia.ID_Uzytkownika = Użytkownicy.ID_Uzytkownika WHERE Status = \'Wypozyczony\'"

        cursor.execute(sql)
        row=cursor.fetchone()
        while row is not None:
            self.wypozyczenia.append(row)
            row=cursor.fetchone()
        for i in self.wypozyczenia:
            self.wybor.addItem("ID(" + str(i[0]) + ") Login: " + i[2] + " - " + i[3])

        layout.addWidget(data , 0 , 0)
        layout.addWidget(self.dataValue , 0 , 1, 1, 2)
        layout.addWidget(self.wybor, 1, 1, 1 , 2)
        layout.addWidget(wyborLabel, 1, 0)
        layout.addWidget(infoUser, 2, 0, 1, 3)
        layout.addWidget(self.infoUserText, 3, 0, 1, 3)
        layout.addWidget(infoCar, 4, 0, 1, 3)
        layout.addWidget(self.infoCarText, 5, 0, 1, 3)
        layout.addItem(spacer, 6, 1)
        layout.addWidget(zatwierdzOddajBtn, 7, 1)
        layout.addItem(spacer, 8, 1)

        cofnijBtn = QPushButton("Cofnij")
        cofnijBtn.resize(cofnijBtn.sizeHint())

        cofnijBtn.clicked.connect(self.backToInterface)
        zatwierdzOddajBtn.clicked.connect(self.zatwierdzOddajFun)
        self.dataValue.clicked.connect(self.chooseDate)


        layout.addWidget(cofnijBtn, 9, 0, 1, 3)
        self.setLayout(layout)
        self.show()

    def backToInterface(self):
        self.close()
        self.interface()
        self.move(self.rePos)

    def newWindow(self):
        self.close()
        self.__init__()
        self.move(self.rePos)
        self.setFixedSize(500,500)
        self.setWindowTitle("Wypożyczalnia samochodów")

    def onWyborWystawFun(self,index):
        self.__cur_select = index

        cursor.execute('SELECT ID_samochodu, NR_rejestracyjny, Model, Marka, Rocznik FROM Samochody WHERE ID_samochodu = '+ str(self.wypozyczenia[self.__cur_select][0]))

        row=cursor.fetchone()
        self.infoCarText.setText("ID(" + str(row[0]) + ") \nRejestracja: " + str(row[1]) + "\nMarka: " + str(row[3]) + "\nModel: " + str(row[2]) + "\nRocznik: " + str(row[4]))

    def wystawSamochodFun(self):
        cursor.execute('SELECT max(ID_sprzedazy) FROM Sprzedaze')
        id = cursor.fetchone()[0]
        if id == None:
            id = 1
        else:
            id += 1

        sql = 'INSERT INTO Sprzedaze VALUES (' + str(id) + ',' + str(self.price.text()) + ',\'Aktualne\',' + str(self.wypozyczenia[self.__cur_select][0]) + ')'

        try:
            cursor.execute(sql)
            database.commit()
            sql = 'UPDATE Samochody SET Status = \'Sprzedaz\' WHERE ID_samochodu = ' + str(self.wypozyczenia[self.__cur_select][0])
            cursor.execute(sql)
            database.commit()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Udalo się wystawić samochód na sprzedaż!")
            msg.setWindowTitle("Informacja")
            msg.exec_()
            self.wybor.clear()
            self.wypozyczenia = []
            sql = "SELECT ID_samochodu, nr_rejestracyjny FROM Samochody WHERE Status = \'Dostepny\' " 
            cursor.execute(sql)
            row=cursor.fetchone()
            while row is not None:
                self.wypozyczenia.append(row)
                row=cursor.fetchone()
            for i in self.wypozyczenia:
                self.wybor.addItem("ID(" + str(i[0]) + ") Numer rejestracyjny: " + i[1])
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Wystąpił błąd podczas wystawiania samochodu na sprzedaż!")
            msg.setWindowTitle("Błąd")
            msg.exec_()
            return

    def wystawSamochod(self):

        self.newWindow()
        layout = QGridLayout()

        infoCar = QLabel("Informacje o samochodze")
        self.infoCarText = QLabel()
        infoCar.setAlignment(Qt.AlignCenter)
        self.infoCarText.setAlignment(Qt.AlignCenter)
        self.price = QLineEdit()
        priceLabel = QLabel("Podaj cene sprzedaży")
        zatwierdzWystawBtn = QPushButton("WYSTAW")
        spacer = QSpacerItem(1,120)

        self.wypozyczenia=[]
        self.wybor= QComboBox()
        wyborLabel = QLabel("Wybierz samochód")
        self.wybor.currentIndexChanged.connect(self.onWyborWystawFun)
        sql = "SELECT ID_samochodu, nr_rejestracyjny FROM Samochody WHERE Status = \'Dostepny\' "      

        cursor.execute(sql)
        row=cursor.fetchone()
        while row is not None:
            self.wypozyczenia.append(row)
            row=cursor.fetchone()
        for i in self.wypozyczenia:
            self.wybor.addItem("ID(" + str(i[0]) + ") Numer rejestracyjny: " + i[1])
        
        layout.addWidget(wyborLabel, 1, 0, 1, 1)
        layout.addWidget(self.wybor, 1, 1, 1, 2)
        layout.addWidget(priceLabel, 2, 0, 1, 1)
        layout.addWidget(self.price, 2, 1, 1, 2)
        layout.addWidget(infoCar, 3, 0, 1, 3)
        layout.addWidget(self.infoCarText, 4, 0, 1, 3)

        layout.addItem(spacer, 5, 1)
        layout.addWidget(zatwierdzWystawBtn, 6, 1)
        layout.addItem(spacer, 7, 1)

        cofnijBtn = QPushButton("Cofnij")
        cofnijBtn.resize(cofnijBtn.sizeHint())
        layout.addWidget(cofnijBtn, 8, 0, 1, 3)

        zatwierdzWystawBtn.clicked.connect(self.wystawSamochodFun)
        cofnijBtn.clicked.connect(self.backToInterface)


        self.setLayout(layout)
        self.show()

    def interface(self):

        self.__init__()
        layout = QGridLayout()
        font = QFont("Arial",40)
        
        # separatory
        space = QSpacerItem(1,75)
        space1 = QSpacerItem(1,200)

        layout.addItem(space,1,1)
        layout.addItem(space1,7,1)

        # etykiety
        label = QLabel("WYPOZYCZALNIA\nSAMOCHODÓW")
        label.setAlignment(Qt.AlignCenter)
        label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed);
        label.setFont(font)

        layout.addWidget(label, 0, 0,1,3)

        # przyciski
        dodajBtn = QPushButton("Dodaj samochód")
        wypozyczBtn = QPushButton("Wypożycz samochód")
        oddajBtn = QPushButton("Oddaj samochód")
        dodajProtokolBtn = QPushButton("Dodaj protokół szkód")
        wystawBtn = QPushButton("Wystaw na sprzedaż")
        wyjdzBtn = QPushButton("Wyjdź")
        wyjdzBtn.resize(wyjdzBtn.sizeHint())

        layout.addWidget(dodajBtn, 2, 1)
        layout.addWidget(wypozyczBtn, 3, 1)
        layout.addWidget(dodajProtokolBtn, 4, 1)
        layout.addWidget(wystawBtn, 5, 1)
        layout.addWidget(oddajBtn, 6, 1)
        layout.addWidget(wyjdzBtn, 8, 0, 1, 3)

        wystawBtn.clicked.connect(self.wystawSamochod)
        dodajBtn.clicked.connect(self.dodajSamochod)
        wyjdzBtn.clicked.connect(self.close)
        oddajBtn.clicked.connect(self.oddajSamochod)
        dodajProtokolBtn.clicked.connect(self.dodajProtokol)
        wypozyczBtn.clicked.connect(self.f_wyp_sam)

        self.setLayout(layout)
        self.setFixedSize(500,500)
        self.setWindowTitle("Wypożyczalnia samochodów")
        self.show()




if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    aplikacja = Wypozyczalnia()
    aplikacja.interface()
    sys.exit(app.exec_())