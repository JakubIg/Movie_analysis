import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

filmy = pd.read_csv("C:/Users/Jan/Desktop/filmy.csv", sep=';')

filmy.info()

#ANALIZA OPISOWA, FEATURE ENGINEERING

#OCENA
filmy['Ocena'].describe()
#Dosc rownomierny rozklad ocen. Trzeba pamietac, ze same najlepsze
filmy['Ocena'].hist(bins=8)
plt.title("Histogram ocen filmów")
plt.xlabel('Ocena filmu')
plt.ylabel('Częstość')
#Widac, ze jest sporo bardzo dobrych filmow, z ocena powyzej sredniej
#Wybitnych jest jednak malo

#Outliery wsrod ocen
sns.boxplot(filmy['Ocena'])
filmy.loc[filmy['Ocena']<5.5]

#TYTUL
#Najlepsze filmy:
naj_filmy_ind = filmy['Ocena'].sort_values(ascending=False).head(10).index
filmy[['Tytul','Ocena']].iloc[naj_filmy_ind]

#AKTOR + OCENA_AKTORA
#Prawie sami mezczyzni w top 10 wystapien
len(filmy['Aktor'].unique())
filmy['Aktor'].value_counts().head(10)

#Filmy z jedyna kobieta w tej stawce
filmy['Tytul'][filmy['Aktor'] == 'Keira Knightley']

#Najlepsi aktorzy (nie ma kobiet)
filmy[['Aktor','Ocena_aktora']].drop_duplicates().nlargest(10,'Ocena_aktora')

#Dosc rownomierny rozklad ocen. Jak to sie ma do ocen filmow?
filmy['Ocena_aktora'].describe()

plt.hist(filmy['Ocena'], bins=10, alpha=0.5, label='Ocena filmu')
plt.hist(filmy['Ocena_aktora'], bins=10, alpha=0.5, label='Ocena aktora')
plt.legend(loc='upper left')
plt.title("Histogramy ocen filmów oraz ocen aktorów")
plt.ylabel('Częstość')
plt.show()

#Outliery wsrod ocen
sns.boxplot(filmy['Ocena_aktora'])
filmy.loc[filmy['Ocena_aktora']<7.1]
(filmy['Aktor'] == 'Charlotte Gainsbourg').sum()

#Czy ocena aktorskiej gry pokrywa sie z ocenami filmow?
sns.regplot(filmy['Ocena'], filmy['Ocena_aktora'])
np.corrcoef(filmy['Ocena'], filmy['Ocena_aktora'])

#Filmy dobre aktorsko, sam film slabszy (i na odwrot)
roznice_aktorskie = filmy['Ocena_aktora'] - filmy['Ocena']
roznice_aktorskie.hist(bins=7)
roznice_aktorskie_ind = roznice_aktorskie.sort_values(ascending=False).index
filmy[['Tytul','Ocena','Aktor','Ocena_aktora','Oscary']].iloc[roznice_aktorskie_ind].head(5)
filmy[['Tytul','Ocena','Aktor','Ocena_aktora','Oscary']].iloc[roznice_aktorskie_ind].tail(10)

#REZYSER + OCENA_REZYSERA
#Wieksza roznorodnosc niz u aktorow, ale istnieje tez wiecej dominatorow
len(filmy['Rezyser'].unique())
filmy['Rezyser'].value_counts().head(10)

#Najlepsi rezyserzy
filmy[['Rezyser','Ocena_rezysera']].drop_duplicates().nlargest(10,'Ocena_rezysera')

#Dosc rownomierny rozklad ocen. Jak to sie ma do ocen filmow?
filmy['Ocena_rezysera'].describe()

#Jeszcze inny zakres ocen?
plt.hist(filmy['Ocena'], bins=10, alpha=0.5, label='Ocena filmu')
plt.hist(filmy['Ocena_aktora'], bins=10, alpha=0.5, label='Ocena aktora')
plt.hist(filmy['Ocena_rezysera'], bins=10, alpha=0.5, label='Ocena rezysera')
plt.legend(loc='upper left')
plt.title("Histogramy ocen filmów, aktorów oraz reżyserów")
plt.ylabel('Częstość')
plt.show()

#Outliery wsrod ocen (brak)
sns.boxplot(filmy['Ocena_rezysera'])

#Czy ocena rezysera pokrywa sie z ocenami filmow/gry aktorskiej?
sns.regplot(filmy['Ocena'], filmy['Ocena_rezysera'])
np.corrcoef(filmy['Ocena'], filmy['Ocena_rezysera'])

sns.regplot(filmy['Ocena_aktora'], filmy['Ocena_rezysera'])
np.corrcoef(filmy['Ocena_aktora'], filmy['Ocena_rezysera'])

#Slabe filmy tworzone przez dobrych rezyserow (i na odwrot)
roznice_rezyserskie = filmy['Ocena_rezysera'] - filmy['Ocena']
roznice_rezyserskie.hist(bins=7)
roznice_rezyserskie_ind = roznice_rezyserskie.sort_values(ascending=False).index
filmy[['Tytul','Ocena','Rezyser','Ocena_rezysera','Oscary']].iloc[roznice_rezyserskie_ind].head(5)
filmy[['Tytul','Ocena','Rezyser','Ocena_rezysera','Oscary']].iloc[roznice_rezyserskie_ind].tail(10)

