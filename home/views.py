from django.shortcuts import render
from django.http import HttpResponse
from .services import MyService


def home(request):
    api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkZDQ1ZmFmNzJkMzIyZmJiMzYwY2I3OTYzNmI2NTQwYiIsInN1YiI6IjY1ZDlmNWRjNGU0ZGZmMDE3Y2I4NzUxOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.M-XxT8D7MjHmjdKmlfUfjW8uLaT97lOQJW7Pvp6e-sk'
    my_service = MyService(api_key)
    result = my_service.perform_action()
    
   
    context = {
        'message': result
    }
    return render(request, 'home/index.html',context)
def recommend_movies(request):
    if request.method == 'POST':
        movie_name = request.POST.get('movie_name')
        number = request.POST.get('number')
        if movie_name:
            my_service = request.my_service
            num_mov=int(number)
            recommended_movies = my_service.get_recommendations(movie_name,num_mov)
            recommended_movies_list = recommended_movies.reset_index().to_dict(orient='records')
            return render(request, 'home/recommendations.html', {'recommended_movies': recommended_movies_list})
        else:
            return HttpResponse('Please provide a movie name.')
    else:
        return render(request, 'home/recommendations.html')
