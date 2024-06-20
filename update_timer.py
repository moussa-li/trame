# import datetime
# import threading
# from apscheduler.schedulers.blocking import BlockingScheduler
# from pathlib import Path

# __all__ = [
#     "UpdateTimer"
# ]

# class UpdateTimer:
#     """
#     控制数据的刷新
#     通过定时查询当前数据版本更新数据
#     """
#     def __init__(self, updateFun, interval = 1.0):
#         self.updateFun = updateFun
#         self.version = 0    
#         self.interval = interval if interval > 0.0 else 1.0

#         self.sched = BlockingScheduler()
#         self.sched.add_job(self.UpdateFun, 'interval', seconds = interval)
#         self.thread = threading.Thread(target = self.LaunchSchedule)

#     def __del__(self):
#         self.Stop()

#     def UpdateFun(self):
#         path = Path(__file__).parent / "work_dir/version.txt"
#         if(path.exists()):
#             # 打开版本文件获取当前结果版本号
#             versionFile = open(path.absolute(), 'rb')
#             currentVersion = int(versionFile.read())
#             versionFile.close()

#             # 版本更新时调用更新回调
#             if(currentVersion > self.version):
#                 self.updateFun()
#                 self.version = currentVersion

#     def LaunchSchedule(self):
#         self.sched.start()

#     def Start(self):
#         self.thread.start()

#     def Stop(self):
#         self.sched.shutdown(wait = False)
#         self.thread.stop()