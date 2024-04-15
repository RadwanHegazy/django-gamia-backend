from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from users.models import User
from payment.models import Payment

class SuccessView (APIView) : 
    permission_classes = [permissions.IsAuthenticated]

    def get (self, request, payment_id,*kwargs) : 
        
        try :
            payment = Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

        user:User = request.user

        if payment.isExpired or payment.user != user :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        payment.isExpired = True
        payment.status = "success"

        total = user.balance + payment.amount
        user.balance = round(total,2)

        user.save()
        payment.save()

        return Response(status=status.HTTP_200_OK)



