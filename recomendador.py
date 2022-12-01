import pandas as pd
import re, signal, sys


def handler_signal(signal, frame):

    print('You pressed Ctrl+C!')
    sys.exit(0)


#Preguntar a Federico si se puede poner esto dentro del main
#Asigno la señal de interrupción a la función handler_signal para que se ejecute cuando se pulse Ctrl+C
signal.signal(signal.SIGINT, handler_signal)

ARCHIVO = "./imdb.csv"

def extract(csv):

    #Lee el archivo csv y lo guarda en un dataframe
    df = pd.read_csv(csv) 
    return df


def transform(df):

    #Elimina las columnas que no nos interesan"
    df = df.drop(columns=['Date','Votes','Duration','Type','Certificate','Episodes','Nudity','Violence','Profanity','Alcohol','Frightening'])

    #Guardar en una lista los valores de 'Genre' del dataframe
    lista = df['Genre'].tolist()

    #Ponemos todos los valores de la lista separados por comas
    lista = ', '.join(lista)
    lista = lista.split(', ')

    #Eliminamos los valores repetidos y así tenemos todos los géneros
    generos = set(lista)

    #Mostramos los géneros disponibles de una forma más estética
    print('Géneros disponibles: ', re.sub(r"[{}'']", '', str(generos)) + '\n')

    #Pedimos al usuario que introduzca el género que quiere buscar
    print('Mostraremos las 10 mejores series/películas según el género que elijas.')

    #Recogemos el género introducido por el usuario sin importar si introduce mayúsculas o minúsculas
    genero = re.findall(str(input('Género: ')), str(generos), re.IGNORECASE)

    #Si el género introducido no está en la lista de géneros disponibles, se le vuelve a pedir que introduzca un género
    if genero:
        print('El género que has elegido es correcto.')
    else:
        print('El género que has elegido no es correcto. Vuelve a intentarlo.')
        sys.exit(0)

    #Busca las filas que contengan el género deseado
    df = df[df['Genre'].str.contains(genero[0])]

    #Elimina las filas que 'Rate' sea igual a 'No Rate'
    df = df[df['Rate'] != 'No Rate']

    #Ordena el dataframe por la columna "Rate" de forma descendente
    df = df.sort_values(by=['Rate'], ascending=False)

    #Quito la columna 'Genre', ya que no me interesa que se muestre
    df =df.drop(columns=['Genre'])

    #No quiero que muestren los índices iniciales
    df = df.reset_index(drop=True)

    #Empieza los indices en 1 para que se vea como un top 10
    df.index = df.index + 1
    
    return df

def load(df):

    #Muestra las 10 primeras filas del dataframe
    df = df.head(10)

    return print(df)


if __name__ == "__main__":
    df = extract(ARCHIVO)
    df = transform(df)
    df = load(df)

