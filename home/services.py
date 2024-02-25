import requests
import pandas as pd
from fuzzywuzzy import process
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
class MyService:
    df = None
   
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
            print(MyService.df)

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
    def get_recommendations(self,movie_title):
        self.df['genre_ids'] = self.df['genre_ids'].apply(lambda x: ' '.join(map(str, x)))
        self.df['content'] = self.df['genre_ids'] + ' ' + self.df['original_language'] + ' ' + self.df['release_date'].astype(str) + ' ' + self.df['vote_average'].astype(str) + ' ' + self.df['vote_count'].astype(str) + ' ' + self.df['popularity'].astype(str)
        vectorizer = CountVectorizer()
        content_matrix = vectorizer.fit_transform(self.df['content'])
        cosine_sim = cosine_similarity(content_matrix, content_matrix)
        title = self.movie_finder(movie_title)
        movie_idx = dict(zip(self.df['title'], list(self.df.index)))
        idx = movie_idx[title]
    
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]  
        movie_indices = [i[0] for i in sim_scores]
        return self.df['title'].iloc[movie_indices]

    def fetch_top_rated_movies(self, num_pages=40):
        all_movies = []

        for page in range(1, num_pages + 1):
            response = requests.get(self.url.format(page), headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                movies = data.get('results', [])
                all_movies.extend(movies)
            else:
                print(f"Error on page {page}: {response.status_code}")

        return pd.DataFrame(all_movies)