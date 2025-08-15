import tkinter as tk
from tkinter import Menu
import sqlite3
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
#--------------------Ana pencere----------------------
root=tk.Tk()
root.title("🏥 DOKTOR KAYIT !FORM!")
root.geometry("1000x800+300+200")
#-----------------------------------------------------


secilenHasta=None
secilenDoktor=None
secilenTarih=None


hastalarVeritabani=sqlite3.connect("hastalar.db")
cur=hastalarVeritabani.cursor()
cur.execute(''' 
            
      CREATE TABLE IF NOT EXISTS hastalar(
          kimlik INTEGER PRIMARY KEY AUTOINCREMENT,
          ad TEXT,
          soyad TEXT,
          yas INTEGER,
          cinsiyet TEXT
      ) 
            
            ''')

hastalarVeritabani.commit()
hastalarVeritabani.close()



#DATABASE
doktorlarVeritabani=sqlite3.connect("doktorlar.db")
cur=doktorlarVeritabani.cursor()
cur.execute(''' 

    CREATE TABLE IF NOT EXISTS doktorlar(
            kimlik INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT,
            soyad TEXT,
            yas INTEGER,
            cinsiyet TEXT
            )


''')

doktorlarVeritabani.commit()
doktorlarVeritabani.close()

#---------------sql kodları yazılacak-------------------

def HastaKayit():
    hastaKayitEkrani=tk.Toplevel()
    hastaKayitEkrani.title("Hasta Kayıt")
    hastaKayitEkrani.geometry("500x500+300+200")
    
    def kaydet():
        ad=hastaAdi.get()
        soyad=hastaSoyadi.get()
        yas=hastaYas.get()
        cinsiyet=hastaCinsiyet.get()
        
        hastalarVeritabani=sqlite3.connect("hastalar.db")
        cur=hastalarVeritabani.cursor()
        cur.execute(''' 
                INSERT INTO hastalar(ad,soyad,yas,cinsiyet) VALUES(?,?,?,?)
            
            ''', (ad,soyad,yas,cinsiyet) )

        hastalarVeritabani.commit()
        hastalarVeritabani.close()
        messagebox.showinfo("Kayıt Başarılı👍"," Hasta kaydı başarıyla gerçekleşmiştir")

        hastaKayitEkrani.after(3000,hastaKayitEkrani.destroy)
        
    
    baslikFrame=tk.Frame(hastaKayitEkrani,width=500,height=40,background="#8a2424")
    baslikFrame.place(x=0,y=0)
    hastaneName=tk.Label(baslikFrame,text="Digi Hospital",font=("Georgia",16,"bold"),fg="white",background="#8a2424")
    hastaneName.place(x=30,y=7)
    
    tk.Label(hastaKayitEkrani,text="HASTA KAYIT İŞLEMİ", font=("Arial",13),fg="#8a2424").place(x=30,y=60)
    
    footer=tk.Frame(hastaKayitEkrani,width=500,height=100,background="#8a2424")
    footer.place(x=0,y=400)
    
    hastaAdi=tk.Label(hastaKayitEkrani,text="Adınız:")
    hastaAdi.place(x=30,y=100)
    hastaAdi=tk.Entry(hastaKayitEkrani)
    hastaAdi.place(x=150,y=100)
    
    hastaSoyadi=tk.Label(hastaKayitEkrani,text="Soyadınız:")
    hastaSoyadi.place(x=30,y=140)
    hastaSoyadi=tk.Entry(hastaKayitEkrani)
    hastaSoyadi.place(x=150,y=140)
    
    hastaYas=tk.Label(hastaKayitEkrani,text="Yaşınız:")
    hastaYas.place(x=30,y=180)
    hastaYas=tk.Entry(hastaKayitEkrani)
    hastaYas.place(x=150,y=180)
    
    hastaCinsiyet=tk.Label(hastaKayitEkrani,text="Cinsiyetniz:")
    hastaCinsiyet.place(x=30,y=220)
    hastaCinsiyet=tk.Entry(hastaKayitEkrani)
    hastaCinsiyet.place(x=150,y=220)
    
    kaydetButon=tk.Button(hastaKayitEkrani,text="KAYDET",command=kaydet)
    kaydetButon.place(x=30,y=260)


