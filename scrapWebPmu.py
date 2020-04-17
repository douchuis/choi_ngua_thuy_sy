from bs4 import BeautifulSoup
from time import sleep
import requests
from selenium import webdriver
import csv 
import pandas as pd 

"""
Cette fonction va collecter les données des courses de chevaux sur le site de la loterie romande.
En utilisant Selenium, cette fonction retourne un fichier csv
"""

def pmuScrapingRomande(url):
    ##------------------------ changes in this part only --------------------------------- ##
    driver = webdriver.Chrome()
    url = url
    driver.get(url)
    nameCsv = url[37:57]
    # https://jeux.loro.ch/horses/raceCard/20200416_R2_R2C4?date=2020-04-16

    ### Pour une course déjà terminée
    #element = driver.find_element_by_xpath("""//*[@id="root"]/main/section/div/div/section/nav/ul/li[3]/p""")
    #element.click()

    ### supprimer des lettres spéciales
    def delSpeLetter(text):
        for x in text:
            if x not in 'abcdefghijklmnopqrstuvwyzABCDEFGHIJKLMNOPQRSTUVWYZ ':
                text = text.replace(x,'')
        return text

    ### on va regarder la liste des cheveaux qui vont faire de la course
    tempsAttente = 2

    sleep(tempsAttente)
    listePartante =[]
    listeNumber = driver.find_elements_by_class_name('participant-list__item-info__heading-number')
    sleep(tempsAttente)
    listeRun = driver.find_elements_by_class_name('participant-list__item-odds__number')
    sleep(tempsAttente)
    print('le nombre de chevaux dans la course')
    print(len(listeNumber))
    print('--'*20)
    print(len(listeRun))
    print('--'*20)
    for number,run in zip(listeNumber,listeRun):
        if run.text != '-':
            listePartante.append(number.text)
        sleep(tempsAttente)
    ### la liste des partants en int 

    listePartante = [int(x) for x in listePartante]
    print("la liste des chevaux partants")
    print(listePartante)

    ###chercher les informations des chevaux de la course
    links = driver.find_elements_by_class_name('collapsible__section')
    counterLinks = 0
    ## fiche de cheval
    listeInfos = [1,2,3,4,9,10]

    ### main programe

    ### écrire les données dans la un fichier csv
    dataFile = 'data_{0}.csv'.format(nameCsv)
    with open(dataFile, mode='w') as horseRacing:
        horseRacing.write('number,name_horse,horse_age,weight,race_place,distance,prize,win_odd,draw,entraineur,proprietaire,sex\n')
        for link in links:
            if counterLinks < len(listePartante):

                ### le numéro de chaque cheval
                print('--'*20)
                print(listePartante[counterLinks])
                number = listePartante[counterLinks]
                print('--'*20)

                ### nom des chevaux
                horseName =driver.find_element_by_xpath("""
                //*[@id="root"]/main/section/div[1]/div/section/div[2]
                /div[1]/div/section[{0}]/header/div/div[1]/div/div/div
                /h2/span[2]
                """.format(listePartante[counterLinks]))
                print('Nom du cheval: ' + horseName.text)
                horse_name = delSpeLetter(horseName.text)
                ### la côte de chaque cheval
                odd = driver.find_element_by_xpath("""
                //*[@id="root"]/main/section/div/div/section/div/div[1]
                /div/section[{0}]/header/div/div[2]/span
                """.format(listePartante[counterLinks]))
                print('la côte: ' + odd.text)
                win_odd = odd.text
                ### cliquer sur les informations de chaque cheval
                link =driver.find_element_by_xpath("""
                //*[@id="root"]/main/section/div[1]/div/section/div[2]/div[1]/div/section[{0}]
                """.format(listePartante[counterLinks]))
            #     //*[@id="root"]/main/section/div/div/section/section/div[1]/div/section[{0}]
            #     //*[@id="root"]/main/section/div[1]/div/section/div[2]/div[1]/div/section[{0}]

                link.click()
                sleep(tempsAttente)
                ### fiche du cheval

                for x in listeInfos:
                    linke = driver.find_element_by_xpath("""
                    //*[@id="root"]/main/section/div/div/section/div[2]/div[1]/
                    div/section[{0}]/article/section/div/div/div[2]/div/div[2]/
                    div/table/tbody/tr[{1}]/td""".format(listePartante[counterLinks],x))

                    ## pour la course à l'avenir
                    """
                    //*[@id="root"]/main/section/div/div/section/div[2]/div[1]/
                    div/section[{0}]/article/section/div/div/div[2]/div/div[2]/
                    div/table/tbody/tr[{1}]/td
                    """

                    ## pour la course déjà terminé
                    """
                    //*[@id="root"]/main/section/div/div/section/section/div[1]
                    /div/section[{0}]/article/section/div/div/div[2]/div/div[2]
                    /div/table/tbody/tr[{1}]/td
                    """

                    if linke != None:
                        if x == 1 : 
                            print('Entraîneur: ' + linke.text)
                            entraineur = delSpeLetter(linke.text)
                        elif x == 2 :
                            print('Propriétaire: ' + linke.text)
                            proprietaire = delSpeLetter(linke.text)
                        elif x == 3 :
                            print('Sex: ' + linke.text)
                            sex = linke.text
                            if sex == 'MÂLE':
                                sex = 'MALE'
                        elif x == 4 :
                            print('Âge: ' + linke.text)
                            age = linke.text
                        elif x == 9 :
                            print('Poids(kg): ' + linke.text.replace('Kg',''))
                            poid = linke.text.replace('Kg','')
                        else:
                            print('Corde: ' + linke.text)
                            corde = linke.text

                    else:
                        print('hallo quoi !')
                    sleep(tempsAttente)

                ### changer de la fiche 
                sleep(tempsAttente)
                changeFiche = driver.find_element_by_xpath("""
                //*[@id="root"]/main/section/div[1]/div/section/div[2]
                /div[1]/div/section[{0}]/article/section/div/div/div[3]
                """.format(listePartante[counterLinks]))
                changeFiche.click()
                sleep(tempsAttente)

                ### performance 
                linkPlace = driver.find_element_by_xpath("""
                //*[@id="root"]/main/section/div[1]/div/section/div[2]
                /div[1]/div/section[{0}]/article/section/div/div/div[2]
                /div/div[3]/div/table[2]/tbody/tr[3]/td""".format(listePartante[counterLinks]))
                ### Places
                sleep(tempsAttente)
                print( 'Places: ' + linkPlace.text)
                place = linkPlace.text

                ### Pour la course déjà terminée
                """...
                """
                ### Pour la course à l’avenir
                """
                //*[@id="root"]/main/section/div/div/section/div[2]/div[1]
                /div/section[{0}]/article/section/div/div/div[2]/div/div[3]
                /div/table[2]/tbody/tr[3]/td
                """

                linkGain = driver.find_element_by_xpath("""
                //*[@id="root"]/main/section/div[1]/div/section/div[2]
                /div[1]/div/section[{0}]/article/section/div/div/div[2]
                /div/div[3]/div/table[2]/tbody/tr[4]/td""".format(listePartante[counterLinks]))
                sleep(tempsAttente)
                ### Gain en carrière
                print('Gain en carrière(frs): ' + linkGain.text.replace("'",""))
                gainCarriere = linkGain.text.replace("'","")

                ### xpath Pour la course déjà terminée
                """...
                """
                ### xpath Pour la course à l’avenir
                """
                //*[@id="root"]/main/section/div/div/section/div[2]/div[1]
                /div/section[{0}]/article/section/div/div/div[2]/div/div[3]
                /div/table[2]/tbody/tr[4]/td
                """

                ### Distance de la course 
                distance = driver.find_element_by_xpath("""
                //*[@id="root"]/main/div/article[2]/section/div/div[3]/div[1]/p
                """)
                print('Distance(m): ' + distance.text.replace('m',''))
                distanceCourse = distance.text.replace('m','')
                counterLinks += 1
                sleep(tempsAttente)
            else:
                break

            sleep(tempsAttente)
            horseRacing.write(str(number) + ','+ horse_name + ','+ age + ','+ poid + ','+ place + ','+ distanceCourse + ','+ gainCarriere + ','+ win_odd + ','+ corde + ','+ entraineur + ','+ proprietaire + ','+ sex + '\n')

    res = driver.execute_script("return document.documentElement.outerHTML")

    return dataFile
