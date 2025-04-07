# spotify_app/views/user_views.py
from rest_framework import generics, permissions
from spotify_app.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv
import os 
from django.contrib.auth import get_user_model

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")



class GoogleLoginAPIView(APIView):
    def post(self, request):
        token = request.data.get("id_token")
        if not token:
            return Response({"error": "Missing ID token"}, status=400)

        try:
            # ✅ Secure token verification using env-based client ID
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), GOOGLE_CLIENT_ID
            )

            email = idinfo.get("email")
            name = idinfo.get("name", "")
            google_id = idinfo.get("sub")
            picture = idinfo.get("picture")

            if not email:
                return Response({"error": "Email not provided by Google"}, status=400)

            User = get_user_model()
            user, created = User.objects.get_or_create(email=email, defaults={
                "username": email.split("@")[0],
                "first_name": name,
                "is_google_user": True,
                "google_id": google_id,
                "profile_picture": picture,
            })

            # 🔄 Update if needed
            if not created:
                user.is_google_user = True
                user.google_id = user.google_id or google_id
                user.profile_picture = user.profile_picture or picture
                user.save()

            # 🎫 Generate access/refresh tokens
            refresh = RefreshToken.for_user(user)
            print(str(refresh.access_token))
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })

        except ValueError:
            return Response({"error": "Invalid ID token"}, status=400)
