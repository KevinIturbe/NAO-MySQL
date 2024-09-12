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
tweets["texto"].head(15)

# %%
tweets["texto"] = tweets["texto"].replace(r'https://\S+', '', regex=True)

# %%
tweets["texto"].head(15)

# %%
tweets["texto"] = tweets["texto"].replace(r'#\S+', '', regex=True)

# %%
# Usamos un regex que busca patrones de URLs o dominios
tweets["texto"] = tweets["texto"].replace(r'\b\w+\.com\.uy\b', '', regex=True)

# %%
tweets["texto"].head()

# %%
tweets["texto"] = tweets["texto"].replace(r'@\S+', '', regex=True)

# %%
tweets["texto"] = tweets["texto"].replace('[^a-zA-Z0-9áéíóúüñ\s]', '', regex=True)

# %%
tweets["texto"].head()

# %%
tweets["tokens"] = tweets["texto"].str.split()

# %%
tweets["tokens"]

# %%
#Se importa nltk 
import nltk 
from nltk.corpus import stopwords

#Dercargar las stopwords
nltk.download('stopwords')

#Se obtiene la lista de stopwords en español
stop_words = set(stopwords.words('spanish'))

# %%
#Se obtiene la frecuencia
frecuencias = [palabra for linea in tweets["tokens"] 
               for palabra in linea
               if palabra not in stop_words]

# %%
#Se importa el módulo Counter de la librería collections para hacer el conteo de frecuencia de palabras.
from collections import Counter

# %%
frec_palabra = Counter(frecuencias)

# %%
print(frec_palabra.most_common(20))

# %%
#Seleccionando las palabras más comunes.
top_palabras = frec_palabra.most_common(20)

# %%
df_palabras = pd.DataFrame(top_palabras, columns=["palabra", "frecuencia"])

# %%
df_palabras.to_csv("top_palabras.csv")

# %%
from textblob import TextBlob
from collections import defaultdict

# %%
tweets.texto

# %%
# Diccionarios para almacenar la suma de polaridad, subjetividad y frecuencia
polaridad_palabra = defaultdict(float)
subjetividad_palabra = defaultdict(float)
frecuencia_palabra = defaultdict(int)

# Iterar sobre cada tweet en la columna 'texto'
for _, fila in tweets.iterrows():
    texto = fila['texto']  # Obtener el texto completo del tweet
    analisis = TextBlob(texto)  # Analizar el sentimiento del tweet completo
    polaridad = analisis.sentiment.polarity  # Polaridad del tweet
    subjetividad = analisis.sentiment.subjectivity  # Subjetividad del tweet

    # Tokenizar manualmente el texto (puedes ajustarlo si ya está tokenizado)
    palabras = texto.split()  # Dividir el texto en palabras

    # Asignar la polaridad y subjetividad del tweet a cada palabra
    for palabra in palabras:
        polaridad_palabra[palabra] += polaridad
        subjetividad_palabra[palabra] += subjetividad
        frecuencia_palabra[palabra] += 1

# Crear una lista final con la polaridad y subjetividad promedio por palabra
polaridad_subjetividad_promedio = []

for palabra, frec in frecuencia_palabra.items():
    polaridad_promedio = polaridad_palabra[palabra] / frec
    subjetividad_promedio = subjetividad_palabra[palabra] / frec
    polaridad_subjetividad_promedio.append({
        'palabra': palabra,
        'polaridad_promedio': polaridad_promedio,
        'subjetividad_promedio': subjetividad_promedio
    })




# %%
df_resultado = pd.DataFrame(polaridad_subjetividad_promedio)
df_resultado

# %%
pol_sub_palabra =df_resultado[df_resultado.palabra.isin(df_palabras["palabra"])]

# %%
pol_sub_palabra.to_csv("pol_sub_palabra.csv")