#Slabe filmy z dobra obsada rezyserska i aktorska
roznice_filmowe = (filmy['Ocena_rezysera'] + filmy['Ocena_aktora'])/2 - filmy['Ocena']
roznice_filmowe.hist()
roznice_filmowe_ind = roznice_filmowe.sort_values(ascending=False).index
filmy[['Tytul','Oscary']].iloc[roznice_filmowe_ind].head(10)
filmy[['Tytul','Oscary']].iloc[roznice_filmowe_ind].tail(10)

#Jakies czeste duety aktorsko-rezyserskie?
(filmy['Rezyser'] + ' + ' + filmy['Aktor']).value_counts().head(10)
duety = (filmy['Rezyser'] + ' + ' + filmy['Aktor']).value_counts()

sns.countplot(duety)
plt.title("Liczba wspólnych wystąpień aktorów i reżyserów")
plt.ylabel("")
plt.show()

duety = pd.DataFrame(duety.loc[duety>1])
duety['Duet'] = duety.index
czy_duet = []
for i in range(0,len(filmy.index)):
    if ((filmy['Rezyser'][i] + ' + ' + filmy['Aktor'][i]) in duety['Duet']):
        czy_duet.append(1)
    else:
        czy_duet.append(0)

czy_duet = np.array(czy_duet)
srednia_ocena_z_duetem = filmy.loc[czy_duet==1]['Ocena'].mean()
srednia_ocena_bez_duetu = filmy.loc[czy_duet==0]['Ocena'].mean()

#Ten sam aktor i rezyser?
(filmy['Aktor'] == filmy['Rezyser']).sum()
filmy[filmy['Aktor'] == filmy['Rezyser']]['Tytul']

#GATUNEK
filmy['Gatunek'].unique()
gatunek_filmu = filmy['Gatunek'].str.split(',', expand=True)[0]
gatunek_filmu.value_counts()
filmy_grozy_ind = gatunek_filmu[(gatunek_filmu=='Mystery') | (gatunek_filmu=='Horror') | 
        (gatunek_filmu=='Thriller')].index
animacja_ind = gatunek_filmu[gatunek_filmu=='Animation'].index

#Wszystkie maja wspolny "thriller", mozna wiec zmienic
filmy[['Tytul','Gatunek']].iloc[filmy_grozy_ind]
gatunek_filmu.iloc[filmy_grozy_ind] = 'Thriller'

#Zmiana animacji na komedie
filmy[['Tytul','Gatunek']].iloc[animacja_ind]
gatunek_filmu.iloc[animacja_ind] = 'Comedy'

#Oceny filmow wg gatunku
plt.figure(figsize=(8, 4))
sns.barplot(filmy[['Ocena']].groupby(gatunek_filmu).mean().index,
        filmy['Ocena'].groupby(gatunek_filmu).mean())
plt.title("Średnia ocena filmu wg gatunku")
plt.xlabel("")
plt.ylim(6, 8)

#A jak to sie ma do ogolu ocen?
dane = filmy[['Ocena', 'Ocena_aktora', 'Ocena_rezysera']].groupby(gatunek_filmu).mean()
dane['Gatunek'] = dane.index
dane = pd.melt(dane, id_vars=['Gatunek'])
dane['variable'] = dane['variable'].replace({'Ocena': 'Ocena_filmu'})
dane = dane.rename({'variable':'Ocena'}, axis='columns')
plt.figure(figsize=(10, 4))
sns.catplot(x="Gatunek", y="value", hue="Ocena", data=dane,
                height=6, kind="bar", palette="muted")
plt.title("Średnia ocena filmu, aktora i reżysera wg gatunku")
plt.xlabel("")
plt.ylabel("Ocena")
plt.ylim(6, 8.5)

#Aktorzy miedzygatunkowi?
filmy_gatunki = filmy
filmy_gatunki['Gatunek'] = gatunek_filmu
multi_aktorzy = np.array(filmy_gatunki['Aktor'].value_counts()[filmy_gatunki['Aktor'].value_counts()>1].index)
filmy_multi_aktorow = filmy_gatunki[filmy_gatunki['Aktor'].isin(multi_aktorzy)]
multi_aktorzy_gatunki = pd.crosstab(filmy_multi_aktorow['Aktor'], filmy_multi_aktorow['Gatunek'])
multi_aktorzy_gatunki.astype(bool).sum(axis=1).sort_values(ascending=False)
#Porownanie liczby filmow ogolem z liczba gatunkow
wszystkie_filmy = filmy_multi_aktorow['Aktor'].value_counts().sort_index()
liczba_gatunkow = multi_aktorzy_gatunki.astype(bool).sum(axis=1).sort_index()
aktorzy_vs_gatunki = pd.DataFrame({'Wszystkie_filmy':wszystkie_filmy, 
                                  'Liczba_gatunkow':liczba_gatunkow})
    
aktorzy_vs_gatunki[aktorzy_vs_gatunki['Wszystkie_filmy']>2].plot(
        y=['Wszystkie_filmy','Liczba_gatunkow'], kind="bar")
plt.title("Liczba wystąpień aktorów w różnych gatunkach filmów")
plt.xlabel("")
plt.ylabel("")

#Generalnie im czesciej tym wiecej gatunkow. Wyjatek: Christian Bale
#DiCaprio i Tom Hanks ciekawi
filmy[['Tytul','Ocena','Gatunek']][filmy['Aktor'] == 'Christian Bale']

