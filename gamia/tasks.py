from celery import shared_task
from datetime import datetime , timedelta
from .models import Gamia, GamiaUser
from users.models import User
from reports.models import Report


def create_report (body,user,gamia) : 
    rep = Report.objects.create(
        user = user,
        gamia=gamia,
        body = body
    )

    rep.save()

@shared_task
def SetMembersRecivedAtDates(gamia_id) :
    gamia = Gamia.objects.get(id=gamia_id)
    gamiaMembers = GamiaUser.objects.filter(gamia=gamia)
    current_date = datetime.now()
    
    gamia.started_at = current_date.date()
    gamia_end_at = current_date

    for member in gamiaMembers :
        new_date = gamia_end_at + timedelta(days=gamia.pay_every_days)
        member.recived_money_at = new_date.date()
        gamia_end_at = new_date
        member.save()
    
    gamia_end_at = gamia_end_at + timedelta(days=1)
    gamia.end_at = gamia_end_at.date()
    gamia.save()


@shared_task
def PayForEachGamia() :
    current_date = datetime.now().date()
    AllGamia = Gamia.objects.filter(end_at__gt=current_date)

    for gamia in AllGamia : 
        gamia_users = GamiaUser.objects.filter(gamia=gamia)
        collected_gamia_balance = 0

        for gamia_user in gamia_users : 
            user:User = gamia_user.user
            if user.balance > gamia.price_per_user:
                collected_gamia_balance = collected_gamia_balance + gamia.price_per_user
                user.balance = user.balance - gamia.price_per_user
                user.save()
            else:
                # create report for unpayed user
                report_body = f""" 
                        User With id "{user.id}" who named "{user.full_name}" and his email is "{user.email}" and Mobile "{user.cash_phone}",
                        didn't pay in gamia "{gamia.title}" at "{current_date}", because he don't have balance to implement the payment.
                        the current user balance at "{current_date}" is {user.balance} EGP. 
                    """
                create_report(
                    body=report_body,
                    user=user,
                    gamia=gamia
                )
                

        gamia.current_balance = collected_gamia_balance
        gamia.save()

@shared_task
def Gamia_Users_Transations() : 
    try : 
        members = GamiaUser.objects.filter(hasReceived=False)
        current_date = datetime.now().date()

        for member in members:
            if current_date == member.recived_money_at :
                            
                if member.gamia.current_balance != member.gamia.total :
                    user = member.user
                    gamia = member.gamia
                    report_body = f""" 
                            User With id "{user.id}" who named "{user.full_name}" and his email is "{user.email}" and Mobile "{user.cash_phone}",
                            didn't recive his full gamia money as he just recived {member.gamia.current_balance} EGP and he must recived in his gamia
                            {member.gamia.total} EGP, and there is still {member.gamia.total - member.gamia.current_balance} EGP must sent to him.
                        """
                    create_report(
                        body=report_body,
                        user=user,
                        gamia=gamia
                    )
                    
                member.user.balance = member.user.balance + member.gamia.current_balance
                member.gamia.current_balance = 0
                member.hasReceived = True
                member.save()
                member.user.save()
                member.gamia.save()

    except Exception as error :
        print(f'an error accoured : {error}')