import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#
#Sa se citeasca din fisierul furnizori.csv. Datele din fisier vor fi transformate din string in date. Pentru valori lipsa se va afisa
#mesajul "Nu se cunoaste numarul de clienti"
fisier=pd.read_csv("furnizori.csv", delimiter=",")

fisier["Data_afisare_oferta"]=pd.to_datetime(fisier["Data_afisare_oferta"])
fisier["Nr_clienti_multumiti_de_oferta"]=fisier["Nr_clienti_multumiti_de_oferta"].replace(np.nan,"Nu se cunoaste numarul de clienti")
print(fisier)

#Sa se sterga din DataFrame-ul fisier ofertele a caror data nu mai este valabila
today=pd.to_datetime("today")
for row in fisier.index:
    if fisier["Data_afisare_oferta"][row]>today:
        fisier = fisier.drop(row,axis=0)
print(fisier)

# Avand in vedere ca multe oferte nu au numarul de clienti multumiti, se cere stergerea coloanei Nr_clienti_multumiti_de_oferta
fisier=fisier.drop(["Nr_clienti_multumiti_de_oferta"],axis=1)
print(fisier)


#Sucursalele firmei Damen din Romania au nevoie de otel. Insa sucursalele doresc ca furnizorii sa aiba puncte de lucru in Romania
#iar pretul sa nu fie mai mare de 4000 de euro. Sa se afiseze furnizorii care indeplinesc aceste criterii.

conditieTara=fisier['TaraOrigine']=='Romania'
conditiePret=fisier['Pret']<4000
conditieTip_prod=fisier["Tip_prod"]=="otel"
furnizoriOtelRomania=fisier.loc[conditieTara & conditiePret & conditieTip_prod]
print(furnizoriOtelRomania)

#Pentru alegerea celei mai bune optiuni, sucursalele firmei Damen din Romania vor sa cunoasca pretul otelului pe metrul patrat.
#Sa se introduca o noua coloana care sa arate acest lucru.

fisier['Pret_pe_unitate_de_masura']=fisier['Pret']/fisier['Cantitate']
fisierFurnizoriOtelRomania=fisier.loc[conditieTara & conditiePret & conditieTip_prod]
print(fisierFurnizoriOtelRomania)

# Pentru a alege furnizorul potrivit firma doreste sa afle pretul minim, pretul maxim si pretul mediu
# practicat de fiecare furnizor din fisierul fisierFurnizoriOtelRomania.

fisierAnalizaOferte=fisierFurnizoriOtelRomania.groupby(["NumeFurnizor"]).agg({
    "Pret_pe_unitate_de_masura": [min,max,"mean"]
})
print(fisierAnalizaOferte)

#Sa se compare grafic pretul minim, maxim si mediu practicat de fiecare furnizor de otel din Romania.
fisierAnalizaOferte.plot(kind="bar")
plt.show()




