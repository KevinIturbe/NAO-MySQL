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
#Se verifica nuevamente que no existan duplicados
tweets.duplicated().sum()

# %%
#Se verifican valores nulos
tweets.isna().sum()

# %%
#Explorando el tipo de dato
tweets["texto"].dtype

# %%
#Se utiliza astype para convertir el tipo object generico a str
tweets["texto"] = tweets["texto"].astype(str)

# %%
tweets["texto"] = tweets["texto"].str.lower()

# %%
#Se modifica la opción para visualizar los datos
pd.set_option('display.max_colwidth', None)

# %%
#Se muestra la columna texto antes de ser modificada.
tweets["texto"].head(15)

# %%
#Se eliminan enlaces
tweets["texto"] = tweets["texto"].replace(r'http\S+', '', regex=True)


# %%
tweets["texto"].head(15)

# %%
#Se eliminan hashtags
tweets["texto"] = tweets["texto"].replace(r'#\S+', '', regex=True)

# %%
# Usamos un regex que busca patrones de URLs o dominios
tweets["texto"] = tweets["texto"].replace(r'\b\w+\.com\.uy\b', '', regex=True)

# %%
tweets["texto"].tail(15)


# %%
#Se eliminan menciones
tweets["texto"] = tweets["texto"].replace(r'@\S+', '', regex=True)

# %%
tweets["texto"] = tweets["texto"].replace('[^a-zA-Z0-9áéíóúüñ\s]', '', regex=True)

# %%
#Se visualizan los datos limpios
tweets["texto"].head()

# %%
#Se importa nltk 
import nltk 
from nltk.corpus import stopwords

#Dercargar las stopwords
nltk.download('stopwords')

#Se obtiene la lista de stopwords en español
stop_words = set(stopwords.words('spanish'))

# %%
#Se importa textblob
from textblob import TextBlob

# %%
def analizar_sentimiento(texto):
    analisis = TextBlob(texto)
    # El valor de polarity va de -1 (negativo) a 1 (positivo)
    return analisis.sentiment.polarity

tweets['sentimiento'] = tweets['texto'].apply(analizar_sentimiento)

# %%
tweets.head()

# %%
tweets.sort_values(by='sentimiento', ascending=True).head(5)

# %%
#Conocer el promedio 
tweets["sentimiento"].mean()

# %%
def analizar_subjetividad(texto):
    analisis = TextBlob(texto)
    return analisis.sentiment.subjectivity

tweets['subjetividad'] = tweets['texto'].apply(analizar_subjetividad)

# %%
tweets["subjetividad"].mean()

# %%
tweets.sort_values(by=["fecha"])

# %%
# Agrupar los tweets por día y calcular el promedio de polaridad (sentimiento)
tweets_diarios = tweets.groupby(tweets['fecha'].dt.date)['sentimiento'].mean().reset_index()

# Renombrar las columnas para mayor claridad
tweets_diarios.columns = ['fecha', 'promedio_sentimiento']


# %%
tweets.to_csv("nuevos_datos.csv")


