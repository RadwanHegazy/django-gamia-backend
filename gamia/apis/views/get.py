from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from ...models import Gamia, GamiaUser

class GetAllUserGamia (APIView) : 
    permission_classes = [permissions.IsAuthenticated]

    def get (self, request, **kwargs) : 
        user = request.user

        data = [
            {
                'id' : str(i.gamia.id),
                'title' : i.gamia.title,
                'start_at' : i.gamia.started_at,
                'end_at' : i.gamia.started_at,
            } 
            for i in GamiaUser.objects.filter(user=user)
        ]

        return Response(data,status=status.HTTP_200_OK)
    
