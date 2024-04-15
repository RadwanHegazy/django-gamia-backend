from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from ..serializers import CreateGamiaSerialzier

class CreateGamia (APIView) : 
    serializer_class = CreateGamiaSerialzier
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request,**kwargs) : 
        serializer = self.serializer_class(data=request.data,context={'user':request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'id' : serializer.data['id']
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
