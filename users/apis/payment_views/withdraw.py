from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from payment.models import Withdraw

class WithdrawView(APIView) : 
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request,**kwargs) :
        user:User = request.user
        amount = request.data.get('amount',0)
        amount = float(amount)

        if amount > user.balance or user.balance == 0 :
            return Response({
                'message' : 'invalid amount'
            },status=status.HTTP_400_BAD_REQUEST)

        user.balance = round((user.balance - amount),2)
        user.save()

        wd = Withdraw.objects.create(
            user = user,
            mobile_cash = user.cash_phone,
            amount = amount
        )

        wd.save()

        return Response(status=status.HTTP_200_OK)
    
