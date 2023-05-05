from cron.controllers.runner import CronRunner


def start():
    cron_runner = CronRunner()
    cron_runner.start()


# if __name__ == '__main__':
#     start()

