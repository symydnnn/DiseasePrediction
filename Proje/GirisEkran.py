from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import HastaEkran

##GIRIS EKRANI METHODLARI
def temizle():
    tckimlikgiris.delete(0, END)
    sifregiris.delete(0, END)

def girisEkraniKapat():
    girisEkranı.destroy()

def giris():
    if tc_.get() == "" or sifre_.get() == "":
        messagebox.showerror("Hata!", "TC Kimlik ve Sifre Bolumleri Bos Birakilamaz", parent=girisEkranı)
    else:
        try:
            con = pymysql.connect(host="localhost", user="root",password="", database="saglik")
            cur = con.cursor()
            cur.execute("select * from uyeler where tckimlik=%s and sifre = %s", (tc_.get(), sifre_.get()))
            row = cur.fetchone()

            if row == None:
                messagebox.showerror("Hata!", "Geçersiz TC kimlik veya şifre", parent=girisEkranı)
            else:
                messagebox.showinfo("Başarılı", "Giriş Başarılı!", parent=girisEkranı)
                girisEkraniKapat()
                con.close()
                HastaEkran.page()

            con.close()
        except Exception as es:
            messagebox.showerror("Hata!", f"Hata nedeni : {str(es)}", parent=girisEkranı)


##KAYIT EKRANI METHODLARI

def kayit():
    def kayitOl():
        try:
            con = pymysql.connect(host="localhost", user="root", password="", database="saglik")
            cur = con.cursor()
            cur.execute("select * from uyeler where tckimlik=%s", tckimlik.get())
            row = cur.fetchone()
            cur.execute("INSERT INTO uyeler(ad,soyad,tckimlik,cinsiyet,dogumtarihi,sifre) VALUES(%s,%s,%s,%s,%s,%s)",
                        (   ad.get(),
                            soyad.get(),
                            tckimlik.get(),
                            cinsiyet.get(),
                            dob.get(),
                            sifre.get()
                        ))
            con.commit()
            con.close()
            messagebox.showinfo("Başarılı", "Kayıt Başarılı", parent=kayıtEkranı)
            temizle()
            degistir()

        except Exception as es:
            messagebox.showerror("Hata!", f"Hata nedeni : {str(es)}", parent=kayıtEkranı)


    def degistir():
        kayıtEkranı.destroy()


    def temizle():
        ad.delete(0, END)
        soyad.delete(0, END)
        tckimlik.delete(0, END)
        cinsiyet.set("Kadın")
        dob.delete(0, END)
        sifre.delete(0, END)

    ##KAYIT EKRANI

    kayıtEkranı = Tk()
    kayıtEkranı.configure(bg='#A7DABD')
    kayıtEkranı.title("Kayıt Ol")
    kayıtEkranı.maxsize(width=500, height=500)
    kayıtEkranı.minsize(width=500, height=500)
    baslik2 = Label(kayıtEkranı, text="Kayıt Ol", bg='#A7DABD', fg="#375466",font='Verdana 20 bold')
    baslik2.place(x=80, y=60)

    ad = Label(kayıtEkranı, text="Ad :", bg='#A7DABD', fg="#375466",font='Verdana 10 bold')
    ad.place(x=80, y=130)

    soyad = Label(kayıtEkranı, text="Soyad :", bg='#A7DABD', fg="#375466",font='Verdana 10 bold')
    soyad.place(x=80, y=160)

    tckimlik = Label(kayıtEkranı, text="Tc Kimlik :", bg='#A7DABD', fg="#375466",font='Verdana 10 bold')
    tckimlik.place(x=80, y=190)

    cinsiyet = Label(kayıtEkranı, text="Cinsiyet :", bg='#A7DABD', fg="#375466",font='Verdana 10 bold')
    cinsiyet.place(x=80, y=220)

    dob = Label(kayıtEkranı, text="Doğum Tarihi :", bg='#A7DABD', fg="#375466",font='Verdana 10 bold')
    dob.place(x=80, y=260)

    sifre = Label(kayıtEkranı, text="Şifre :", bg='#A7DABD', fg="#375466",font='Verdana 10 bold')
    sifre.place(x=80, y=290)


    ad = StringVar()
    soyad = StringVar()
    tckimlik = StringVar()
    cinsiyet = StringVar()
    dob = StringVar()
    sifre = StringVar()
    ad = Entry(kayıtEkranı, width=40, textvariable=ad)
    ad.place(x=200, y=133)

    soyad = Entry(kayıtEkranı, width=40, textvariable=soyad)
    soyad.place(x=200, y=163)

    tckimlik = Entry(kayıtEkranı, width=40, textvariable=tckimlik)
    tckimlik.place(x=200, y=193)

    cinsiyet = ttk.Combobox(kayıtEkranı, textvariable=cinsiyet, font=("times new roman", 10, "bold"),
                            state="readonly")
    cinsiyet['values'] = ("Erkek", "Kadın", "diger")
    cinsiyet.place(x=200, y=220, width=250, height=20)

    dob = Entry(kayıtEkranı, width=40, textvariable=dob)
    dob.place(x=200, y=263)

    sifre = Entry(kayıtEkranı, width=40, textvariable=sifre)
    sifre.place(x=200, y=293)

    kayitbtn = Button(kayıtEkranı, text="Kayıt Ol", font='Verdana 10 bold', fg="#375466",command=kayitOl)
    kayitbtn.place(x=150, y=350,width=100, height=50)

    girisbtn = Button(kayıtEkranı, text="Temizle", font='Verdana 10 bold', fg="#375466",command=temizle)
    girisbtn.place(x=280, y=350,width=100, height=50)

    kayitolbtn = Button(kayıtEkranı, text="Giriş Ekranı", fg="#375466",font='Verdana 10 bold',command=degistir)
    kayitolbtn.place(x=350, y=20,width=100, height=50)

    kayıtEkranı.mainloop()

## GIRIS EKRANI

girisEkranı = Tk()

girisEkranı.title("Giriş Ekranı")
girisEkranı.configure(bg='#A7DABD')
girisEkranı.maxsize(width=500, height=300)
girisEkranı.minsize(width=500, height=300)

baslik = Label(girisEkranı, text="GIRIS YAP", bg='#A7DABD', fg="#375466",font='Verdana 25 bold')
baslik.place(x=80, y=50)

tckimliklbl = Label(girisEkranı, text="TC Kimlik No :", bg='#A7DABD',fg="#375466", font='Verdana 10 bold')
tckimliklbl.place(x=80, y=120)

sifrelbl = Label(girisEkranı, text="Şifre :", bg='#A7DABD',fg="#375466", font='Verdana 10 bold')
sifrelbl.place(x=80, y=160)

tc_ = StringVar()
sifre_ = StringVar()

tckimlikgiris = Entry(girisEkranı, width=40, textvariable=tc_)
tckimlikgiris.focus()
tckimlikgiris.place(x=200, y=123)

sifregiris = Entry(girisEkranı, width=40, show="*", textvariable=sifre_)
sifregiris.place(x=200, y=160)

girisbtn = Button(girisEkranı, text="Giriş Yap", font='Verdana 10 bold', fg="#375466", command=giris)
girisbtn.place(x=350, y=193, width=100, height=50)

girisbtn = Button(girisEkranı, text="Temizle", font='Verdana 10 bold', fg="#375466", command=temizle)
girisbtn.place(x=100, y=193, width=100, height=50)

kayitolbtn = Button(girisEkranı, text="Kayıt Ol", font='Verdana 10 bold', fg="#375466", command=kayit)
kayitolbtn.place(x=225, y=193, width=100, height=50)

girisEkranı.mainloop()