def HastaListeleme():
    listelemeEkrani=tk.Toplevel()
    listelemeEkrani.geometry("400x600+200+200")
    listelemeEkrani.title("HASTA LİSTE EKRANI")
    
    tk.Label(listelemeEkrani,text="HASTALARIMIZ",fg="red",font=("Georgia",14)).place(x=120,y=20)
    
    listem=tk.Listbox(listelemeEkrani,width=35,height=30)
    listem.place(x=30,y=60)
    
    hastalarVeritabani=sqlite3.connect("hastalar.db")
    cur=hastalarVeritabani.cursor()
    cur.execute(''' 
             SELECT * FROM hastalar
            
            ''' )

    hastaBilgileri=cur.fetchall()    
    hastalarVeritabani.close()
    
    for hasta in hastaBilgileri:
        duzenliBilgi=f"{hasta[0]}       {hasta[1]}         {hasta[2]}"
        listem.insert(tk.END,duzenliBilgi)
        
    
    def guncelle():
        guncellemeEkrani=tk.Toplevel()
        guncellemeEkrani.geometry("500x600+200+300")
        guncellemeEkrani.title("KAYIT GUNCELLEME EKRANI")
        
        secilen=listem.curselection()
        siraNumarasi=secilen[0]
        bilgi=hastaBilgileri[siraNumarasi]   
        
        
        def guncellemeIslemi():
            
            ad=hastaAdi.get()
            soyad=hastaSoyadi.get()
            yas=hastaYas.get()
            cinsiyet=hastaCinsiyet.get()
            
            hastalarVeritabani=sqlite3.connect("hastalar.db")
            cur=hastalarVeritabani.cursor()
            cur.execute(''' 
                    
                UPDATE hastalar SET ad=?,soyad=?,yas=?,cinsiyet=? WHERE kimlik=?
                ''', (ad,soyad,yas,cinsiyet,bilgi[0]) )

            hastalarVeritabani.commit()
            hastalarVeritabani.close()
            
            
            
            messagebox.showinfo("Güncelleme Başarılı👍"," Hasta kaydı başarıyla güncellenmiştir")
            
            HastaListeleme()
            
        
        
        hastaAdi=tk.Label(guncellemeEkrani,text="Adınız:")
        hastaAdi.place(x=30,y=100)
        hastaAdi=tk.Entry(guncellemeEkrani)
        hastaAdi.place(x=150,y=100)
        hastaAdi.insert(0,bilgi[1])
        
        hastaSoyadi=tk.Label(guncellemeEkrani,text="Soyadınız:")
        hastaSoyadi.place(x=30,y=140)
        hastaSoyadi=tk.Entry(guncellemeEkrani)
        hastaSoyadi.place(x=150,y=140)
        hastaSoyadi.insert(0,bilgi[2])
        
        hastaYas=tk.Label(guncellemeEkrani,text="Yaşınız:")
        hastaYas.place(x=30,y=180)
        hastaYas=tk.Entry(guncellemeEkrani)
        hastaYas.place(x=150,y=180)
        hastaYas.insert(0,bilgi[3])
                
        hastaCinsiyet=tk.Label(guncellemeEkrani,text="Cinsiyetniz:")
        hastaCinsiyet.place(x=30,y=220)
        hastaCinsiyet=tk.Entry(guncellemeEkrani)
        hastaCinsiyet.place(x=150,y=220)
        hastaCinsiyet.insert(0,bilgi[4])
                
        guncellemeButon=tk.Button(guncellemeEkrani,text="GUNCELLE",command=guncellemeIslemi)
        guncellemeButon.place(x=30,y=260)
        
    def  sil():
        silinecek=listem.curselection()
        silinecekHastaSirasi=silinecek[0]
        silinecekHasta=hastaBilgileri[silinecekHastaSirasi]
        kimlikNo=silinecekHasta[0]
        print(kimlikNo)
        
        karar=messagebox.askyesno("Silme İşlemi Onayı","Bu hasta kaydını silmek istediğinize emin misiniz?")
        
        if karar:
            hastalarVeritabani=sqlite3.connect("hastalar.db")
            cur=hastalarVeritabani.cursor()
            cur.execute(''' 
                    
                    DELETE FROM hastalar WHERE kimlik=?
                
                ''', (kimlikNo,))

            hastalarVeritabani.commit()
            hastalarVeritabani.close()
            messagebox.showinfo("Silme Başarılı👍"," Hasta kaydı başarıyla silinmiştir")
            HastaListeleme()
        
           
        
    guncelleButton=tk.Button(listelemeEkrani,text="GÜNCELLE",width=10,command=guncelle)
    guncelleButton.place(x=300,y=60)
    
    silButton=tk.Button(listelemeEkrani,text="SİL",width=10,command=sil)
    silButton.place(x=300,y=100)
    



