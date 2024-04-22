from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

class JWTAuthenticationMiddleware:
    """
    Middleware for authenticating requests using JSON Web Tokens (JWT).

    Exempts certain paths from authentication based on `exempt_paths`.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware.

        Args:
            get_response (callable): The next middleware in the chain or the view.
        """
        self.get_response = get_response
        self.exempt_paths = ['/login', '/register']

    def __call__(self, request):
        """
        Process incoming requests.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            HttpResponse: The response to be returned.
        """
        if any(request.path.startswith(path) for path in self.exempt_paths):
            return self.get_response(request)

        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return JsonResponse({"error": "Authorization header missing"}, status=401)
        print("Auth header:", auth_header)
        try:
            auth = JWTAuthentication()
            print("Authenticating...")
            user, _ = auth.authenticate(request)
            print("Authenticated user:", user)
            if user is None:
                raise AuthenticationFailed("Invalid or expired token")
            request.user = user
        except AuthenticationFailed as e:
            return JsonResponse({"error": str(e)}, status=401)

        response = self.get_response(request)
        return response
