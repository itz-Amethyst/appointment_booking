from django.shortcuts import redirect

class RedirectToDocsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request path is the root URL
        if request.path == '/':
            return redirect('/api/docs')
        response = self.get_response(request)
        return response