def doktorKayit():
    doktorKayitEkrani=tk.Toplevel()
    doktorKayitEkrani.title("doktor Kayıt")
    doktorKayitEkrani.geometry("500x600+300+200")
    
    def kaydet():
        ad=doktorAdi.get()
        soyad=doktorSoyadi.get()
        yas=doktoryas.get()
        cinsiyet=doktorcinsiyet.get()

        doktorlarVeritabani=sqlite3.connect("doktorlar.db")
        cur=doktorlarVeritabani.cursor()
        cur.execute(''' 

                INSERT INTO doktorlar(ad,soyad,yas,cinsiyet) VALUES(?,?,?,?)
            ''', (ad,soyad,yas,cinsiyet) )

        doktorlarVeritabani.commit()
        doktorlarVeritabani.close()
        messagebox.showinfo("kayıt Başarılı👌","doktor kaydı gerçekleştirildi")

        doktorKayitEkrani.after(3000,doktorKayitEkrani.destroy)

    baslikFrame=tk.Frame(doktorKayitEkrani,width=500,height=40,background="#8a2424")
    baslikFrame.place(x=0,y=0)
    hastaneName=tk.Label(baslikFrame,text="Digi Hospital",font=("Georgia",16,"bold"),fg="white",background="#8a2424")
    hastaneName.place(x=30,y=7)
    
    tk.Label(doktorKayitEkrani,text="HASTA KAYIT İŞLEMİ", font=("Arial",13),fg="#8a2424").place(x=30,y=60)
    
    footer=tk.Frame(doktorKayitEkrani,width=500,height=100,background="#8a2424")
    footer.place(x=0,y=400)


    doktorAdi=tk.Label(doktorKayitEkrani,text="Adınız:")
    doktorAdi.place(x=30,y=100)
    doktorAdi=tk.Entry(doktorKayitEkrani)
    doktorAdi.place(x=150,y=100)
    
    doktorSoyadi=tk.Label(doktorKayitEkrani,text="Soyadınız:")
    doktorSoyadi.place(x=30,y=140)
    doktorSoyadi=tk.Entry(doktorKayitEkrani)
    doktorSoyadi.place(x=150,y=140)
    
    doktoryas=tk.Label(doktorKayitEkrani,text="Yaşınız:")
    doktoryas.place(x=30,y=180)
    doktoryas=tk.Entry(doktorKayitEkrani)
    doktoryas.place(x=150,y=180)
    
    doktorcinsiyet=tk.Label(doktorKayitEkrani,text="Cinsiyetniz:")
    doktorcinsiyet.place(x=30,y=220)
    doktorcinsiyet=tk.Entry(doktorKayitEkrani)
    doktorcinsiyet.place(x=150,y=220)
    
    kaydetButon=tk.Button(doktorKayitEkrani,text="KAYDET",command=kaydet)
    kaydetButon.place(x=30,y=260)




