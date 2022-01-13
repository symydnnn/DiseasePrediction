from tkinter import *
import numpy as np
import pandas as pd
import fsspec
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score,KFold
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from catboost import CatBoostClassifier

def tahminPage():
    # TAHMIN YAPILACAK EKRAN
    tahminPencere = Tk()
    tahminPencere.title("HASTALIK TAHMIN")
    tahminPencere.geometry("600x450")

    Hastalik_Tahmin_Frame = Frame(tahminPencere, bd=4, relief=RIDGE, bg="#A7DABD")
    Hastalik_Tahmin_Frame.place(x=50, y=50, width=500, height=350)

    semptom1 = StringVar()
    semptom2 = StringVar()
    semptom3 = StringVar()
    semptom4 = StringVar()
    semptom5 = StringVar()
    lb_semptom1 = StringVar()
    lb_semptom2 = StringVar()
    lb_semptom3 = StringVar()
    lb_semptom4 = StringVar()
    lb_semptom5 = StringVar()
    teshis1 = StringVar()
    teshis2 = StringVar()

    ##TAHMIN KISIM
    dataset = pd.read_csv("C://Users//seyma//OneDrive//Masaüstü//hastalikTahmin//hastalikbuyuksett.csv")

        ##Semptomlar eklendi.
    semptomlar = dataset.columns.drop('teshis')

        ##Yeni gelecek data için list oluşturuldu.
    yeni_data = []
    for i in range(0, len(semptomlar)):
        yeni_data.append(0)

        ##Veri setinden hastalıklar listesi oluşturuldu. Veri setinde birden çok bulunan hastalıkların
        # sadece bir kez olduğu hasta listesi oluşturuldu ve bununla beraber onlara verilecek numaraların tutulduğu
        # a listesi kaydedildi.
    hastalik = []
    l = dataset.values.tolist()
    for i in l:
        for n in i:
            c = str(n)
            if c.isdigit():
                continue
            else:
                hastalik.append(n)
    hasta = []
    sayi = []
    a = 0
    for i in hastalik:
        if i not in hasta:
            hasta.append(i)
            sayi.append(a)
            a = a + 1


    ##teshislerde hastalıklar numaralara göre eşleştirilip datasete kaydedildi.
    for i in range(0, len(hasta)):
        dataset.replace({'teshis': {hasta[i]: i}}, inplace=True)

        ##X'e datasetin semptomlar kısmı, y'ye ise teshisler eklendi
    X = dataset[semptomlar]
    y = dataset["teshis"]

    # model eğitimi için test ve eğitim verileri %20 oranında paylaştırıldı. Random ataması 42 ayarlandı.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, )

    # Kullanılabilecek algoritmalarla model test edildi.
    modeller = [
        ('LR', LogisticRegression()),
        ('NB', GaussianNB()),
        ('KNN', KNeighborsClassifier(n_neighbors=3)),
        ('ABC', AdaBoostClassifier()),
        ('DTC', DecisionTreeClassifier()),
        ('CatBoost', CatBoostClassifier(iterations=5, ))]

    isimler = []
    sonuclar = []
    for isim, model in modeller:
        kfold = KFold(n_splits=10, shuffle=True, random_state=42)
        cv_sonuclar = cross_val_score(model, X_train, y_train, cv=kfold, scoring='accuracy')
        isimler.append(isim)
        sonuclar.append(cv_sonuclar)
        print("Algoritma: %s / Başarım: %f / Std: %f" % (isim, cv_sonuclar.mean(), cv_sonuclar.std()))

        # Başarım oranları yazdırıldı.

    # Tahmin için seçilen Desicion Tree ve Naive Bayes algoritmaları tahminEt methoduna aktarıldı.
    def tahminEt():
        dtc = DecisionTreeClassifier()
        dtc = dtc.fit(X, y)
        y_pred = dtc.predict(X_test)
        print("Desicion Tree Dogruluk: ", accuracy_score(y_test, y_pred))

        gnb = GaussianNB()
        gnb = gnb.fit(X, y)
        y_pred = gnb.predict(X_test)
        print("Naive Bayes Dogruluk: ", accuracy_score(y_test, y_pred))

        psymptoms = [semptom1.get(), semptom2.get(), semptom3.get(), semptom4.get(),
                     semptom5.get()]
        for k in range(0, len(semptomlar)):
            for z in psymptoms:
                if (z == semptomlar[k]):
                    yeni_data[k] = 1

        ##Desicion Tree yeni data testi:
        test = np.array(yeni_data)
        test = test.reshape(1, -1)
        predict = dtc.predict(test)
        predicted = predict[0]

        ##Naive Bayes yeni data testi:
        yeni_test = [yeni_data]
        yeni_test = np.array(yeni_test).reshape(1, -1)
        predict1 = gnb.predict(yeni_test)
        predicted1 = predict[0]

        gnb_kontrol = 0
        dtc_kontrol = 0
        for a in range(0, len(hastalik)):
            if (predicted == a):
                gnb_kontrol = 1
                ##break
            if (predicted == a):
                b = a
                dtc_kontrol = 1


        if (gnb_kontrol == 1):
            teshis1.delete("1.0", END)
            teshis1.insert(END, hastalik[a])
            print(hastalik[a])
        else:
            teshis1.delete("1.0", END)
            teshis1.insert(END, "Teshis Edilemedi")


        if (dtc_kontrol == 1):
            teshis2.delete("1.0", END)
            teshis2.insert(END, hastalik[b])
            print(hastalik[b])
        else:
            teshis2.delete("1.0", END)
            teshis2.insert(END, "Teshis Edilemedi")


    semptom1.set("SECIM")
    semptom2.set("SECIM")
    semptom3.set("SECIM")
    semptom4.set("SECIM")
    semptom5.set("SECIM")

    w2 = Label(Hastalik_Tahmin_Frame, justify=LEFT, text="HASTALIK TAHMINI", fg="#375466", bg="#A7DABD")
    w2.grid(row=1, column=0, columnspan=2, padx=100)
    w2.config(font=("Times", 20, "bold"))

    semptom_secenekler = sorted(semptomlar)

    lb_semptom1 = Label(Hastalik_Tahmin_Frame, width=8, text="Semptom", bg="#A7DABD", fg="#375466",
                        font=("times new roman", 13, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="w")
    lb_semptom2 = Label(Hastalik_Tahmin_Frame, width=8, text="Semptom", bg="#A7DABD", fg="#375466",
                        font=("times new roman", 13, "bold")).grid(row=3, column=0, padx=5, pady=5, sticky="w")
    lb_semptom3 = Label(Hastalik_Tahmin_Frame, width=8, text="Semptom", bg="#A7DABD", fg="#375466",
                        font=("times new roman", 13, "bold")).grid(row=4, column=0, padx=5, pady=5, sticky="w")
    lb_semptom4 = Label(Hastalik_Tahmin_Frame, width=8, text="Semptom", bg="#A7DABD", fg="#375466",
                        font=("times new roman", 13, "bold")).grid(row=5, column=0, padx=5, pady=5, sticky="w")
    lb_semptom5 = Label(Hastalik_Tahmin_Frame, width=8, text="Semptom", bg="#A7DABD", fg="#375466",
                        font=("times new roman", 13, "bold")).grid(row=6, column=0, padx=5, pady=5, sticky="w")

    S1 = OptionMenu(Hastalik_Tahmin_Frame, semptom1, *semptom_secenekler)
    S1.grid(row=2, column=1)
    S2 = OptionMenu(Hastalik_Tahmin_Frame, semptom2, *semptom_secenekler)
    S2.grid(row=3, column=1)
    S3 = OptionMenu(Hastalik_Tahmin_Frame, semptom3, *semptom_secenekler)
    S3.grid(row=4, column=1)
    S4 = OptionMenu(Hastalik_Tahmin_Frame, semptom4, *semptom_secenekler)
    S4.grid(row=5, column=1)
    S5 = OptionMenu(Hastalik_Tahmin_Frame, semptom5, *semptom_secenekler)
    S5.grid(row=6, column=1)

    dst = Button(Hastalik_Tahmin_Frame, text="SONUC BUL", command=tahminEt, bg="#33664D", fg="#FEFFC7")
    dst.grid(row=8, column=1, padx=20)

    teshis1 = Text(Hastalik_Tahmin_Frame, height=1, width=30, bg="#B3D4B6", fg="#3B6E45")
    teshis1.config(font=("Times", 15, "bold"))
    teshis1.grid(row=10, column=1, padx=10)

    teshis2 = Text(Hastalik_Tahmin_Frame, height=1, width=30, bg="#CED4B3", fg="#3B6E45")
    teshis2.config(font=("Times", 15, "bold italic"))
    teshis2.grid(row=12, column=1, padx=5)

    tahminPencere.mainloop()

tahminPage()