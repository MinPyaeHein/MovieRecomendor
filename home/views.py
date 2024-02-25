from django.shortcuts import render
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