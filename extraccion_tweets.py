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
tweets.drop_duplicates(subset="id",inplace=True)

# %%
#Se verifica nuevamente que no existan duplicados, se utiliza la variable previamente definida
no_duplicados

# %%
#Se verifican valores nulos
tweets.isna().sum()


