from .services import MyService

class MyServiceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Initialize your service when the middleware is executed
        api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkZDQ1ZmFmNzJkMzIyZmJiMzYwY2I3OTYzNmI2NTQwYiIsInN1YiI6IjY1ZDlmNWRjNGU0ZGZmMDE3Y2I4NzUxOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.M-XxT8D7MjHmjdKmlfUfjW8uLaT97lOQJW7Pvp6e-sk'
        my_service = MyService(api_key)

        # Attach the service instance to the request object
        request.my_service = my_service

        response = self.get_response(request)

        return response