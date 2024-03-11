import threading

from django.core.management import BaseCommand

from ticket_tracking.telegram_bot import bot


def start_bot_polling():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)


class Command(BaseCommand):
    help = 'Run bot separate thread'

    def handle(self, *args, **options):
        threading.Thread(target=start_bot_polling).start()
        self.stdout.write(self.style.SUCCESS('Bot is running'))