#Rezyserzy miedzygatunkowi?
multi_rezyserzy = np.array(filmy_gatunki['Rezyser'].value_counts()[filmy_gatunki['Rezyser'].value_counts()>1].index)
filmy_multi_rezyserow = filmy_gatunki[filmy_gatunki['Rezyser'].isin(multi_rezyserzy)]
multi_rezyserzy_gatunki = pd.crosstab(filmy_multi_rezyserow['Rezyser'], filmy_multi_rezyserow['Gatunek'])
multi_rezyserzy_gatunki.astype(bool).sum(axis=1).sort_values(ascending=False)
#Porownanie liczby filmow ogolem z liczba gatunkow
wszystkie_filmy = filmy_multi_rezyserow['Rezyser'].value_counts().sort_index()
liczba_gatunkow = multi_rezyserzy_gatunki.astype(bool).sum(axis=1).sort_index()
rezyserzy_vs_gatunki = pd.DataFrame({'Wszystkie_filmy':wszystkie_filmy, 
                                  'Liczba_gatunkow':liczba_gatunkow})
    
rezyserzy_vs_gatunki[rezyserzy_vs_gatunki['Wszystkie_filmy']>3].plot(
        y=['Wszystkie_filmy','Liczba_gatunkow'], kind="bar")
plt.title("Liczba wyreżyserowanych różnych gatunków filmów")
plt.xlabel("")
plt.ylabel("")

#Generalnie tak samo jak u aktorow. Wyjatek: Guy Ritchie, Lars von Trier
filmy[['Tytul','Ocena','Gatunek']][filmy['Rezyser'] == 'Guy Ritchie']
filmy[['Tytul','Ocena','Gatunek']][filmy['Rezyser'] == 'Lars von Trier']

#DLUGOSC
filmy['Dlugosc'].describe()
#Dominuja filmy o dlugosci okolo 2 godzin, rzadko przekraczaja 3
filmy['Dlugosc'].hist(bins=10)
plt.title("Histogram długości filmów")
plt.xlabel('Długość filmu')
plt.ylabel('Częstość')

#Outliery wsrod filmow (okazuje sie, ze brak)
sns.boxplot(filmy['Dlugosc'])

#Czy dlugosc filmu pokrywa sie z ocenami filmow?
sns.regplot(filmy['Ocena'], filmy['Dlugosc'])
np.corrcoef(filmy['Ocena'], filmy['Dlugosc'])

#Czy lepiej oceniani aktorzy/rezyserzy graja w dluzszych filmach?
sns.regplot(filmy['Ocena_aktora'], filmy['Dlugosc'])
np.corrcoef(filmy['Ocena_aktora'], filmy['Dlugosc'])

#Dla rezyserow ma to wiekszy sens (lepsi rezyserzy sa w stanie krecic dluzsze filmy)
#Niekoniecznie jednak wieksza dlugosc przekuwa sie w lepsza ocene, j.w.
sns.regplot(filmy['Ocena_rezysera'], filmy['Dlugosc'])
np.corrcoef(filmy['Ocena_rezysera'], filmy['Dlugosc'])

#Czy sa rezyserzy, ktorzy upodobali sobie szczegolnie dlugie filmy?
#75%      143.750000
rezyserzy_dlugich_filmow = filmy[filmy['Dlugosc']>=143.75]['Rezyser'].value_counts().sort_index()
filmy_dlugich_rezyserow = filmy[filmy['Rezyser'].isin(rezyserzy_dlugich_filmow.index)]
filmy_dlugich_rezyserow_suma = filmy_dlugich_rezyserow['Rezyser'].value_counts().sort_index()
wszystkie_filmy_dlugich = pd.concat([rezyserzy_dlugich_filmow, filmy_dlugich_rezyserow_suma], axis=1)
wszystkie_filmy_dlugich.columns = ['Dlugie_filmy', 'Wszystkie_filmy']

#Widac, ze sa rezyserzy, ktorzy nakrecili wylacznie dlugie filmy:
#Gore Verbinski, Paul Thomas Anderson. Bezwzglednie - Christopher Nolan
#Ciekawy David Lynch - jeden film dlugi to caly dorobek
wszystkie_filmy_dlugich.plot(y=['Wszystkie_filmy','Dlugie_filmy'], kind="bar")
plt.title("Dorobek artystyczny reżyserów długich filmów")
plt.xlabel("")
plt.ylabel("")

filmy[['Tytul','Ocena','Dlugosc']][filmy['Rezyser'] == 'Gore Verbinski']
filmy[['Tytul','Ocena','Dlugosc']][filmy['Rezyser'] == 'Paul Thomas Anderson']
filmy[['Tytul','Ocena','Dlugosc']][filmy['Rezyser'] == 'David Lynch']

#Ktore gatunki przewazaja w najdluzszych filmach?
gatunki_dlugich_filmow = filmy_gatunki[filmy_gatunki['Dlugosc']>=143.75]['Gatunek'].value_counts().sort_index()
gatunki_suma = filmy_gatunki['Gatunek'].value_counts().sort_index()
gatunki_dlugich = pd.concat([gatunki_dlugich_filmow, gatunki_suma], axis=1)
gatunki_dlugich.columns = ['Dlugie_filmy', 'Wszystkie_filmy']

#Procentowo filmy przygodowe wygrywaja, komediowe przegrywaja
gatunki_dlugich.plot(y=['Wszystkie_filmy','Dlugie_filmy'], kind="bar")
plt.title("Gatunki długich filmów w stosunku do ogółu filmów")
plt.xlabel("")
plt.ylabel("")

