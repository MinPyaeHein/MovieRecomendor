from django.shortcuts import render
from django.http import HttpResponse
from .services import MyService


def home(request):
    api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkZDQ1ZmFmNzJkMzIyZmJiMzYwY2I3OTYzNmI2NTQwYiIsInN1YiI6IjY1ZDlmNWRjNGU0ZGZmMDE3Y2I4NzUxOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.M-XxT8D7MjHmjdKmlfUfjW8uLaT97lOQJW7Pvp6e-sk'
    my_service = MyService(api_key)
    result = my_service.perform_action()
    rec_movies=my_service.get_recommendations('Avatar')
    print(rec_movies)
    context = {
        'message': result
    }
    return render(request, 'home/index.html',context)
def recommend_movies(request):
    if request.method == 'POST':
        movie_name = request.POST.get('movie_name')
        if movie_name:
            # Access the service instance from the request object
            my_service = request.my_service

            # Use the service methods or properties
            recommended_movies = my_service.get_recommendations(movie_name)

            # Convert the DataFrame to a list of dictionaries
            recommended_movies_list = recommended_movies.reset_index().to_dict(orient='records')
            # Pass the recommended movies to the template
            return render(request, 'home/recommendations.html', {'recommended_movies': recommended_movies_list})
        else:
            return HttpResponse('Please provide a movie name.')
    else:
        return render(request, 'home/recommendations.html')
