import requests
import pandas as pd
from fuzzywuzzy import process
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
class MyService:
    df = None
    df_original = None
    all_movies=[]
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = 'https://api.themoviedb.org/3/movie/top_rated?language=en-US&page={}'
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'accept': 'application/json'
        }

        # Check if df is already loaded, if not, load it
        if MyService.df is None:
            MyService.df = self.fetch_top_rated_movies(10)
            MyService.df_original = MyService.df

    # Initialize merged_df only if it's None
       
    def perform_action(self):
        # Your business logic goes here
        result = f"Performing action with parameter: {self.api_key}"
        return result
    
    def movie_finder(self,title):
        title = str(title)
        all_titles = [str(t) for t in self.df['title'].tolist()]
        closest_match = process.extractOne(title, all_titles)
        return closest_match[0]
    def get_recommendations(self, movie_title, n_recommendations):
        genres = set()
        for genre_list in self.df['genre_ids']:
            for genre in genre_list:
                genres.add(genre)

        for genre in genres:
            self.df[genre] = self.df['genre_ids'].transform(lambda x: int(genre in x))

        movie_genres = self.df.drop(columns=['id', 'original_language', 'original_title','title', 'overview', 'genre_ids', 'backdrop_path', 'popularity', 'poster_path', 'release_date', 'vote_average', 'vote_count', 'adult', 'video'])
        
        cosine_sim = cosine_similarity(movie_genres, movie_genres)
        title = self.movie_finder(movie_title)
        movie_idx = dict(zip(self.df['title'], list(self.df.index)))
        idx = movie_idx[title]  
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:n_recommendations]
        movie_indices = [i[0] for i in sim_scores]
        recommendations_df = self.df_original.loc[movie_indices, ['title', 'genre_ids','overview']]
        return recommendations_df
    def fetch_top_rated_movies(self, num_pages=40):
        print (f"Fetching top rated movies.....")

        for page in range(1, num_pages + 1):
            response = requests.get(self.url.format(page), headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                movies = data.get('results', [])
                self.all_movies.extend(movies)
            else:
                print(f"Error on page {page}: {response.status_code}")
            MyService.df=pd.DataFrame(self.all_movies)
            MyService.df_original=pd.DataFrame(self.all_movies)
            
        return pd.DataFrame(self.all_movies)