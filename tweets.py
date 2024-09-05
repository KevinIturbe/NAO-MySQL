# %%
#Se importa Pandas
import pandas as pd

# %%
#Se leen los tweets 
tweets = pd.read_json(r"C:\Users\Kevin\Documents\NAO\MySQL\data\tweets_extraction.json")

# %%
#Se comienza a explorar los datos
tweets.info()

# %%
tweets.head()

# %%
#Se convierte la columna fecha al formato correcto
tweets['fecha'] = pd.to_datetime(tweets["fecha"])

# %%
#Se verifica que se hayan aplicado exitosamente los cambios
tweets.info()

# %%
#Se comprueba con otro atributo las columnas
print(tweets.dtypes)

# %%
#Como la columna hashtag contiene listas no se puede verificar las filas duplicadas
tweets.hashtags.head()

# %%
#Se utiliza apply para poder acceder a las listas de hashtag ya que no son elementos hashtables
tweets.hashtags = tweets["hashtags"].apply(tuple)

# %%
tweets.head()

# %%
no_duplicados = tweets.duplicated().sum()
no_duplicados

# %%
duplicados = tweets[tweets.duplicated()]

# %%
#Se exploran los duplicados
duplicados.head()

# %%
#Se eliminan los registros duplicados, por defecto se mantiene el primer registro de los duplicados
#Se utiliza el argumento inplace para aplicar la eliminación directamente en el DataFrame
tweets.drop_duplicates(subset=['id'], keep=False, inplace=True)

# %%
#Se verifica nuevamente que no existan duplicados, se utiliza la variable previamente definida
no_duplicados

# %%
#Se verifican valores nulos
tweets.isna().sum()

# %%
#se importa el modulo para la conexión
import mysql.connector

# %%
#Se establece la conexión
conexion = mysql.connector.connect(
    host="localhost",        
    user="root",       
    password="Nocturno00?", 
    database="TweetsDB"       
)

# %%
#Se crea el cursor
cursor = conexion.cursor()
cursor.execute("SET innodb_lock_wait_timeout = 180")

# %%
# SQL para insertar datos en la tabla Tweets
sql_insert = """
INSERT INTO Tweets (id, texto, usuario, hashtags, fecha, retweets, favoritos)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

# Iterar sobre las filas del DataFrame y ejecutar la inserción
for index, row in tweets.iterrows():
    # Convertir la tupla de hashtags a una cadena de texto
    hashtags_str = ', '.join(row['hashtags']) if row['hashtags'] else None
    
    # Ejecutar el comando SQL
    cursor.execute(sql_insert, (
        row['id'],
        row['texto'],
        row['usuario'],
        hashtags_str,
        row['fecha'].strftime('%Y-%m-%d %H:%M:%S'),
        row['retweets'],
        row['favoritos']
    ))

# %%
# Confirmar los cambios en la base de datos
conexion.commit()

# %%
#Se termina la conexión
cursor.close()
conexion.close()


