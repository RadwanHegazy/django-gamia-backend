from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from ...models import Gamia, GamiaUser
from ..serializers import GamiaUserSerializer
from gamia.tasks import SetMembersRecivedAtDates
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
    


class GetGamia (APIView) : 
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, gamia_id) :
        try : 
            gamia = Gamia.objects.get(id=gamia_id)
        except Gamia.DoesNotExist :
            return Response({
                'message' : 'gamia not found'
            },status=status.HTTP_404_NOT_FOUND)
        
        user = request.user
        UserInGamia = GamiaUser.objects.filter(user=user,gamia=gamia).exists()
        GamiaMembers = GamiaUser.objects.filter(gamia=gamia)
        TotalGamiaUsers = GamiaMembers.count()

        if not UserInGamia :

            if TotalGamiaUsers < gamia.max_users_count:
                gm = GamiaUser.objects.create(
                    user = user,
                    gamia=gamia
                )
                gm.save()

                if TotalGamiaUsers + 1 == gamia.max_users_count :
                    print('start celery task') 
                    SetMembersRecivedAtDates.delay(gamia_id)

            else:
                return Response({
                    'message' : "gamia arrived to max users"
                },status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            'gamia' : {
                'title' : gamia.title,
                'members_count': TotalGamiaUsers,
                'every_days_count' : gamia.pay_every_days,
                'price_per_user' : gamia.price_per_user,
                'total_money_per_user' : gamia.total,
                'current_balance' : gamia.current_balance,
                'start_at' : gamia.started_at,
                'end_at' : gamia.end_at,
            },
            'members' : GamiaUserSerializer(GamiaMembers,many=True).data
        }

        return Response(data,status=status.HTTP_200_OK)

            