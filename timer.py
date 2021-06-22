from apscheduler.schedulers.background import BackgroundScheduler
from models import Download, User

scheduler = BackgroundScheduler()


@scheduler.scheduled_job('cron', second='*/7')
def sensor():
    print("MUDOU")
    cliente = User.query.filter_by(role='Cliente')

    if cliente:
        for item in cliente:
            idc = item.id
            leads = item.leads
            down = Download.query.filter_by(cliente=idc)
            if down:
                for i in down:
                    i.qtd += leads

    else:
        print("Erro")


# , day=30
def start():
    scheduler.start()
