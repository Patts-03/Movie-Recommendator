import pandas as pd

def extract():
    df_mov = pd.read_csv('movies.csv', encoding='latin')            
    df_rats = pd.read_csv('ratings.csv', encoding='latin')

    return df_mov,df_rats

def transform(df_mov,df_rats,wanted):
    df_title = df_mov['title']
    df_genre = df_mov['genres']
    df_ratings = df_rats['rating']

    movie_index=[]
    for a in range(len(df_genre)):
        genre = df_genre[a]
        options = []
        new_g=''
        for i in range(len(genre)):
            if genre[i] != '|':
                new_g += genre[i]
            else:
                options.append(new_g)
                new_g = ''

        if wanted in options:
            movie_index.append(a)

    return movie_index,df_title,df_ratings

def load(movie_index,df_title,df_ratings):

    num = int(input('\nHow many films would you like to be recommended? (Introduce 0 if you want all our results) : '))
    if (len(movie_index)-1) < num:
        print("\nSorry, we've just found",len(movie_index)-1," coincidences")
        num = len(movie_index)-1
    elif num == 0:
        num = len(movie_index)-1

    print("\nBased on your initial choice, we are sure you'll love these films")
      
    for a in range(num):
        index = movie_index[a]
        title = df_title[index]
        rate = df_ratings[index]
        print('\n- Title:', title,'\n ---> Rated:',rate)

    print('\n -- We hope you enjoy our recommendation --\n')

    return


if __name__=='__main__':
    valid = False
    genres_list = ['Action','Adventure','Animation', "Childrend's", 'Comedy' , 'Crime', 'Documentary','Drama','Fantasy','Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi','Thriller','War', 'Western']
    
    # Inicio el programa y hago un print de los géneros
    print('\nWelcome to your movie recommendator!\n''Please introduce one of the following genres in order to be recommended a new film:\n ')
    for genre in genres_list:
        print('-',genre)
    
    # Obtenemos el género base y ponemos en marcha la búsqueda
    
    wanted = input('\nYour choice: ')
    while not valid:
        if wanted not in genres_list:
            print("Your choice doesn't exist. Please write it down again(It must be identical to the shown list)")
            wanted = input('\nYour choice: ')
        else:
            valid = True
    print("Now we'll search in out database. Please be patient")

    df_mov,df_rats = extract()
    movie_index,df_title,df_ratings = transform(df_mov,df_rats,wanted)
    load(movie_index,df_title,df_ratings)