#Ktore gatunki przewazaja w najkrotszych filmach?
#25%      114.500000
gatunki_krotkich_filmow = filmy_gatunki[filmy_gatunki['Dlugosc']<=114.5]['Gatunek'].value_counts().sort_index()
gatunki_krotkich = pd.concat([gatunki_krotkich_filmow, gatunki_suma], axis=1)
gatunki_krotkich.columns = ['Krotkie_filmy', 'Wszystkie_filmy']

#Procentowo filmy komediowe wygrywaja, ale nie jest na odwrot
#(filmy przygodowe sa w polowie stawki). Biograficznych jest najmniej, (bez)wzglednie
gatunki_krotkich.plot(y=['Wszystkie_filmy','Krotkie_filmy'], kind="bar")
plt.title("Gatunki krótkich filmów w stosunku do ogółu filmów")
plt.xlabel("")
plt.ylabel("")

#Sredni czas trwania poszczegolnych gatunkow
#Biografie wychodza srednio najdlusze, ale w rekordzistach najwiecej przygodowych
plt.figure(figsize=(8, 4))
sns.barplot(filmy[['Dlugosc']].groupby(gatunek_filmu).mean().index,
        filmy['Dlugosc'].groupby(gatunek_filmu).mean())
plt.title("Średnia długość filmu wg gatunku")
plt.xlabel("")
plt.ylim(80, 140)

#GLOSY
filmy['Glosy'].hist(bins=10)
plt.title("Histogram liczby głosów")
plt.xlabel('Liczba głosów')
plt.ylabel('Częstość')

#Widac, ze logarytm lepiej pasuje
sns.regplot(filmy['Ocena'], filmy['Glosy'])
np.corrcoef(filmy['Ocena'], filmy['Glosy'])

sns.regplot(filmy['Ocena'], np.log(filmy['Glosy']))
np.corrcoef(filmy['Ocena'], np.log(filmy['Glosy']))

#Outliery wsrod glosow
sns.boxplot(filmy['Glosy'])
filmy.loc[filmy['Glosy']>1000000][['Tytul','Ocena','Glosy']]

#Co jak z logarytmem? (brak outlierow)
sns.boxplot(np.log(filmy['Glosy']))

#Najpopularniejsze juz byly, teraz te mniej popularne:
filmy[['Tytul','Ocena','Glosy']].sort_values('Glosy').head(5)

#Popularnosc a ocena aktora (malo glosow, najwyzsza ocena - nie uwzgledniono Jokera)
#Raczej brak zaleznosci, ale filmy powyzej 750 tys. maja prawie zawsze wysokie noty
sns.regplot(filmy['Ocena_aktora'], filmy['Glosy'])
np.corrcoef(filmy['Ocena_aktora'], filmy['Glosy'])

sns.regplot(filmy['Ocena_rezysera'], filmy['Glosy'])
np.corrcoef(filmy['Ocena_rezysera'], filmy['Glosy'])

#Badanie popularnosci wg aktorow/rezyserow nie ma duzego sensu, bo niektorzy aktorzy
#z jednego hitu beda mieli wyzsza srednia niz dobrzy aktorzy z wielu produkcji
#Ponadto, popularnosc tyczy sie stricte filmu
aktorzy_popularnosc = filmy['Glosy'].groupby(filmy['Aktor']).mean().sort_values(ascending=False)
aktorzy_popularnosc.head(10)

rezyserzy_popularnosc = filmy['Glosy'].groupby(filmy['Rezyser']).mean().sort_values(ascending=False)
rezyserzy_popularnosc.head(10)

#Ktore gatunki maja najwieksza popularnosc?
filmy.loc[filmy['Glosy']>1000000][['Tytul','Ocena','Glosy','Gatunek']]

#Ciekawi niski wynik komedii, wysoki wynik akcji mimo mnostwa filmow
plt.figure(figsize=(8, 4))
sns.barplot(filmy[['Glosy']].groupby(gatunek_filmu).mean().index,
        filmy['Glosy'].groupby(gatunek_filmu).mean())
plt.title("Średnia liczba głosów na film wg gatunku")
plt.xlabel("")
#Oceny filmow wg gatunku
plt.figure(figsize=(8, 4))
sns.barplot(filmy[['Ocena']].groupby(gatunek_filmu).mean().index,
        filmy['Ocena'].groupby(gatunek_filmu).mean())
plt.title("Średnia ocena filmu wg gatunku")
plt.xlabel("")
plt.ylim(6, 8)

#No i wszystko jasne: to przez najwieksze hity
filmy_bez_najpopularniejszych = filmy.loc[filmy['Glosy']<1000000]
plt.figure(figsize=(8, 4))
sns.barplot(filmy_bez_najpopularniejszych[['Glosy']].groupby(gatunek_filmu).mean().index,
        filmy_bez_najpopularniejszych['Glosy'].groupby(gatunek_filmu).mean())
plt.title("Średnia liczba głosów na film wg gatunku (bez najpopularniejszych)")
plt.xlabel("")

#Czy ludzie nie sa znudzeni dlugimi filmami?
#(oceny dla dlugich filmow byly nieco lepsze niz srednia ogolna)
sns.regplot(filmy['Dlugosc'], filmy['Glosy'])
np.corrcoef(filmy['Dlugosc'], filmy['Glosy'])

#BOX.OFFICE
filmy['Box.office'].hist(bins=10)
plt.title("Histogram box office'u")
plt.xlabel('Box office')
plt.ylabel('Częstość')

