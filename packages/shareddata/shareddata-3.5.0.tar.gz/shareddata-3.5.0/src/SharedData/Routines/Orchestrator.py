# PROPRIETARY LIBS
import os,sys,time
from datetime import datetime

from SharedData.SharedData import SharedData
shdata = SharedData('SharedData/Routines/Orchestrator',user='master')
from SharedData.Logger import Logger
from SharedData.Routines.Scheduler import RoutineScheduler

if len(sys.argv)>=2:
    SCHEDULE_NAME = str(sys.argv[1])
else:
    Logger.log.error('SCHEDULE_NAME not provided, please specify!')
    raise Exception('SCHEDULE_NAME not provided, please specify!')

Logger.log.info('SharedData Routines orchestrator starting for %s...' % (SCHEDULE_NAME))

sched = RoutineScheduler(SCHEDULE_NAME)
sched.UpdateRoutinesStatus()
sched.save()

lastheartbeat = time.time()
while(True):    
    Logger.log.debug('#heartbeat#,schedule:%s' % (SCHEDULE_NAME))

    if sched.schedule['Run Times'][0].date()<datetime.now().date():
        print('')
        print('Reloading Schedule %s' % (str(datetime.now())))
        print('')
        sched.LoadSchedule()
        sched.UpdateRoutinesStatus()

    sched.UpdateRoutinesStatus()
    sched.RunPendingRoutines()    
    time.sleep(5)