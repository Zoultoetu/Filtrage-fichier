import numpy as np
import datetime
import csv
import matplotlib.pyplot as plt

fh=open("C:/Users/melda/Downloads/ADE_RT1_Septembre2022_Decembre2022.ics","r")
res=fh.read()
ress=res.split('\n')
valeur=[]
liste_valeur_split=[]
#print(ress)
#writer.writerow(["identifiant","date","heure de début","heure de fin","modalite","intitule","localisation","prof","groupe"])
septembre=0
octobre=0
novembre=0
decembre=0
def lecture():
    for row in ress:
        comparaison_vcalendar(row)

def comparaison_vcalendar(row):
    if row.startswith("BEGIN:VCALENDAR"):
        a=0
    elif row.startswith("END:VCALENDAR"):
        return 0
    else:
        construction_du_cour(row)
    return septembre,octobre,novembre,decembre


def construction_du_cour(row):
    global intitule,date,heurecompletestop,heurecompletestart,heurestart,minutestart,secondestart,heurestop,minutestop,secondestop,identifiant,localisation,prof,groupe,modalite,septembre,octobre,novembre,decembre
    if row.startswith("BEGIN:VEVENT"):
        b=0
    if row.startswith("DTSTART"):
        textestart=row.split(":")
        anneestart=textestart[1][0:4]
        moistart=textestart[1][4:6]
        jourstart=textestart[1][6:8]
        heurestart=textestart[1][9:11]
        minutestart=textestart[1][11:13]
        secondestart=textestart[1][13:15]
        date=jourstart+"-"+moistart+"-"+anneestart
        heurecompletestart=heurestart+":"+minutestart+":"+secondestart
        if moistart=="09":
            septembre+=1
        elif moistart=="10":
            octobre+=1
        elif moistart=="11":
            novembre+=1
        elif moistart=="12":
            decembre+=1
        return septembre,octobre,novembre,decembre
        #print ("date de début =",date, "heure début =",heurecompletestart)
        #return date,heurecompletestart
    if row.startswith("UID"):
        texteIUD=row.split(":")
        identifiant=texteIUD[1]
        #print("identifiant :",identifiant)
        #return identifiant
    if row.startswith("SUMMARY"):
        textesummary=row.split(":")
        textesummary2=textesummary[1]
        textesummary3=textesummary2.split(" ")
        intitule=textesummary3[0]
        #print('intitule :',intitule)
        #return intitule
    if row.startswith("LOCATION"):
        textelocation=row.split(":")
        localisation=textelocation[1]
        #print("localisation :",localisation)
        #return localisation
    if row.startswith("DESCRIPTION"):
        textedescription=row.split("\\n\\n")
        textedescription1=textedescription[1]
        textedescription2=textedescription1.split('\\n')
        if textedescription2[1].startswith("("):
            prof="vide"
        else:
            prof=textedescription2[1]
        textedescription3=textedescription2[0]
        textedescription4=textedescription3.split(" ")
        if textedescription4[0]=="RT1-S1":
            modalite="CM"
            groupe="A1,A2,B1,B2"
        elif textedescription4[0]=="RT1-TD":
            modalite="TD"
            if textedescription4[1]=="A":
                groupe="A1,A2"
            elif textedescription4[1]=="B":
                groupe="B1,B2"
        elif textedescription4[0]=="RT1-TP":
            modalite="TP"
            if textedescription4[1]=="A1":
                groupe="A1"
            elif textedescription4[1]=="A2":
                groupe="A2"
            elif textedescription4[1]=="B1":
                groupe="B1"
            elif textedescription4[1]=="B2":
                groupe="B2"
        #print("prof :",prof,"Groupe :",groupe,"modalité :",modalite)
        #return prof, groupe
    if row.startswith("DTEND"):
        textestop=row.split(":")
        anneestop=textestop[1][0:4]
        moistop=textestop[1][4:6]
        jourstop=textestop[1][6:8]
        heurestop=textestop[1][9:11]
        minutestop=textestop[1][11:13]
        secondestop=textestop[1][13:15]
        date=jourstop+"-"+moistop+"-"+anneestop
        heurecompletestop=heurestop+":"+minutestop+":"+secondestop
        #print ("date de fin =",date, "heure fin =",heurecompletestop)
        #return heurecompletestop
    if row.startswith("END:VEVENT"):
        if groupe=="A1":
            heure_en_seconde=int(heurestart)*3600
            seconde_total_start=int(heurestart)*3600+int(minutestart)*60+int(secondestart)
            seconde_total_stop=int(heurestop)*3600+int(minutestop)*60+int(secondestop)
            duree_seconde=seconde_total_stop-seconde_total_start
            heure_duree=duree_seconde//3600
            duree_seconde-=heure_duree*3600
            duree_minute=duree_seconde//60
            duree_seconde-=duree_minute*60
            if duree_minute==0:
                str_duree_minute="00"
            else:
                str_duree_minute=str(duree_minute)
            if duree_seconde==0:
                str_duree_seconde="00"
            else:
                str_duree_seconde=str(duree_seconde)
            
            duree=str(heure_duree)+":"+str_duree_minute+":"+str_duree_seconde
    
            #duree=str(int(heurestop)-int(heurestart))+":"+"00"+":"+"00"
            evenement=date+";"+duree+";"+modalite+";"+groupe
            #evenementsplit=evenement.split(";")
            #print(evenementsplit)
            valeur.append(evenement)
            #print ("\n",evenementsplit)
        else:
            a=0
    
            
            
lecture()

#Tableau CSV

for j in range (len(valeur)):
    valeur_split=valeur[j].split(",")
    liste_valeur_split.append(valeur_split)


titre='date'+';'+'duree'+';'+'modalite'+";"+'groupe'
with open('data4.csv','w',newline='') as fichiercsv:
    writer=csv.writer(fichiercsv)
    writer.writerow([titre])
    #writer.writerow("\n")
    for i in range (len(liste_valeur_split)):
        writer.writerow(liste_valeur_split[i])
        print(liste_valeur_split[i])

#Graphe
labels='Septembre','Octobre','Novembre','Decembre'
sizes=[septembre,octobre,novembre,decembre]
colors=['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
plt.pie(sizes, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')
plt.savefig('PieChart01.png')
plt.show()

fh.close()
fichiercsv.close()