from threading import Thread
import inspect
import ctypes


class KillableThread(Thread):
    """
    Like Py threads but better
    You can kill them :)
    """
    
    def __tid(self):
        if self.is_alive():
            return ctypes.c_long(self.ident)

        return None

    def bury(self) -> str:
        """
        Magic here.
        This injects an exception in this thread.

        Return thread status -> str (burried | not alive)

        Raise ValueError if tid is incorrect
        Raise SystemError if thread is more powerful than kill -9 :)
        """
        tid = self.__tid()
        if tid is not None:
            exctype = SystemExit
            
            if not inspect.isclass(exctype):
                exctype = type(exctype)  

            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))

            if res == 1:
                return f'Thread {self.name} burried'
            elif res == 0:
                raise ValueError("invalid thread id")
            elif res != 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                raise SystemError("PyThreadState_SetAsyncExc failed")

        else:
            return f'Thread {self.name} is not alive'
            