def doktorListeleme():
    listelemeEkrani=tk.Toplevel()
    listelemeEkrani.geometry("400x600+200+200")
    listelemeEkrani.title("doktor Liste Ekrani")

    tk.Label(listelemeEkrani,text="DOKTORLARIMIZ",fg="red",font=("Georgia",14)).place(x=120,y=20)
    
    listem=tk.Listbox(listelemeEkrani,width=35,height=40)
    listem.place(x=30,y=60)

    doktorlarVeritabani=sqlite3.connect("doktorlar.db")
    cur=doktorlarVeritabani.cursor()
    cur.execute(''' 
            SELECT * FROM doktorlar

             ''')
    
    doktorBilgileri=cur.fetchall()
    doktorlarVeritabani.close()

    print(doktorBilgileri)

    for doktor in doktorBilgileri:
        düzenliBilgi=f"{doktor[0]}      {doktor[1]}            {doktor[2]}"
        listem.insert(tk.END,düzenliBilgi)

    
    def guncelle():
        guncellemeEkrani=tk.Toplevel()
        guncellemeEkrani.geometry("500x600+200+300")
        guncellemeEkrani.title("KAYIT GUNCELLEME EKRANI")
        
        secilen=listem.curselection()
        siraNumarasi=secilen[0]
        bilgi=doktorBilgileri[siraNumarasi]   
        
        
        def guncellemeIslemi():
            ad=doktorAdi.get()
            soyad=doktorSoyadi.get()
            yas=doktorYas.get()
            cinsiyet=doktorCinsiyet.get()
            
            doktorlarVeritabani=sqlite3.connect("doktorlar.db")
            cur=doktorlarVeritabani.cursor()
            cur.execute(''' 
                    
                UPDATE doktorlar SET ad=?,soyad=?,yas=?,cinsiyet=? WHERE kimlik=?
                ''', (ad,soyad,yas,cinsiyet,bilgi[0]) )

            doktorlarVeritabani.commit()
            doktorlarVeritabani.close()
            messagebox.showinfo("Güncelleme Başarılı👍"," doktor kaydı başarıyla güncellenmiştir")
            guncellemeEkrani.after(3000,guncellemeEkrani.destroy)
        
        
        doktorAdi=tk.Label(guncellemeEkrani,text="Adınız:")
        doktorAdi.place(x=30,y=100)
        doktorAdi=tk.Entry(guncellemeEkrani)
        doktorAdi.place(x=150,y=100)
        doktorAdi.insert(0,bilgi[1])
        
        doktorSoyadi=tk.Label(guncellemeEkrani,text="Soyadınız:")
        doktorSoyadi.place(x=30,y=140)
        doktorSoyadi=tk.Entry(guncellemeEkrani)
        doktorSoyadi.place(x=150,y=140)
        doktorSoyadi.insert(0,bilgi[2])
        
        doktorYas=tk.Label(guncellemeEkrani,text="Yaşınız:")
        doktorYas.place(x=30,y=180)
        doktorYas=tk.Entry(guncellemeEkrani)
        doktorYas.place(x=150,y=180)
        doktorYas.insert(0,bilgi[3])
                
        doktorCinsiyet=tk.Label(guncellemeEkrani,text="Cinsiyetniz:")
        doktorCinsiyet.place(x=30,y=220)
        doktorCinsiyet=tk.Entry(guncellemeEkrani)
        doktorCinsiyet.place(x=150,y=220)
        doktorCinsiyet.insert(0,bilgi[4])
                
        guncellemeButon=tk.Button(guncellemeEkrani,text="GUNCELLE",command=guncellemeIslemi)
        guncellemeButon.place(x=30,y=260)
        

    def sil():
        silinecek=listem.curselection()
        silinecekdoktorSirasi=silinecek[0]
        silinecekdoktor=doktorBilgileri[silinecekdoktorSirasi]
        kimlikNo=silinecekdoktor[0]
        print(kimlikNo)
        karar=messagebox.askyesno("!ONAY! Gerekiyor")

        if karar:
            doktorlarVeritabani=sqlite3.connect("doktorlar.db")
            cur=doktorlarVeritabani.cursor()
            cur.execute(''' 

                DELETE FROM doktorlar WHERE kimlik=?
            ''',(kimlikNo,))

            doktorlarVeritabani.commit()
            doktorlarVeritabani.close()
            messagebox.showinfo("silme Başarılı👍",)
            doktorListeleme()
    guncelleButton=tk.Button(listelemeEkrani,text="GÜNCELLE",width=10,command=guncelle)
    guncelleButton.place(x=300,y=60)
    
    silButton=tk.Button(listelemeEkrani,text="SİL",width=10,command=sil)
    silButton.place(x=300,y=100)