#Widac, ze logarytm zbytnio nie pomaga
sns.regplot(filmy['Ocena'], filmy['Box.office'])
np.corrcoef(filmy['Ocena'], filmy['Box.office'])

sns.regplot(filmy['Ocena'], np.log(filmy['Box.office']))
np.corrcoef(filmy['Ocena'], np.log(filmy['Box.office']))

#Outliery wsrod box office
sns.boxplot(filmy['Box.office'])
filmy.loc[filmy['Box.office']>340][['Tytul','Ocena','Box.office']]

#Co jak z logarytmem?
sns.boxplot(np.log(filmy['Box.office']))

#Najbardziej kasowe juz byly, teraz te mniej:
filmy[['Tytul','Ocena','Box.office']].sort_values('Box.office').head(5)
#Tytuly znajome (to od rezysera, co specjalizuje sie w jednym gatunku)
filmy[['Tytul','Rezyser','Box.office']].sort_values('Box.office').head(5)

#Brak szczegolnej zaleznosci
sns.regplot(filmy['Ocena_aktora'], filmy['Box.office'])
np.corrcoef(filmy['Ocena_aktora'], filmy['Box.office'])

#Ktorzy aktorzy graja w najbardziej kasowych filmach?
#Z tej stawki tylko Chris Evans gral w >1 filmie (Kapitan Ameryka 2 czesci)
zarobki_aktorow = filmy['Box.office'].groupby(filmy['Aktor']).mean().sort_values(ascending=False)
plt.figure(figsize=(8, 4))
sns.barplot(zarobki_aktorow.head(5).index, zarobki_aktorow.head(5))
plt.title("Aktorzy grający najczęściej w najbardziej kasowych filmach")
plt.xlabel("")
#Tu ponownie Nimfomanka (Charlotte Gainsbourg - tylko ona w >1 filmie)
plt.figure(figsize=(8, 4))
sns.barplot(zarobki_aktorow.tail(5).index, zarobki_aktorow.tail(5))
plt.title("Aktorzy grający najczęściej w najmniej kasowych filmach")
plt.xlabel("")

#Rowniez brak szczegolnej zaleznosci
sns.regplot(filmy['Ocena_rezysera'], filmy['Box.office'])
np.corrcoef(filmy['Ocena_rezysera'], filmy['Box.office'])

#Jak wyzej, ale odnosnie rezyserow (nie ma tu jednostrzalowcow, nie jak u aktorow)
zarobki_rezyserow = filmy['Box.office'].groupby(filmy['Rezyser']).mean().sort_values(ascending=False)
plt.figure(figsize=(8, 4))
sns.barplot(zarobki_rezyserow.head(5).index, zarobki_rezyserow.head(5))
plt.title("Reżyserzy reżyserujący najczęściej najbardziej kasowe filmy")
plt.xlabel("")
#Tu rowniez rezyser od Nimfomanki
zarobki_rezyserow = filmy['Box.office'].groupby(filmy['Rezyser']).mean().sort_values(ascending=False)
plt.figure(figsize=(8, 4))
sns.barplot(zarobki_rezyserow.tail(5).index, zarobki_rezyserow.tail(5))
plt.title("Reżyserzy reżyserujący najczęściej najmniej kasowe filmy")
plt.xlabel("")

#Czy box office moze brac sie z popularnosci?
sns.regplot(filmy['Glosy'], filmy['Box.office'])
np.corrcoef(filmy['Glosy'], filmy['Box.office'])

#Czy wklad czasowy przeklada sie na box office?
sns.regplot(filmy['Dlugosc'], filmy['Box.office'])
np.corrcoef(filmy['Dlugosc'], filmy['Box.office'])

#Podsumowanie gatunkowe (dac wszystkie slajdy odnosnie gatunku)
plt.figure(figsize=(8, 4))
sns.barplot(filmy[['Box.office']].groupby(gatunek_filmu).mean().index,
        filmy['Box.office'].groupby(gatunek_filmu).mean())
plt.title("Średni box office filmu wg gatunku")
plt.xlabel("")

ind = filmy.groupby(gatunek_filmu)['Box.office'].transform(max) == filmy['Box.office']
filmy[ind][['Gatunek','Tytul','Box.office']].sort_values('Gatunek')

#OSCARY
filmy['Oscary'].hist(bins=6)
plt.title("Histogram liczby Oscarów")
plt.xlabel('Liczba Oscarów')
plt.ylabel('Częstość')

#Outliery
sns.boxplot(filmy['Oscary'])
#Wplyw dodatkwoego Oscara raczej nie jest tak duzy, mozna zrobic zmienna 0-1-2+
#(wartosci wyzsze wystepuja tez rzadko)
oscary = filmy['Oscary'].replace([3,4,5,6], 2)

#Czyli obecnosc Oscara o czyms swiadczy
dane = filmy[['Ocena', 'Ocena_aktora', 'Ocena_rezysera']].groupby(oscary).mean()
dane['Oscary'] = dane.index
dane = pd.melt(dane, id_vars='Oscary')
dane['variable'] = dane['variable'].replace({'Ocena': 'Ocena_filmu'})
dane = dane.rename({'variable':'Ocena'}, axis='columns')
plt.figure(figsize=(8, 4))
sns.catplot(x="Ocena", y="value", hue="Oscary", data=dane,
                height=6, kind="bar", palette="muted")
