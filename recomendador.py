import pandas as pd
import re

def extract():
    df_mov = pd.read_csv('movies.csv', encoding='latin')            

    return df_mov

def transform_mov(df_mov,movie):
    df_title = df_mov['title']
    df_genre = df_mov['genres']
    fin = False
    index = 0
    coincidences = 0
    options_comp = []
    complete_g_index = []


    # Búsqueda de la película en el dataset y de películas con su mismo género completo
    while not fin:
        title = df_title[index]
        is_title = re.search(movie,title,re.IGNORECASE)

        if is_title != None:
            complete_gen = df_genre[index]    
            options_comp = re.split('\|', complete_gen)

            for a in range(len(df_genre)):
                genre = df_genre[a]
                options = re.split('\|', genre)
                for option in options:
                    if option in options_comp:
                        coincidences += 1 
                if coincidences >=2:
                    complete_g_index.append(a)
                coincidences = 0
            fin = True

        elif index == (len(df_title)-1):
            fin = True
            
        index += 1

    # Si lo hemos encontrado, buscamos en el dataset películas que coincidan en 2 géneros o más con ella

    if is_title == None:
        return None , None ,None                                                # Si no encontramos la película en el dtaset, devolvemos False
    else:
        return complete_g_index,df_title, df_genre

def transform_gen(df_mov,wanted):
    df_title = df_mov['title']
    df_genre = df_mov['genres']
    
    # Extracción del género por película 
    movie_index=[]

    for a in range(len(df_genre)):
        genre = df_genre[a]
        options = re.split('\|', genre)

        if wanted in options:
            movie_index.append(a)
        
    return movie_index,df_title, df_genre

def load(movie_index,df_title,df_genres):

    num = int(input('\nHow many films would you like to be recommended? (Introduce 0 if you want all our results) : '))
    if (len(movie_index)-1) < num:
        print("\nSorry, we've just found",len(movie_index)-1,"coincidences")
        num = len(movie_index)-1
    elif num == 0:
        num = len(movie_index)-1

    print("\n - Suggestions -")
    
    for a in range(num):
        index = movie_index[a]
        title = df_title[index]
        genre = df_genres[index]
        print('\n- Title:', title,'\n ---> Complete genre:',genre)

    print('\n -- We hope you enjoy our recommendation --\n')

    return

if __name__=='__main__':
    valid = False
    genres_list = ['Action','Adventure','Animation', "Children", 'Comedy' , 'Crime', 'Documentary','Drama','Fantasy','Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi','Thriller','War', 'Western']
    
    # Inicio el programa y hago un print de los géneros
    print('\nWelcome to your movie recommendator!\n\n''Please introduce one of the following genres in order to be recommended a new film:\n ')
    for genre in genres_list:  
        print('-',genre)
    
    
    # Obtenemos el género base y la película y ponemos en marcha la búsqueda
    
    wanted = input('\nYour genre choice: ')
    while not valid:
        if wanted not in genres_list:
            print("Your choice doesn't exist. Please write it down again(It must be identical to the shown list)")
            wanted = input('\nYour choice: ')
        else:
            valid = True
            
    print("\nNow please write a movie you'd want your recommendation to be similar to ")
    movie = input('\nYour movie: ')
    
    print("Now we'll search in our database. Please be patient")

    df_mov = extract()

    # Utilizamos primero el transform que busca la película dada
    complete_g_index,df_title, df_genres = transform_mov(df_mov,movie)

    if (complete_g_index , df_title, df_genres) == (None, None , None):
        print('\nUnfortunately, your movie choice is not in our database. We will base our recommendations in your genre choice')
        movie_index,df_title,df_genres = transform_gen(df_mov,wanted)
        load(movie_index,df_title,df_genres)
    else:
        print('\nWe foud your movie. These following films have at least 2 genres in common with it')
        load(complete_g_index,df_title, df_genres)
