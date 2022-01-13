import pymysql
from tkinter import *
from tkinter import ttk
import pymysql
from tkinter import messagebox

def RandevuPage():
    class Randevu:
        def __init__(self, root):
            self.root = root
            self.root.title("Randevu Alma Ekranı")
            root.geometry("1300x700+0+0")

            title = Label(self.root, text="RANDEVU ALMA", bd=10, relief=GROOVE,
                          font=("times new roman", 40, "bold"), bg="#A7DABD", fg="#375466")
            title.pack(side=TOP, fill=X)

            self.idpoliklinik = StringVar()
            self.poladi = StringVar()
            self.hastaneadi = StringVar()
            self.tckimlik = StringVar()

            RandevuAlma_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="#A7DABD")
            RandevuAlma_Frame.place(x=20, y=100, width=1250, height=500)

            ra_title = Label(RandevuAlma_Frame, text="Randevu Secme", bg="#A7DABD", fg="#375466",
                            font=("times new roman", 20, "bold"))
            ra_title.grid(row=0, columnspan=2, pady=20)

            lbl_id = Label(RandevuAlma_Frame, text="Poliklinik ID", bg="#A7DABD", fg="#375466", font=("times new roman", 18, "bold"))
            lbl_id.grid(row=1, column=0, padx=20, pady=10, sticky="w")
            txt_id = Entry(RandevuAlma_Frame, textvariable=self.idpoliklinik, font=("times new roman", 18, "bold"), bd=5,
                             relief=GROOVE)
            txt_id.grid(row=1, column=1, padx=20, pady=10, sticky="w")

            lbl_polad = Label(RandevuAlma_Frame, text="Polikinlik Adı", bg="#A7DABD", fg="#375466", font=("times new roman", 18, "bold"))
            lbl_polad.grid(row=2, column=0, padx=20, pady=10, sticky="w")
            txt_polad = Entry(RandevuAlma_Frame, textvariable=self.poladi, font=("times new roman", 18, "bold"), bd=5,
                             relief=GROOVE)
            txt_polad.grid(row=2, column=1, padx=20, pady=10, sticky="w")

            lbl_hstad = Label(RandevuAlma_Frame, text="Hastane Adı", bg="#A7DABD", fg="#375466", font=("times new roman", 18, "bold"))
            lbl_hstad.grid(row=3, column=0, padx=20, pady=10, sticky="w")
            txt_hstad = Entry(RandevuAlma_Frame, textvariable=self.hastaneadi, font=("times new roman", 18, "bold"), bd=5,
                              relief=GROOVE)
            txt_hstad.grid(row=3, column=1, padx=20, pady=10, sticky="w")

            lbl_tc = Label(RandevuAlma_Frame, text="TC Kimlik", bg="#A7DABD", fg="#375466",
                                font=("times new roman", 18, "bold"))
            lbl_tc.grid(row=5, column=0, padx=20, pady=10, sticky="w")
            txt_tc = Entry(RandevuAlma_Frame, textvariable=self.tckimlik, font=("times new roman", 18, "bold"), bd=5,
                                relief=GROOVE)
            txt_tc.grid(row=5, column=1, padx=20, pady=10, sticky="w")

            Table_Frame = Frame(RandevuAlma_Frame, bd=4, relief=RIDGE, bg="#A7DABD")
            Table_Frame.place(x=500, y=60, width=700, height=300)

            scroll_x = Scrollbar(Table_Frame, orient=HORIZONTAL)
            scroll_y = Scrollbar(Table_Frame, orient=VERTICAL)

            self.Polikinlikler_Table = ttk.Treeview(Table_Frame,columns=("idpoliklinik", "poladi", "hastaneadi"),
                                              xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
            scroll_x.pack(side=BOTTOM, fill=X)
            scroll_y.pack(side=RIGHT, fill=Y)
            scroll_x.config(command=self.Polikinlikler_Table.xview)
            scroll_y.config(command=self.Polikinlikler_Table.yview)
            self.Polikinlikler_Table.heading("idpoliklinik", text="ID")
            self.Polikinlikler_Table.heading("poladi", text="Poliklinik Adı")
            self.Polikinlikler_Table.heading("hastaneadi", text="Hastane Adı")
            self.Polikinlikler_Table['show'] = 'headings'  # removing extra index col at begining

            self.Polikinlikler_Table.column("idpoliklinik", width=100)
            self.Polikinlikler_Table.column("poladi", width=100)
            self.Polikinlikler_Table.column("hastaneadi", width=100)
            self.Polikinlikler_Table.pack(fill=BOTH, expand=1)
            self.Polikinlikler_Table.bind("<ButtonRelease-1>", self.tabloyaEkle)

            self.polikinlikleriGetir()

            randevueklebtn = Button(RandevuAlma_Frame, text="Randevu Al", font=("times new roman", 25, "bold"),
                                     fg="#375466", width=15, command=self.randevuEkle)
            randevueklebtn.place(x=50, y=350, width=330, height=50)


        def polikinlikleriGetir(self):
            con = pymysql.connect(host="localhost", user="root", password="", database="saglik")
            cur = con.cursor()
            cur.execute("select * from poliklinik")
            rows = cur.fetchall()
            if (len(rows) != 0):
                self.Polikinlikler_Table.delete(*self.Polikinlikler_Table.get_children())
                for row in rows:
                    self.Polikinlikler_Table.insert('', END, values=row)
                con.commit()
            con.close()

        def tabloyaEkle(self, evnt):
            cursor_row = self.Polikinlikler_Table.focus()
            content = self.Polikinlikler_Table.item(cursor_row)
            row = content['values']
            self.idpoliklinik.set(row[0])
            self.poladi.set(row[1])
            self.hastaneadi.set(row[2])

        def randevuEkle(self):
            con = pymysql.connect(host="localhost", user="root", password="", database="saglik")
            cur = con.cursor()
            cur.execute("select * from uyeler where tckimlik=%s", self.tckimlik.get())
            row = cur.fetchone()
            cur.execute("INSERT INTO randevualma(polikinlikid,tckimlik) VALUES(%s,%s)",
                        (self.idpoliklinik.get(),self.tckimlik.get()))
            con.commit()
            con.close()
            messagebox.showinfo("Başarılı", "Randevu Alındı")

    root = Tk()
    obj = Randevu(root)
    root.mainloop()