def canliDestek():
    destekEkrani=tk.Toplevel()
    destekEkrani.title("CANLI DESTEK")
    destekEkrani.geometry("300x600+1100+320")

    #def mesajGonder():
        
    #def mesajGoster():

    #def cevapVer():


    soru=tk.Entry(destekEkrani,width=20,font=("Georgia",12))
    soru.place(x=20, y=50)
    
    cevap= tk.Text(destekEkrani,width=20,height=20,font=("Georgia",12))
    cevap.place(x=20, y=100)

    cevapGoster=tk.Button(destekEkrani,text="Cevap GOSTER",width=20,font=("Georgia",12))
    cevapGoster.place(x=20,y=500)
    

def randevu():
    randevuEkrani=tk.Toplevel()
    randevuEkrani.geometry("800x600+200+200")
    listem=tk.Listbox(randevuEkrani,width=35,height=30)
    listem.place(x=30,y=50)
    
    tk.Label(randevuEkrani,text="hasta seçin",font=("Georgia",14),fg="#8a2424").place(x=30,y=15)

    hastalarVeritabani=sqlite3.connect("hastalar.db")
    cur=hastalarVeritabani.cursor()
    cur.execute(''' 
             SELECT * FROM hastalar
            
            ''' )

    hastaBilgileri=cur.fetchall()    
    hastalarVeritabani.close()
    
    for hasta in hastaBilgileri:
        duzenliBilgi=f"{hasta[0]}       {hasta[1]}         {hasta[2]}"
        listem.insert(tk.END,duzenliBilgi)
    tk.Label(randevuEkrani,text="doktor seçin",font=("Georgia",14),fg="#8a2424").place(x=260,y=15)
    doktorlistem=tk.Listbox(randevuEkrani,width=35,height=30)
    doktorlistem.place(x=300,y=50)

    doktorlarVeritabani=sqlite3.connect("doktorlar.db")
    cur=doktorlarVeritabani.cursor()
    cur.execute(''' 
            SELECT * FROM doktorlar

             ''')
    
    doktorBilgileri=cur.fetchall()
    doktorlarVeritabani.close()

    print(doktorBilgileri)

    for doktor in doktorBilgileri:
        düzenliBilgi=f"{doktor[0]}      {doktor[1]}            {doktor[2]}"
        doktorlistem.insert(tk.END,düzenliBilgi)

    tk.Label(randevuEkrani,text="tarih seçin",font=("Georgia",14),fg="#8a2424").place(x=500,y=15)
    takvim=Calendar(randevuEkrani,date_pattern="dd-mm-yyyy",selectmode="day")
    takvim.place(x=520,y=50)



    def hastaSec():
        global secilenHasta
        secilen=listem.curselection()
        siraNumarasi=secilen[0]
        secilenHasta=hastaBilgileri[siraNumarasi]
        print(secilenHasta)
    def doktorSec():
        global secilenDoktor
        secilen=doktorlistem.curselection()
        siraNumarasi=secilen[0]
        secilenDoktor=doktorBilgileri[siraNumarasi]
        print(secilenDoktor)
    def tarihSec():
        global secilenTarih
        secilenTarih=takvim.get_date()
        print(secilenTarih)

    def randevuGoster():
        msj=f"{secilenHasta[1]} {secilenHasta[2]} hastamızın {secilenDoktor[1]} {secilenDoktor[2]} ile {secilenTarih}de randevusu oluşturulmuştur"
        messagebox.showinfo("RANDEVU",msj)
        
    hastaSec=tk.Button(randevuEkrani,text="Hasta Seç",command=hastaSec)
    hastaSec.place(x=30,y=550)
    doktorSec=tk.Button(randevuEkrani,text="doktor Seç",command=doktorSec)
    doktorSec.place(x=260,y=550)
    tarihSec=tk.Button(randevuEkrani,text="tarih Seç",command=tarihSec)
    tarihSec.place(x=520,y=550)
    randevuOlustur=tk.Button(randevuEkrani,text="randevu oluştur",command=randevuGoster)
    randevuOlustur.place(x=600,y=550)

