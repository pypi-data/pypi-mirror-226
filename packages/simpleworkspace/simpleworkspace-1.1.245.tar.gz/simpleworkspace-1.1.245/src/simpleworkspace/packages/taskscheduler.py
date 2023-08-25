from logging import Logger as _Logger
from abc import ABC as _ABC
from datetime import datetime as _datetime, timedelta as _timedelta
from ..types.time import TimeSpan as _TimeSpan
from ..settingsproviders import SettingsManager_JSON as _SettingsManager_JSON
from ..utility.stopwatch import StopWatch as _StopWatch
from time import sleep as _sleep
import os as _os
from zlib import crc32 as _crc32
from ..utility import module as _module
from ..io import directory as _directory

class ITask(_ABC):
    task_Interval = None  # type: _TimeSpan
    task_Ignore = False

    def __init__(self) -> None:
        if(self.task_Interval is None):
            raise NotImplementedError("task_interval not specified for instance")
        self.task_id = self.__class__.__module__ + "." + self.__class__.__name__
        self._task_nextSchedule = _datetime.min

    def On_StartUp(self):
        pass

    def On_Schedule(self):
        pass


class TaskSchedulerManager:
    def __init__(self, settingsPath: str, logger: _Logger) -> None:
        self.logger = logger
        self._settingsPath = settingsPath
        self._settingsManager = _SettingsManager_JSON(self._settingsPath)
        self._settingsManager.LoadSettings()
        self._tasks = {} #type: dict[str, ITask]
        self._activeTaskList = [] #type: list[ITask]
        self._flag_SaveSettings = False

    def Run(self):
        self._InitializeTasks()
        self.logger.info(f"Event Start")

        def StopwatchStrFormat(stopwatch: _StopWatch):
            return f"{stopwatch.GetElapsedMilliseconds(decimalPrecision=2)} MS"
        
        for task in self._activeTaskList:
            stopwatch = _StopWatch()
            stopwatch.Start()
            try:
                task.On_StartUp()
                self.logger.info(f"Event On_StartUp[{StopwatchStrFormat(stopwatch)}]: {task.task_id}")
            except Exception:
                self.logger.exception(f"Event On_StartUp failed[{StopwatchStrFormat(stopwatch)}]: {task.task_id}")
                continue
            

        while True:
            for task in self._activeTaskList:
                stopwatch = _StopWatch()
                stopwatch.Start()
                try:
                    if self._ScheduledTask_ShouldRun(task):
                        task.On_Schedule()
                        self._ScheduledTask_SetNextSchedule(task)
                        self.logger.info(f"OnSchedule Event[{StopwatchStrFormat(stopwatch)}]: {task.task_id}")
                except Exception as e:
                    self.logger.exception(f"Event On_Schedule Failed[{StopwatchStrFormat(stopwatch)}]: {task.task_id}")
            self.SaveSettingsIfNeeded()
            _sleep(1)

    def SaveSettingsIfNeeded(self):
        if(self._flag_SaveSettings): #instead of saving after each small modification, change after one full task iteration if needed
            self._settingsManager.SaveSettings()
            self._flag_SaveSettings = False
            
    def _ScheduledTask_ShouldRun(self, task: ITask):
        if( _datetime.now() > task._task_nextSchedule):
            return True
        return False
    
    def _ScheduledTask_SetNextSchedule(self, task: ITask):
        task._task_nextSchedule = _datetime.now() + _timedelta(seconds=task.task_Interval.InSeconds())
        self._settingsManager.Settings["TaskSchedules"][task.task_id]["next"] = task._task_nextSchedule.isoformat()
        self._flag_SaveSettings = True
        return

    def LoadTasks(self, tasks: list[ITask]):
        for task in tasks:
            if not isinstance(task, ITask):
                raise TypeError(f"Task must be of type ITask, got {type(task)}")
            self._tasks[task.task_id] = task
        return self

    def LoadTasksFromFile(self, path:str):
        if(not _os.path.isfile(path)):
            raise FileNotFoundError(path)
        
        taskInstances = []
        
        dynamicModuleName = f"{_os.path.basename(path)}_{_crc32(path.encode())}"
        dynamicModule = _module.ImportModuleDynamically(dynamicModuleName, path)
        dynamicModuleInfo = _module.ModuleInfo(dynamicModule)
        classes = dynamicModuleInfo.GetDeclaredClasses(ITask, includeChildsOnly=True)
        for className,obj in classes.items():
            taskInstances.append(obj())

        self.LoadTasks(taskInstances)  

        return self

    def LoadTasksFromDirectory(self, path:str, recursive=True):
        if(not _os.path.isdir(path)):
            raise NotADirectoryError(path)
        
        maxRecursionDepth = None if recursive == True else 1
        taskInstances = []
        pyFiles = _directory.List(path, 
                             includeDirs=False, 
                             includeFilter='/\.py$/i',
                             maxRecursionDepth=maxRecursionDepth)
        for filepath in pyFiles:
            self.LoadTasksFromFile(filepath)

        return self

    def _InitializeTasks(self):
        for task in self._tasks.values():
            if(task.task_Ignore):
                continue
            self._activeTaskList.append(task)
                
        if("TaskSchedules" not in self._settingsManager.Settings):
            self._settingsManager.Settings["TaskSchedules"] = {}
            self._flag_SaveSettings = True
            

        #clear invalid/old settings
        for key in list(self._settingsManager.Settings["TaskSchedules"].keys()):
            if(key not in self._tasks): #this includes ignored tasks aswell, since we dont want to reset it's schedule when its temporarily ignored
                del self._settingsManager.Settings["TaskSchedules"][key]
                self._flag_SaveSettings = True

        #register tasks
        taskSchedulesSettings = self._settingsManager.Settings["TaskSchedules"]
        for taskID, task in self._tasks.items():
            #if this is a new task, or task interval has changed, then set to trigger them right away
            if(taskID not in taskSchedulesSettings) or (taskSchedulesSettings[taskID]["interval"] != task.task_Interval.InSeconds()):
                taskSchedulesSettings[taskID] = {
                    "interval": task.task_Interval.InSeconds(),
                    "next": _datetime.min.isoformat()
                }
                self._flag_SaveSettings = True
            
            task._task_nextSchedule = _datetime.fromisoformat(taskSchedulesSettings[taskID]["next"])

        
        self.SaveSettingsIfNeeded()            
        return