plt.title("Średnia ocena filmu, aktora i reżysera wg Oscarów")
plt.xlabel("")
plt.ylabel("Ocena")
plt.ylim(6, 8.5)

#Dlugosc o jakies 10 minut, ale roznica tylko miedzy 0 i 1
sns.barplot(filmy['Dlugosc'].groupby(oscary).mean().index,
            filmy['Dlugosc'].groupby(oscary).mean())
plt.title("Średnia długość filmu wg Oscarów")
plt.xlabel("")

#Gatunki vs Oscary
filmy_gatunki['Oscary'] = oscary
plt.figure(figsize=(8, 4))
sns.countplot('Gatunek',hue='Oscary',data=filmy_gatunki)
plt.legend(['0','1','>=2'], title="Oscary", loc='upper right')
plt.title("Podział gatunków filmów ze względu na Oscary")
plt.xlabel("")
plt.ylabel("Liczba")
plt.show()

#Film z najnizsza/najwyzsza ocena, jaki dostal Oscara
filmy[filmy['Oscary']>1][['Tytul','Ocena','Oscary']].sort_values('Ocena').head(1)
filmy[filmy['Oscary']>1][['Tytul','Ocena','Oscary']].sort_values('Ocena').tail(1)

#Zmienna: liczba gatunkow przypisana do filmu?
liczba_gatunkow = []
for i in range(0, len(filmy['Gatunek'])):
    liczba_gatunkow.append(filmy['Gatunek'][i].count(",")+1)
liczba_gatunkow = pd.Series(liczba_gatunkow)

liczba_gatunkow.value_counts()

plt.figure(figsize=(8, 4))
sns.barplot(filmy[['Ocena']].groupby(liczba_gatunkow).mean().index,
        filmy['Ocena'].groupby(liczba_gatunkow).mean())
plt.ylim(6,8)

#USUNIECIE OUTLIEROW
#Ze wzgledu na ocene:
filmy = filmy.loc[filmy['Ocena']>=5.5]
#Ze wzgledu na ocene aktora:
filmy = filmy.loc[filmy['Aktor']!='Charlotte Gainsbourg']
#Dla Glosy: uzyty bedzie logarytm, po nim nie ma outlierow
#Ze wzgledu na Box.office (logarytm, bo ogon jest spory):
filmy = filmy.loc[np.log(filmy['Box.office'])>0.5]

filmy = filmy.reset_index(drop=True)

#PRZYGOTOWANIE DANYCH
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import FeatureUnion
from sklearn.preprocessing import StandardScaler

