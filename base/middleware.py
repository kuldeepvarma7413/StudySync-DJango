# from django.contrib.auth.middleware import AuthenticationMiddleware
# from django.http import HttpResponseRedirect
# from django.shortcuts import redirect
# from django.urls import reverse

# class AdminHomepageRedirectMiddleware(AuthenticationMiddleware):

#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Here I call login if not authenticated and request is not login page
#         if not request.user.is_authenticated and request.path != reverse('login'):
#             return HttpResponseRedirect(reverse('login'))  
#         response = self.get_response(request)
#         return response