resim=tk.PhotoImage(file="assets\hastane.png")
resim=resim.subsample(2, 2)
photoLabel=tk.Label(root,image=resim, borderwidth=5,highlightthickness=5,relief="groove",highlightbackground="gray")
photoLabel.place(x=230, y=100)

canliDestek=tk.Button(root,text="Canli destek",font=("Georgia",13),bg="#154360",fg="white",command=canliDestek).place(x=850, y=750)

def iletisim():
    iletisim=tk.Toplevel()
    iletisim.geometry("500x400+200+200")
    iletisim.title("İLETİSİM")

    tk.Label(iletisim,text="Digi Hospital İletişim Bilgileri",font=("Georgia 13"),fg="#AD1414").place(x=100,y=30)
    tk.Label(iletisim,text="Tel:+49 165 258 16 16",font=("Georgia 13")).place(x=100,y=70)
    tk.Label(iletisim,text="Adres:Gesundheitsstraße 45",font=("Georgia 13")).place(x=100,y=110)
    tk.Label(iletisim,text="10555 Berlin Deutschland",font=("Georgia 13")).place(x=100,y=150)
#----------------------MENU-------------------------------
hastane_menu=Menu(root,tearoff=0)
#------------------HASTA IŞLEMELERI MENUSU--------------------
# Hasta İŞlemleri Menüsü
hasta_menu=Menu(hastane_menu,tearoff=0,background="#AD1414",foreground="white")
hasta_menu.add_command(label="Hasta Kayıt",font=("Arial 12"),command=HastaKayit)
hasta_menu.add_command(label="Hasta Listele",font=("Arial 12"),command=HastaListeleme)
hasta_menu.add_command(label="Randevu Listesi",font=("Arial 12"),command=randevu)



#----------------------doktor işlemleri------------------------------
doktor_menu=Menu(hastane_menu,tearoff=0,background="#AD1414",foreground="white")
doktor_menu.add_command(label="doktor kayıt",font=("Arial 12"),command=doktorKayit)
doktor_menu.add_command(label="doktor liste",font=("Arial 12"),command=doktorListeleme)
doktor_menu.add_command(label="randevu listesi",font=("Arial 12"))
#---------------Yardım Menusu----------------------
yardim_menu=Menu(hastane_menu,tearoff=0,background="#AD1414",foreground="white")
yardim_menu.add_command(label="Yardım Konuları")
#-----------------ILETİSİM MENUSU------------------------------
iletisim_menu=Menu(hastane_menu,tearoff=0,background="#AD1414",foreground="white")
iletisim_menu.add_command(label="İletisim bilgileri"command=iletisim)
#-------------------------------------------------
hastane_menu.add_cascade(label="Hasta İşlemleri",menu=hasta_menu)
hastane_menu.add_cascade(label="Doktor işlemeleri",menu=doktor_menu)
hastane_menu.add_cascade(label="yardım",menu=yardim_menu)
hastane_menu.add_cascade(label="iletişim",menu=iletisim_menu)
root.config(menu=hastane_menu)
#-------------------------------------------------





root.mainloop()