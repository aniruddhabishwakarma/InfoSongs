from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from spotify_app.serializers.user_serializer import UserProfileSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    print("🔥 USER ID:", request.user.id)

    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)