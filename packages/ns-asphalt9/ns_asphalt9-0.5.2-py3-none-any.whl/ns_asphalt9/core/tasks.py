import threading

from datetime import datetime
from . import consts, globals, actions
from .utils.log import logger


class TaskManager:
    timers = []
    status = consts.TaskStatus.default
    current_task = ""
    notify_list = []

    @classmethod
    def task_init(cls):
        if "任务" not in globals.CONFIG:
            return
        car_hunt_task = None
        for task in globals.CONFIG["任务"]:
            if task["运行"] > 0 and task["间隔"]:
                timer = cls.task_producer(task["名称"], task["间隔"])
                cls.timers.append(timer)
                if task["名称"] in [consts.car_hunt_zh, consts.legendary_hunt_zh]:
                    car_hunt_task = task["名称"]
        if car_hunt_task:
            globals.task_queue.put(car_hunt_task)
        else:
            globals.task_queue.put(globals.CONFIG["模式"])

    @classmethod
    def task_producer(cls, task, duration, skiped=False):
        if skiped:
            globals.task_queue.put(task)
        else:
            logger.info(f"Start task {task} producer, duration = {duration}min")
            skiped = True
        timer = threading.Timer(
            duration * 60, cls.task_producer, (task, duration), {"skiped": skiped}
        )
        timer.start()
        return timer

    @classmethod
    def destroy(cls):
        for t in cls.timers:
            t.cancel()

    @classmethod
    def task_dispatch(cls, page) -> None:
        if "任务" not in globals.CONFIG:
            return False

        if page.name not in [
            consts.world_series,
            consts.limited_series,
            consts.trial_series,
            consts.carhunt,
            consts.card_pack,
            consts.legend_pass,
            consts.legendary_hunt,
            consts.daily_events,
            consts.multi_player,
            consts.grand_prix,
            consts.career,
            consts.empty,
        ]:
            return False

        cls.shop_notify_producer()

        if globals.task_queue.empty():
            if cls.status == consts.TaskStatus.done:
                cls.task_enter(globals.CONFIG["模式"], page=page)
                cls.status = consts.TaskStatus.default
                return True
        else:
            task = globals.task_queue.get()
            logger.info(f"Get {task} task from queue.")
            cls.status = consts.TaskStatus.start
            cls.current_task = task
            cls.task_enter(task, page)
            return True

    @classmethod
    def task_enter(cls, task, page=None) -> None:
        logger.info(f"Start process {task} task.")
        if task in [consts.mp1_zh, consts.mp2_zh, consts.mp3_zh]:
            actions.enter_series(page=page)
        if task == consts.car_hunt_zh:
            actions.enter_carhunt(page=page)
        if task == consts.free_pack_zh:
            actions.free_pack()
        if task == consts.prix_pack_zh:
            actions.prix_pack()
        if task == consts.legendary_hunt_zh:
            actions.enter_legend_carhunt(page=page)
        if task == consts.restart:
            actions.restart()
        if task == consts.shop_notify:
            actions.shop_notify()

    @classmethod
    def set_done(cls) -> None:
        if cls.status == consts.TaskStatus.start:
            cls.status = consts.TaskStatus.done
            cls.current_task = ""

    @classmethod
    def shop_notify_status(cls) -> bool:
        for task in globals.CONFIG["任务"]:
            if task["名称"] == "商店通知" and task["运行"] > 0:
                return True
        return False

    @classmethod
    def shop_notify_producer(cls) -> None:
        if "通知" not in globals.CONFIG or not cls.shop_notify_status():
            return
        now_utc = datetime.utcnow()
        # 北京时间17点，20点, 凌晨2点
        if now_utc.hour in [9, 12, 18] and now_utc.minute < 10:
            notify_key = f"{now_utc.month}_{now_utc.day}_{now_utc.hour}"
            if notify_key not in cls.notify_list:
                cls.notify_list.append(notify_key)
                globals.task_queue.put(consts.shop_notify)
