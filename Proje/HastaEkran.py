from tkinter import *
from tkinter import ttk
import pymysql
from tkinter import messagebox
import HastalıkTahmin
import RandevuAlmaEkran
def page():
    class Hastalar:
        def __init__(self, root):

            self.root = root
            self.root.title("ANA SAYFA")
            root.geometry("1000x650")

            title = Label(self.root, text="ANA SAYFA", bd=10, relief=GROOVE,font=("times new roman", 40, "bold"),
                          fg="#375466", bg="#74CE98")
            title.pack(side=TOP,fill=X)

            self.id2 = StringVar()
            self.isim2 = StringVar()
            self.soyad2 = StringVar()
            self.cinsiyet2 = StringVar()
            self.tckimlik2 = StringVar()
            self.dogumgunu2 = StringVar()
            self.sifre2 = StringVar()
            self.search_by = StringVar()
            global a

            # KAYIT OLMA CERCEVESI
            Kayıt_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="#A7DABD")
            Kayıt_Frame.place(x=20, y=100, width=470, height=500)

            kayıt_title = Label(Kayıt_Frame, text="HASTA ISLEMLERI", bg="#A7DABD", fg="#375466",font=("times new roman", 15, "bold"))
            kayıt_title.place(x=5, y=5)

            lbl_id2 = Label(Kayıt_Frame, text="ID", bg="#A7DABD", fg="#375466", font=("times new roman", 12, "bold"))
            lbl_id2.place(x=5, y=40)
            self.id2 = Text(Kayıt_Frame, font=("times new roman", 10, "bold"))
            self.id2.place(x=120, y=40, width=300, height=30)

            lbl_ad = Label(Kayıt_Frame, text="Ad", bg="#A7DABD", fg="#375466", font=("times new roman", 12, "bold"))
            lbl_ad.place(x=5, y=80)
            self.isim2 = Text(Kayıt_Frame, font=("times new roman", 10, "bold"))
            self.isim2.place(x=120, y=80, width=300, height=30)

            lbl_soyad = Label(Kayıt_Frame, text="Soyad", bg="#A7DABD", fg="#375466", font=("times new roman", 12, "bold"))
            lbl_soyad.place(x=5, y=120)
            self.soyad2 = Text(Kayıt_Frame, font=("times new roman", 12, "bold"))
            self.soyad2.place(x=120, y=120, width=300, height=30)

            lbl_cinsiyet = Label(Kayıt_Frame, text="Cinsiyet", bg="#A7DABD", fg="#375466", font=("times new roman", 12, "bold"))
            lbl_cinsiyet.place(x=5, y=160)
            combo_cinsiyet = ttk.Combobox(Kayıt_Frame, textvariable=self.cinsiyet2, font=("times new roman", 10, "bold"),state="readonly")
            combo_cinsiyet['values'] = ("Erkek", "Kadın", "diger")
            combo_cinsiyet.place(x=120, y=160, width=300, height=30)

            lbl_tckimlik = Label(Kayıt_Frame, text="TC Kimlik", bg="#A7DABD", fg="#375466",font=("times new roman", 12, "bold"))
            lbl_tckimlik.place(x=5, y=200)
            self.tckimlik2 = Text(Kayıt_Frame, font=("times new roman", 10, "bold"))
            self.tckimlik2.place(x=120, y=200, width=300, height=30)

            lbl_dob = Label(Kayıt_Frame, text="Dogum Tarihi", bg="#A7DABD", fg="#375466", font=("times new roman", 12, "bold"))
            lbl_dob.place(x=5, y=240)
            self.dogumgunu2 = Text(Kayıt_Frame, font=("times new roman", 10, "bold"))
            self.dogumgunu2.place(x=120, y=240, width=300, height=30)

            lbl_sifre = Label(Kayıt_Frame, text="Sifre", bg="#A7DABD", fg="#375466",font=("times new roman", 12, "bold"))
            lbl_sifre.place(x=5, y=280)
            self.sifre2 = Text(Kayıt_Frame, width=30, height=4, font=("", 10))
            self.sifre2.place(x=120, y=280, width=300, height=30)


            Button_Frame = Frame(Kayıt_Frame, bd=4, relief=RIDGE, bg="#A7DABD")
            Button_Frame.place(x=90, y=420, width=290)
            guncellebtn = Button(Button_Frame, text="Guncelle",font=("times new roman", 12, "bold"),fg="#375466", width=8, command=self.hesapGuncelle).grid(row=0, column=1, padx=5,pady=5)
            silbtn = Button(Button_Frame, text="Sil",font=("times new roman", 12, "bold"),fg="#375466", width=8, command=self.hesapSil).grid(row=0, column=2, padx=5,pady=5)
            temizlebtn = Button(Button_Frame, text="Temizle",font=("times new roman", 12, "bold"),fg="#375466", width=8, command=self.temizle).grid(row=0, column=3, padx=5, pady=5)


            ##ISLEMLER CERCEVESİ
            Islemler_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="#A7DABD")
            Islemler_Frame.place(x=500, y=100, width=470, height=500)

            ıslemler_title = Label(Islemler_Frame, text="HOS GELDINIZ...\nMenu", bg="#A7DABD", fg="#375466",
                                font=("times new roman", 15, "bold"))
            ıslemler_title.place(x=5, y=5)
            profilimegitbtn = Button(Islemler_Frame, text="Profilime Git",font=("times new roman", 25, "bold"),fg="#375466",width=15, command=self.hesapGuncelle)
            profilimegitbtn.place(x=50, y=100, width=350, height=50)
            randevualbtn = Button(Islemler_Frame, text="Randevu Al", font=("times new roman", 25, "bold"),fg="#375466",width=15, command=self.randevucagir)
            randevualbtn.place(x=50, y=200, width=350, height=50)
            hastaliktahminbtn = Button(Islemler_Frame, text="Hastalık Tahmin", font=("times new roman", 25, "bold"),fg="#375466",width=15, command = self.cagir)
            hastaliktahminbtn.place(x=50, y=300, width=350, height=50)
            cikisbtn = Button(Islemler_Frame, text="Cıkıs Yap", font=("times new roman", 25, "bold"),fg="#375466", width=15, command = self.kapat)
            cikisbtn.place(x=50, y=400, width=350, height=50)

        def cagir(self):
            a=1
            if a ==1:
                HastalıkTahmin.tahminPage()
        def randevucagir(self):
            a =2
            if a ==2:
                RandevuAlmaEkran.RandevuPage()

        def kapat(self):
            root.destroy()

        def temizle(self):
            self.id2.delete('1.0', END)
            self.isim2.delete('1.0', END)
            self.soyad2.delete('1.0', END)
            self.cinsiyet2.set("")
            self.tckimlik2.delete('1.0', END)
            self.dogumgunu2.get('1.0', END)
            self.sifre2.delete('1.0', END)

        def hesapGuncelle(self):
            con = pymysql.connect(host="localhost",user='root',password='',db="saglik")
            cur = con.cursor()
            cur.execute("UPDATE uyeler SET ad=%s, soyad=%s,tckimlik = %s, cinsiyet=%s, dogumtarihi=%s, sifre=%s where iduyeler=%s",
                            (self.isim2.get('1.0', END), self.soyad2.get('1.0', END), self.tckimlik2.get('1.0', END), self.cinsiyet2.get(),
                            self.dogumgunu2.get('1.0', END), self.sifre2.get('1.0', END),self.id2.get('1.0', END),))

            con.commit()
            self.temizle()
            con.close()
            messagebox.showinfo("Basarili", "Kayit Guncellendi")

        def hesapSil(self):
            con = pymysql.connect(host="localhost",user='root',password='',db="saglik")
            cur = con.cursor()
            cur.execute("DELETE FROM uyeler where iduyeler = '%s'" %(self.id2.get('1.0', END)))
            con.commit()
            con.close()
            messagebox.showinfo("Basarili", "Kayit Silindi")

    root = Tk()
    obj = Hastalar(root)
    root.mainloop()
