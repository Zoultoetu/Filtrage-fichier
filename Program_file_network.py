import numpy as np
import datetime
import csv
import matplotlib.pyplot as plt
fileopen=str(input("Enter the road of file for example : C:/Users/melda/Downloads/DumpFile.txt "))
namecsv=str(input("Enter the name of the exel file"))
namecsv+=".csv"
namediagram=str(input("Enter the name of the diagram file"))
namediagram+=".png"
fh=open(fileopen,"r")
res=fh.read()
ress=res.split('\n')
valeur=[]
liste_valeur_split=[]
point=0
point_S=0
point_P=0
S=0
def lecture():
    for row in ress:
        comparaison_debut(row)

def comparaison_debut(row):
    if row.startswith("	"):
        a=0
    else:
        print(row)
        construction_liste(row)


def construction_liste(row):
    global txt_split7,evenement,heure,IP_source,IP_destination,txt_flag,txt_seq,txt_ack,txt_win,txt_contenu_option,txt_legth,point,point_P,point_S,S
    a=0
    if "IP" in row:
        if "Flags" in row:
            txt_split=row.split(">")
            txt_split2=txt_split[0]
            txt_split4=txt_split[1]
            txt_split3=txt_split2.split("IP")
            IP_source=txt_split3[1]
            heure=txt_split3[0]
            txt_split5=txt_split4.split(": ")
            IP_destination=txt_split5[0]
            txt_split6=txt_split5[1]
            txt_split7=txt_split6.split(", ")
            if "seq" in row:
                a=1
                if "ack " in row:
                    txt_flag=txt_split7[0]
                    txt_seq=txt_split7[1]
                    txt_ack=txt_split7[2]
                    txt_win=txt_split7[3]
                    if "options" in row:
                        txt_option_split=txt_split7[4].split(" [")
                        txt_contenu_option=txt_option_split[1]
                        txt_legth=txt_split7[5]
                        evenement=heure+";"+IP_source+";"+IP_destination+";"+txt_flag+";"+txt_seq+";"+txt_ack+";"+txt_win+";"+txt_contenu_option+";"+txt_legth
                    elif "length" in row :
                            txt_legth=txt_split7[4]
                            evenement=heure+";"+IP_source+";"+IP_destination+";"+txt_flag+";"+txt_seq+";"+txt_ack+";"+txt_win+";"+" "+";"+txt_legth
                    else:
                            evenement=heure+";"+IP_source+";"+IP_destination+";"+txt_flag+";"+txt_seq+";"+txt_ack+";"+txt_win
                else:
                    txt_flag=txt_split7[0]
                    txt_seq=txt_split7[1]
                    txt_win=txt_split7[2]
                    if "options" in txt_split7[3]:
                        txt_option_split=txt_split7[3].split(" [")
                        txt_contenu_option="["+txt_option_split[1]
                        evenement=heure+";"+IP_source+";"+IP_destination+";"+txt_flag+";"+txt_seq+";"+" "+";"+txt_win+";"+txt_contenu_option+";"+txt_legth
                    else:
                        txt_legth=txt_split7[3]
                        evenement=heure+";"+IP_source+";"+IP_destination+";"+txt_flag+";"+txt_seq+";"+" "+";"+txt_win+";"+" "+";"+txt_legth

            elif "ack " in row:
                a=1
                txt_flag=txt_split7[0]
                txt_ack=txt_split7[1]
                txt_win=txt_split7[2]
                if "options" in txt_split7[3]:
                    txt_option_split=txt_split7[3].split(" [")
                    txt_contenu_option="["+txt_option_split[1]
                    if "length" in row :
                        txt_legth=txt_split7[4]
                        evenement=heure+";"+IP_source+";"+IP_destination+";"+txt_flag+";"+" "+";"+txt_ack+";"+txt_win+";"+txt_contenu_option+";"+txt_legth
                    else:
                        evenement=heure+";"+IP_source+";"+IP_destination+";"+txt_flag+";"+" "+";"+txt_ack+";"+txt_win+";"+txt_contenu_option
                elif "length" in row :
                    txt_legth=txt_split7[3]
                    evenement=heure+";"+IP_source+";"+IP_destination+";"+txt_flag+";"+" "+";"+txt_ack+";"+txt_win+";"+" "+";"+txt_legth
                else :
                    evenement=heure+";"+IP_source+";"+IP_destination+";"+txt_flag+";"+" "+";"+txt_ack+";"+txt_win

    valeur.append(evenement)
    if "Flags [.]" in row:
        point+=1
    elif "Flags [P.]" in row:
        point_P+=1
    elif "Flags [S.]" in row:
        point_S+=1
    elif "Flags [S]" in row:
        S+=1

lecture()



for j in range (len(valeur)):
    valeur_split=valeur[j].split(",")
    liste_valeur_split.append(valeur_split)

titre="heure"+";"+"IP_source"+";"+"IP_destination"+";"+"flag"+";"+"seq"+";"+"ack"+";"+"win"+";"+"option"+";"+"leght"
with open(namecsv,'w',newline='') as fichiercsv:
    writer=csv.writer(fichiercsv)
    writer.writerow([titre])
    #writer.writerow("\n")
    for i in range (len(liste_valeur_split)):
        writer.writerow(liste_valeur_split[i])

#Graphe
labels = 'point','point P','Point S','S'
sizes = [point,point_P,point_S,S]
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
plt.pie(sizes, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')
plt.savefig(namediagram)
plt.show()

fh.close()
fichiercsv.close()