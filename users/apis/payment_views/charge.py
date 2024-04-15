from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
import stripe
from backend import settings
from payment.models import Payment

class ChargeView(APIView) : 
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request,**kwargs) : 
        data = request.data
        user_email = request.user.email
        amount = data.get('amount',None)

        if amount is None :
            return Response({
                'message' : 'please enter the amount'
            },status=status.HTTP_400_BAD_REQUEST)
        
        
        amount = float(amount)
        
        if amount < 100 :
            return Response({
                'message' : 'amount should be more than 100 EGP'
            },status=status.HTTP_400_BAD_REQUEST)

        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        payment = Payment.objects.create(
            amount = amount,
            user = request.user
        )

        payment.save()

        redirect_to = f"http://127.0.0.1:8000/payment/{payment.id}"
        """
        add to this link
            1- payment_uuid
        """

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'egp',
                    'unit_amount': int(amount) * 100, 
                    'product_data': {
                        'name': 'Payment',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            # here you should return to the frontend server no backend
            success_url=f'{redirect_to}/success/',
            cancel_url=f'{redirect_to}/cancel/',
            customer_email=user_email
        )

        return Response({
            'payment_link' : session.url
        },status=status.HTTP_200_OK)
    
