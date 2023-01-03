from core.models import UserProfile
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import SignupSerializer


class SignupAPIView(APIView):
    """
    API view for sign up API
    """
    permission_classes = []

    def post(self, request):
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('confirm_password', None)

        if password == confirm_password:
            serializer = SignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            response = status.HTTP_201_CREATED
        else:
            data = ''
            raise ValidationError(
                {'password_mismatch': 'Password fields did not match.'}
            )

        return Response(data, status=response)