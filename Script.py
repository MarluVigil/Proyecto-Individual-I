import pandas as pd
import numpy as np
import datetime as date
from sqlalchemy import create_engine
import sqlalchemy as db

#Ingesta de archivo
ruta=str(input('coloque ruta: '))
#archivo = open(ruta,'r',sep='|')
#letra = archivo.read()
dataFrame=pd.read_table(ruta,'r')#, sep='|')

#pasar a string
dataFrame.iloc[:1]=dataFrame.iloc[:1].astype(str)

#cambiar cantidad de digitos para codigo EAN
dataFrame.iloc[:,1]=dataFrame.iloc[:,1].str.zfill(13)

#contar y transformar nulos
def nulos (dataFrame):
    if dataFrame.isnull().sum().sum()>0:
        promedio=round(dataFrame.iloc[:0].mean(),2)
        dataFrame.iloc[:0].fillna(promedio,inplace=True)
        dataFrame.dropna()
    return dataFrame
dFrame=dataFrame.apply(nulos)
#print(dFrame)

#contar y borrar duplicados
def duplicados (dFrame):
    if dFrame.duplicated().sum()>0:
        dframe=dFrame.drop_duplicates()
    return dframe
dF=dataFrame.apply(duplicados)

#Agregar columna fecha
fecha=input('Coloque fecha de archivo: ')
dF[fecha]=fecha
dF[fecha]=pd.to_datetime(dF[fecha])

#renombrar columnas para asegurarnos que coincida con las anteriores
tabla=dF.set_axis(['precio', 'producto_id', 'sucursal_id', 'Date'], axis=1)

#guardo el archivo en carpeta 
tabla.to_csv(r'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\tabla.csv', index=False)

#Conexión con MySql
database_username='root' 
database_password=input('coloque contraseña: ')
database_ip='localhost'
database_name='db'
database_conection=db.create_engine(f'mysql+pymysql://{database_username}:{database_password}@{database_ip}/{database_name}')
coneccion=database_conection.connect()
metadata=db.MetaData()

tabla.to_sql('TablaPrec',coneccion)
