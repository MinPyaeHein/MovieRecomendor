from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import MyService

@api_view(['GET'])
def home_api(request):
    api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkZDQ1ZmFmNzJkMzIyZmJiMzYwY2I3OTYzNmI2NTQwYiIsInN1YiI6IjY1ZDlmNWRjNGU0ZGZmMDE3Y2I4NzUxOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.M-XxT8D7MjHmjdKmlfUfjW8uLaT97lOQJW7Pvp6e-sk'
    my_service = MyService(api_key)
    result = my_service.perform_action()
    current_df_shape=my_service.df.shape
    # my_service.fetch_top_rated_movies(20)
    return Response({'current_df_shape': current_df_shape})

@api_view(['POST'])
def update_train_data_api(request):
    if request.method == 'POST':
        number = request.data.get('number_of_pages')
        if number:
            my_service = request.my_service
            num_mov=int(number)
            movies_df=my_service.fetch_top_rated_movies(num_mov)
            return Response({'updateDataSetShape':movies_df.shape}) 
        else:
            return Response({'error': 'Please provide Number Of Pages'}, status=400)
    else:
        return Response(status=405)  


@api_view(['POST'])
def recommend_movies_api(request):
    if request.method == 'POST':
        movie_name = request.data.get('movie_name')
        number = request.data.get('number')
        if movie_name:
            my_service = request.my_service
            num_mov=int(number)
            recommended_movies = my_service.get_recommendations(movie_name,num_mov)
            recommended_movies_list = recommended_movies.reset_index().to_dict(orient='records')
            return Response({'recommended_movies': recommended_movies_list})
        else:
            return Response({'error': 'Please provide a movie name.'}, status=400)
    else:
        return Response(status=405)  