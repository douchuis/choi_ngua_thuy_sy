def predictionChevauxCourse(dataFile):
    """
    Cette fonction va prédire les chevaux gagnant de la course en
    appliquant le réseau de neuronnes pour créer son modèle.
    """

    import pandas as pd
    import numpy as np

    # import runs.csv
    runs = pd.read_csv('../runs.csv')
    # import races.csv
    races = pd.read_csv("../races.csv")

    # changer en franc suisse
    races['prize'] = races['prize'] / 7.98

    # sélectionner les features nécessaires
    runs_data = runs[['race_id', 'won',
            'actual_weight', 'draw', 'win_odds','horse_age'
           ]]

    races_data = races[['race_id', 'race_class','distance','prize']]
    # races_data.head()

    ### le nombre de colonnes à entraîner
    cols = 7

    # merge the two datasets based on race_id column
    df = pd.merge(runs_data, races_data)
    # df.head(100)

    # contrôler et nettoyer les données
    df.isnull().sum()
    df = df.dropna()
    # # drop the unnecessary columns
    df = df.drop(columns=['race_id'])
    df.won.value_counts()

    ## Over-Sampling
    from sklearn.utils import resample
    # separate minority and majority classes
    not_won = df[df.won==0]
    won = df[df.won==1]

    # upsample minority
    won_upsampled = resample(won,
                              replace=True, # sample with replacement
                              n_samples=len(not_won), # match number in majority class
                              random_state=27) # reproducible results

    # combine majority and upsampled minority
    upsampled = pd.concat([not_won, won_upsampled])

    # check new class counts
    upsampled.won.value_counts()

    # 2.Séparer les données d'entraînement
    from sklearn.model_selection import train_test_split
    X = upsampled.drop(['won'],axis=1).values
    y = upsampled['won'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    ### 3. Transformer les données
    # transformer les données
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    ### 4. Construire le réseau de neuronnes artificiels
    # input layers, hidden layers, output layers
    import keras
    from keras.models import Sequential
    from keras.layers import Dense
    # pour nitialiser une pile linéaire de calques.
    classifier = Sequential()
    # ajouter des couches au réseau
    # paramètre 1: le nombre de noeux ||la moyenne des noeuds dans la couche d'entrée et la couche de sortie
    # paramètre 2: initialisation les poids, à des nombres proches de zéro, mais pas de zéro.
    # paramètre 3: modèle d'apprentissage en profondeur apprendra à travers cette fonction d'activation
    # paramètre 4: le nombre d'entités dans la donnée
    #'la première couche input layer'
    classifier.add(Dense(9, kernel_initializer = "uniform",activation = "relu", input_dim=cols))

    #'la couche sortie output layers'
    ### paramètres ###
    # le nombre de noeud de sortie 
    # la fonction  d'activation sigmod, aide à obtenir la probabilité de la sortie
    classifier.add(Dense(1, kernel_initializer = "uniform",activation = "sigmoid"))

    # une gradient descente au réseau de neurones.
    # qui sert à réduire les erreurs pendant le processus de formation.
    # en distribuant de manière aléatoire dans un réseau nouronal. 
    # *** paramètre ***
    # une des stratégie d'optimisation adam  (la descente du gradient)
    # loss:prédit la perte 
    # métrique : évalue le modèle.

    classifier.compile(optimizer= 'adam',loss = "binary_crossentropy",metrics = ["accuracy"])

    # entrainer le modèle, 
    # batch_size : représente le nombre d'échantillon qui passeront par le réseau 
    # de neurones à chaque cycle de formation 
    # epochs : représente le nombre de fois que l'ensemble de données sera transmi via le réseau de neurones
    # plus le nombre d'époches est long, plus le modèle fonctionera longtemps, 
    # ce qui donnera également de meilleurs résultats.
    classifier.fit(X_train, y_train,validation_split=0.2, batch_size = 31, epochs = 30)
    # from sklearn.model_selection import cross_val_score
    # accuracies = cross_val_score(estimator = classifier,X = X_train,y = y_train,cv = 10,n_jobs = -1)

    # # # la moyenne 
    # mean = accuracies.mean()
    # print('la moyenne: ' +  str(mean)) 

    # # la variance des précisions
    # variance = accuracies.var()
    # print('la variance: '+ str(variance) )

    ### 5. Exécution de prévision sur le test

    from sklearn.metrics import confusion_matrix, classification_report
    y_pred = classifier.predict(X_test)
    # print(classification_report(y_test, y_pred))

    y_pred = (y_pred > 0.5)

    print('La prédiction du modèle:' )
    print(y_pred)

    ### 6. Vérification de la matrice de confusion

    cm = confusion_matrix(y_test, y_pred)
    print('La confusion matrice du modèle: ')
    print(cm)

    ### 7. Faire une prédiction unique
    print('Le rapport du modèle: ')
    print(classification_report(y_test, y_pred))

    ## Prédiction le modèle 
    data_test = pd.read_csv(dataFile)

    print('la donnée collectée: ')
    print(data_test.head(10))

    X_deploy = data_test[['weight','draw','win_odd','horse_age','race_place','distance','prize']].values
    # y_deploy_test = data_test['won'].values

    #mettre à l'échelle les données
    # X_deploy = X_deploy.values
    print("La mise à l'échelle les données: ")
    print(X_deploy)
    print('---'*30)
    X_deploy = sc.transform(X_deploy)
    # print(X_deploy)
    print('---'*30)
    ## print(y_deploy_test)      

    ## prédiction 
    y_deploy_pred = classifier.predict(X_deploy)

    y_deploy_pred = y_deploy_pred > 0.5
    print('La prédiction du déploiment du modèle: ')
    print(y_deploy_pred)
    