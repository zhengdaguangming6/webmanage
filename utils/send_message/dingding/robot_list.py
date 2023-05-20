import schedule
import time


class ScheduleTask:

    def run_task(self, task_name, times=1, unit="", time=""):
        if time:
            if unit == "seconds":
                schedule.every(times).seconds.at(time).do(task_name)
        else:
            if unit == "seconds":
                schedule.every(times).seconds.at(time).do(task_name).run()



    def cancel_task(self,):
        pass


def fun1():
    print("你好啦")

if __name__ == "__main__":
    # a = ScheduleTask()
    # b = 0
    # while b < 6:
    #     a.run_task(eval("func1"), unit="seconds")
    #     b += 1
    schedule.every(5).seconds.do(fun1)

    while True:
        schedule.run_pending()
        time.sleep(1)

