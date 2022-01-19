import math
import sys, os

from pandas import *
import pandas as pd
from numpy import *
import numpy as np
import random
import re
from sys import *

# ubicacion = input(str("Hola para leer tu archivo indicame la direccion y el archivo como tal y su extension: "))

df = pd.read_excel("./play_db.xlsx", sheet_name=0)


def NaiveBayes():
    iter = int(input("Numero de iteraciones: "))
    listSumColum = []
    ListAttributeString = []
    ListAttributeNumeric = []
    TableFrecuencyString = []
    TableFrecuencyNumeric = []
    CountTest = 0  # CONTADOR DE FILAS DE PRUEBA
    CountTrainer = 0  # CONTADOR DE FILAS DE ENTRENAMIENTO
    ListTrainer = []  # FILAS QUE SERAN DE ENTRENAMIENTO
    NumIteraciones = 0  # CANTIDAD DE VECES QUE SE VA ITERAR LA FUNCION ZERO-R
    MaxRows = df.shape[0]  # CANTIDAD MAXIMA DE FILAS DEL DATA FRAME
    CountTrainer = MaxRows * 0.7  # CANTIDAD DE FILAS DE ENTRENAMIENTO 70%
    CountTest = MaxRows - int(CountTrainer)  # CANTIDAD DE FILAS DE PRUEBAS
    print("La cantidad de Filas del Dataframe es: ", df.shape[0])
    print("Cantidad de filas para Entrenamiento:  ", int(CountTrainer))
    print("Cantidad de filas para Pruebas:  ", int(CountTest))

    # CANTIDAD DE VECES QUE SE VA ITERAR EL ZERO-R
    for a in range(iter):

        print("\n \n \n _____________________Iteración numero ", str(a + 1), "_____________________")
        # SE CREA LA LISTA DE ENTRENAMIENTO CON NUMEROS RANDOM
        ListTrainer = random.sample(range(int(MaxRows)), int(CountTrainer))
        ListTest = range(int(MaxRows))
        ListTest = list(ListTest)

        # SE CREA UNA LISTA CON TODOS LOS VALORES Y SE ELIMINAN LOS DE LISTA DE ENTRENAMIENTO
        for x in ListTrainer:
            ListTest.remove(x)

        # CREAMOS DATAFRAME EN BASE EL INDICE DE LISTA DE ENTRENAMIENTO
        DataFrameTrainer = df.loc[ListTrainer]
        # CREAMOS DATAFRAME EN BASE EL INDICE DE LA LISTA DE PRUEBAS
        DataFrameTest = df.loc[ListTest]
        print("\n---Datos de Entrenamiento---")
        print(DataFrameTrainer)
        print("\n---Datos de Prueba---")
        print(DataFrameTest)
        # OBTENEMOS LOS NOMBRES DE LAS COLUMNAS
        columns_names = list(DataFrameTrainer.columns.values)
        # OBTENEMOS LA COLUMNA CLASE
        ClassName = columns_names.pop()
        # EN ESTE APARTADO IMPRIMIMOS LA CLASE QUE MAS SE REPITE LA CANTIDAD DE VECES QUE SE ENCUENTRA TANTO EN EL DATAFRAME DE PRUEBA Y ENTRENAMIENTO
        DataFrameTrainerNumeric =  DataFrameTrainer.select_dtypes(include=['int64', 'float64'])
        DataFrameTrainerString = DataFrameTrainer.select_dtypes(include=['object', 'bool'])

        columns_numeric = list(DataFrameTrainerNumeric.columns.values)
        columns_string = list(DataFrameTrainerString.columns.values)

        # AGREGANDO ETIQUETAS DE LOS ATRIBUTOS
        for a in columns_string:
            ListAttributeString.append(DataFrameTrainerString[a].unique().tolist())

        # SE CONSTRUYE LAS TABLAS DE FRECUENCIA
        count = 0
        for y in ListAttributeString:
            TableFrecuencyString.append(pd.crosstab(index=DataFrameTrainerString[columns_string[count]],
                                                    columns=DataFrameTrainerString[ClassName]))
            count += 1

        # AGREGANDO ETIQUETAS DE LOS ATRIBUTOS
        for a in columns_numeric:
            ListAttributeNumeric.append(DataFrameTrainerNumeric[a].unique().tolist())

        # SE CONSTRUYE LAS TABLAS DE FRECUENCIA
        count = 0
        for y in ListAttributeNumeric:
            TableFrecuencyNumeric.append(pd.crosstab(index=DataFrameTrainerNumeric[columns_numeric[count]],
                                                     columns=DataFrameTrainer[ClassName]))
            count += 1

        for y in range(0, len(TableFrecuencyString) - 1):
            numpy_array = TableFrecuencyString[y].to_numpy()
            TableFrecuencyString[y][:] = numpy_array + 1
            listSumColum.append(TableFrecuencyString[y].sum())

        # for b in x:
        #     for d in b:
        #         listFT.append(str(str(d) + str("/") + str(listSumColum[0][0])))
        # x[b] = str(str(d) + str("/") + str(listSumColum[0][0]))

        # x[c] = str(str(c) + str("/") + str(listSumColum[0][0]))
        # x[:] = str(str(1) + str("/") + str(listSumColum[0][0]))

        ValuesClass = DataFrameTrainer[ClassName].unique()
        ValuesClass.sort()
        print(TableFrecuencyString)
        for a in ValuesClass:
            for b in range(0, len(TableFrecuencyString)):
                if len(TableFrecuencyString) == len(TableFrecuencyString):
                    f = CountTrainer
                    TableFrecuencyString[b].loc[TableFrecuencyString[b][a] != '', a] = TableFrecuencyString[b][a] / f
                else:
                    f = TableFrecuencyString[b][a].sum()
                    TableFrecuencyString[b].loc[TableFrecuencyString[b][a] != '', a] = TableFrecuencyString[b][a] / f

        DataFrameNumericColumnNames = list(DataFrameTrainer.select_dtypes(include=['int64', 'float64']).columns.values)
        print(TableFrecuencyNumeric)
        listaDictori = []
        ListaPromedio = []
        ListaDesviacion = []
        count = 0
        for b in DataFrameNumericColumnNames:
            for a in ValuesClass:
                v = DataFrameTrainer.loc[DataFrameTrainer[ClassName] == a]
                dict = {a: list(v[b].values)}
                listaDictori.append(dict)
                prom = {a: np.array(list(listaDictori[count].values())).mean()}
                ListaPromedio.append(prom)
                des = {a: np.std(np.array(list(listaDictori[count].values())), ddof=1)}
                ListaDesviacion.append(des)
                count += 1

        print(listaDictori)
        print("Promedio: ",ListaPromedio)
        print("Desviación: ",ListaDesviacion)
        print(TableFrecuencyString)
        ColumnsNameString= DataFrameTest.select_dtypes(include=['object', 'bool']).columns.values
        ColumnsNameString = list(ColumnsNameString)
        ColumnsNameString.pop()
        print(ColumnsNameString)
        play = TableFrecuencyString.pop()
        play = list(pd.Series(np.diag(play), index=[play.index, play.columns]))
        TotalSi = 1
        TotalNo = 1
        for muestra in range(len(DataFrameTest)): # Valores de prueba
            print(DataFrameTest.iloc[muestra])

            countString = 0
            CountNumerico =1
            for ValorClass in  ValuesClass:
                Total = []
                if(ValorClass == "No"):
                    Total.append(play[0])
                elif(ValorClass == "Yes"):
                    Total.append(play[1])
                    print("Aquí", play[1])
                countString = 0
                CountNumerico = 1
                for column in ColumnsNameString: # for que multiplica los valores que no son numericos
                    valor = DataFrameTest[column].iloc[muestra] # Nombre de las filas de las tablas de frecuencia
                    print("valor: ", valor)
                    Total.append( TableFrecuencyString[countString].loc[valor,ValorClass])
                    countString +=1
                for numerico in DataFrameNumericColumnNames:
                    valor = DataFrameTest[numerico].iloc[muestra]  # Nombre de las filas de las tablas de frecuencia
                    if(ValorClass == "No"):
                        promedio = ListaPromedio[(CountNumerico*len(DataFrameNumericColumnNames))-2].get(ValorClass) # si es yes se le suma uno
                        desviacion = ListaDesviacion[(CountNumerico * len(DataFrameNumericColumnNames)) - 2].get(ValorClass)
                        Total.append(DistribucionNormal(promedio,desviacion,valor))
                    elif(ValorClass == "Yes"):# Si el valor de la clase es Yes

                        promedio = ListaPromedio[(CountNumerico * len(DataFrameNumericColumnNames)) - 1].get(ValorClass)  # si es yes se le suma uno
                        desviacion = ListaDesviacion[(CountNumerico * len(DataFrameNumericColumnNames)) - 1].get(ValorClass)
                        Total.append(DistribucionNormal(promedio, desviacion, valor))
                    CountNumerico += 1

                print("___________________________________________________________________________-")
                for x in Total :

                     if(ValorClass== "Yes"):
                        TotalSi = TotalSi * x
                     else:
                         TotalNo =  TotalNo * x
                print("TotalSí = ", TotalSi)
                print("TotalNo = ", TotalNo)
                print("Total", Total)
                print ("Caso yes",TotalSi /(TotalSi+TotalNo))
                print("Caso No", TotalNo / (TotalNo + TotalSi))
                print("*===================================================0")
                if(TotalSi  > TotalNo):
                    print("La mejor opción es Sí ")
                else:
                    print("La mejor opción es No")

                #sys.exit()

        sys.exit()

    #os.system("PAUSE")
    #print("\n" * 100)

def DistribucionNormal(media,desv,x):
        total = 1/(sqrt(2*math.pi)*desv)*math.e**-(((x-media)**2)/(2*desv**2))
        return total




while True:
    print("1) nayve Bayes")
    print("0) Salir")
    op = input()

    if op == "1":
        NaiveBayes()

    elif op == "2":
        OneR()

    elif op == "0":
        break