class Duety_filmowe(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self._attribute_names = attribute_names
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        duety = (X['Rezyser'] + ' + ' + X['Aktor']).value_counts()
        duety = duety.loc[duety>1]
        czy_duet = list()
        aktorzy = list(X[self._attribute_names])
        for i in range(0, len(aktorzy)):
            if ((X['Rezyser'][i] + ' + ' + aktorzy[i]) in duety.index):
                czy_duet.append(1)
            else:
                czy_duet.append(0)
        X.loc[:, 'Duet'] = czy_duet
        return X.values

class Liczebnosc_gatunkow(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self._attribute_names = attribute_names
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        liczba_gatunkow = list()
        gatunki = list(X[self._attribute_names])
        for i in range(0, len(gatunki)):
            liczba_gatunkow.append(gatunki[i].count(",")+1)
        X.loc[:, 'Liczba_gatunkow'] = liczba_gatunkow
        return X.values

class Ustalenie_gatunku(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self._attribute_names = attribute_names
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        gatunek_filmu = X[self._attribute_names].str.split(',', expand=True)[0]
        filmy_grozy_ind = gatunek_filmu[(gatunek_filmu=='Mystery') | 
        (gatunek_filmu=='Horror') | (gatunek_filmu=='Thriller')].index
        animacja_ind = gatunek_filmu[gatunek_filmu=='Animation'].index
        gatunek_filmu.iloc[filmy_grozy_ind] = 'Thriller'
        gatunek_filmu.iloc[animacja_ind] = 'Comedy'
        X.loc[:,'Gatunek'] = gatunek_filmu
        return X.values

class Logarytm(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self._attribute_names = attribute_names
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        X[self._attribute_names] = np.log(X[self._attribute_names])
        return X.values

class Oscary_kodowanie(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self._attribute_names = attribute_names
    def fit(self, X, y=None):
        return self
    def kodowanie(self, obj):
        if (obj == 0):
            Oscary_k = 'zero'
        elif (obj == 1):
            Oscary_k = 'jeden'
        else:
            Oscary_k = 'wiecej'
        return Oscary_k
    def transform(self, X):
        X.loc[:, 'Oscary_k'] = X[self._attribute_names].apply(self.kodowanie)
        return X.values

aktor = 'Aktor'
aktor_pipeline = Pipeline(steps=[
    ('Duety_filmowe', Duety_filmowe(aktor))
])

gatunek = 'Gatunek'
gatunek_pipeline = Pipeline(steps=[
    ('Liczebnosc_gatunkow', Liczebnosc_gatunkow(gatunek))
])

gatunek_pipeline2 = Pipeline(steps=[
    ('Ustalenie_gatunku', Ustalenie_gatunku(gatunek))
])

box_office = 'Box.office'
box_office_pipeline = Pipeline(steps=[
    ('Logarytm', Logarytm(box_office))
])

glosy = 'Glosy'
glosy_pipeline = Pipeline(steps=[
    ('Logarytm', Logarytm(glosy))
])

oscary = 'Oscary'   
oscary_pipeline = Pipeline(steps=[
    ('Oscary_kodowanie', Oscary_kodowanie(oscary))
])

#Kategoryczne zmienne
atrybuty1 = ['Gatunek','Liczba_gatunkow']
atrybuty1_pipeline = Pipeline(steps=[
    ('encoder', OneHotEncoder(sparse=False)),
    ('standarizer', StandardScaler())
])

#Numeryczne zmienne
atrybuty2 = ['Duet','Dlugosc','Glosy','Box.office','Ocena_aktora','Ocena_rezysera', 'Oscary'
             ]
atrybuty2_pipeline = Pipeline(steps=[
    ('standarizer', StandardScaler())
])

#Polaczenie przeplywow dla kategorycznych i numerycznych
preprocessor = ColumnTransformer(
    remainder = 'drop',
    transformers=[
        ('first', atrybuty1_pipeline, atrybuty1),
        ('second', atrybuty2_pipeline, atrybuty2)
])

#Laczenie wszystkich przeplywow
full_pipeline = FeatureUnion([
    ('aktor_pipeline', aktor_pipeline),
    ('gatunek_pipeline', gatunek_pipeline),
    ('gatunek_pipeline2', gatunek_pipeline2),
    ('box_office_pipeline', box_office_pipeline),
    ('glosy_pipeline', glosy_pipeline),
    #('oscary_pipeline', oscary_pipeline),
    ('preprocessor', preprocessor)
])

#Przeplyw usuwajacy niepotrzebne kolumny
full_pipeline2 = FeatureUnion([
    ('preprocessor', preprocessor)
])

#TRANSFORMACJA DANYCH
filmy_przygotowane = full_pipeline.fit_transform(filmy)
filmy_przygotowane = full_pipeline2.fit_transform(filmy)
X_filmy_przygotowane = filmy_przygotowane
y_filmy_przygotowane = filmy['Ocena']

#UCZENIE MODELU
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.linear_model import ElasticNet
from sklearn.neighbors  import KNeighborsRegressor
##############
#Random Forest
##############
rf_model = RandomForestRegressor(random_state=42)

params_grid = [
        {'n_estimators': [100, 200, 300, 400, 500],
         'criterion': ['mse', 'mae'],
         'min_samples_split': [2, 3, 4, 5],
         'max_features': ['auto', 'log2', 'sqrt'],
         'bootstrap': ['True', 'False']}
]

grid_search = GridSearchCV(rf_model, params_grid, cv=5, scoring="neg_mean_squared_error", n_jobs=1)
grid_search.fit(X_filmy_przygotowane, y_filmy_przygotowane)
grid_search.best_params_

#{'bootstrap': 'True',
# 'criterion': 'mae',
# 'max_features': 'auto',
# 'min_samples_split': 3,
# 'n_estimators': 400}

params_grid2 = [
        {'n_estimators': [120, 140, 160, 180, 200, 220, 240, 260, 280],
         'criterion': ['mse', 'mae'],
         'min_samples_split': [2, 3],
         'max_features': ['auto'],
         'bootstrap': ['True']}
]

grid_search2 = GridSearchCV(rf_model, params_grid2, cv=5, scoring="neg_mean_squared_error", n_jobs=1)
grid_search2.fit(X_filmy_przygotowane, y_filmy_przygotowane)
grid_search2.best_params_

#{'bootstrap': 'True',
# 'criterion': 'mae',
# 'max_features': 'auto',
# 'min_samples_split': 3,
# 'n_estimators': 420}

def indices_of_top_k(arr, k):
    return np.sort(np.argpartition(np.array(arr), -k)[-k:])

def fs_calculate_results():
    cv_mean = list()
    cv_std = list()
    rf_model = RandomForestRegressor()
    feature_importances = grid_search2.best_estimator_.feature_importances_
    for i in range(1,18):
       indices_of_top = indices_of_top_k(feature_importances, i)
       X_filmy_restricted = X_filmy_przygotowane[:, indices_of_top]
       params_grid_fs = [
        {'n_estimators': [120, 140, 160],
         'criterion': ['mse', 'mae'],
         'min_samples_split': [2, 3],
         'max_features': ['auto'],
         'bootstrap': ['True']}
        ]
       print(i)
       grid_search_fs = GridSearchCV(rf_model, params_grid_fs, cv=5, scoring="neg_mean_squared_error", n_jobs=1)
       grid_search_fs.fit(X_filmy_restricted, y_filmy_przygotowane)
       rf_best_model = grid_search_fs.best_estimator_
       rf_cv = cross_val_score(rf_best_model, X_filmy_restricted, y_filmy_przygotowane,
                             scoring="neg_mean_squared_error", cv=10)
       rf_cv = np.sqrt(-rf_cv)
       cv_mean.append(rf_cv.mean())
       cv_std.append(rf_cv.std())
    return cv_mean, cv_std

cv_mean, cv_std = fs_calculate_results()
fs_results = pd.DataFrame({'cv_mean': cv_mean, 'cv_std': cv_std})
fs_results.index += 1
fs_results = fs_results.sort_values('cv_mean')
fs_results

rf_model = grid_search2.best_estimator_
rf_prognoza = rf_model.predict(X_filmy_przygotowane)
rf_mse = mean_squared_error(y_filmy_przygotowane, rf_prognoza)
rf_rmse = np.sqrt(rf_mse)
print("RMSE modelu RF: ", rf_rmse)

def wyniki_sprawdzianu_krzyzowego(wyniki):
    print("Wyniki:", wyniki)
    print("Średnia:", wyniki.mean())
    print("Odchylenie standardowe:", wyniki.std())

rf_cv = cross_val_score(rf_model, X_filmy_przygotowane, y_filmy_przygotowane,
                             scoring="neg_mean_squared_error", cv=10)
rf_cv = np.sqrt(-rf_cv)

wyniki_sprawdzianu_krzyzowego(rf_cv)

#Średnia: 0.45200352604248073
#Odchylenie standardowe: 0.10952795478524784
#################
#Regresja liniowa
#################


lin_reg = LinearRegression()
params_grid = [
        {'fit_intercept': [True, False]}
]
grid_search = GridSearchCV(lin_reg, params_grid, cv=5, scoring="neg_mean_squared_error", n_jobs=1)
grid_search.fit(X_filmy_przygotowane, y_filmy_przygotowane)
grid_search.best_params_

lin_reg_model = grid_search.best_estimator_
lin_reg_prognoza = lin_reg_model.predict(X_filmy_przygotowane)
lin_reg_mse = mean_squared_error(y_filmy_przygotowane, lin_reg_prognoza)
lin_reg_rmse = np.sqrt(lin_reg_mse)
print("RMSE modelu liniowego: ", lin_reg_rmse)

lin_reg_cv = cross_val_score(lin_reg_model, X_filmy_przygotowane, y_filmy_przygotowane,
                             scoring="neg_mean_squared_error", cv=10)
lin_reg_cv = np.sqrt(-lin_reg_cv)

wyniki_sprawdzianu_krzyzowego(lin_reg_cv)
#Średnia: 0.45857143851177173
#Odchylenie standardowe: 0.12547854785389137
###############
#####SVM#######
###############
svm_model = SVR()

params_grid = [
        {'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
         'gamma': ['scale', 'auto'],
         'shrinking': [True, False],
         'C': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]}
]

grid_search = GridSearchCV(svm_model, params_grid, cv=5, scoring="neg_mean_squared_error", n_jobs=1)
grid_search.fit(X_filmy_przygotowane, y_filmy_przygotowane)
grid_search.best_params_
#{'C': 0.3, 'gamma': 'scale', 'kernel': 'linear', 'shrinking': False}
svm_model = grid_search.best_estimator_
svm_prognoza = lin_reg_model.predict(X_filmy_przygotowane)
svm_mse = mean_squared_error(y_filmy_przygotowane, svm_prognoza)
svm_rmse = np.sqrt(svm_mse)
print("RMSE modelu SVM: ", lin_reg_rmse)

svm_cv = cross_val_score(svm_model, X_filmy_przygotowane, y_filmy_przygotowane,
                             scoring="neg_mean_squared_error", cv=10)
svm_cv = np.sqrt(-svm_cv)

wyniki_sprawdzianu_krzyzowego(svm_cv)

############
#Elastic Net
############
en_model = ElasticNet(random_state=42)

params_grid = [
        {'alpha': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
         'l1_ratio': [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
         'fit_intercept': [True, False],
         'tol':[1],
         'max_iter': [500, 1000, 5000, 10000]}
]

grid_search = GridSearchCV(en_model, params_grid, cv=5, scoring="neg_mean_squared_error", n_jobs=1)
grid_search.fit(X_filmy_przygotowane, y_filmy_przygotowane)
grid_search.best_params_
#{'alpha': 0.1,
# 'fit_intercept': True,
# 'l1_ratio': 0.4,
# 'max_iter': 500,
# 'tol': 1}
en_model = grid_search.best_estimator_
en_prognoza = en_model.predict(X_filmy_przygotowane)
en_mse = mean_squared_error(y_filmy_przygotowane, en_prognoza)
en_rmse = np.sqrt(en_mse)
print("RMSE modelu Elastic Net: ", en_rmse)

en_cv = cross_val_score(en_model, X_filmy_przygotowane, y_filmy_przygotowane,
                             scoring="neg_mean_squared_error", cv=10)
en_cv = np.sqrt(-en_cv)

wyniki_sprawdzianu_krzyzowego(en_cv)

###############
#####KNN#######
###############
knn_model = KNeighborsRegressor()
params_grid = [
        {'n_neighbors': [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
         'weights': ['uniform', 'distance'],
         'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
         'metric': ['minkowski', 'euclidean', 'manhattan']}
]

grid_search = GridSearchCV(knn_model, params_grid, cv=5, scoring="neg_mean_squared_error", n_jobs=1)
grid_search.fit(X_filmy_przygotowane, y_filmy_przygotowane)
grid_search.best_params_
#{'algorithm': 'auto',
# 'metric': 'manhattan',
# 'n_neighbors': 16,
# 'weights': 'distance'}
knn_model = grid_search.best_estimator_
knn_prognoza = knn_model.predict(X_filmy_przygotowane)
knn_mse = mean_squared_error(y_filmy_przygotowane, knn_prognoza)
knn_rmse = np.sqrt(knn_mse)
print("RMSE modelu KNN: ", knn_rmse)

knn_cv = cross_val_score(knn_model, X_filmy_przygotowane, y_filmy_przygotowane,
                             scoring="neg_mean_squared_error", cv=10)
knn_cv = np.sqrt(-knn_cv)

wyniki_sprawdzianu_krzyzowego(knn_cv)