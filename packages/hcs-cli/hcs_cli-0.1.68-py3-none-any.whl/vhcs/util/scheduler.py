import threading
import time
import heapq
from concurrent.futures import ThreadPoolExecutor


class ThreadPoolScheduler:
    def __init__(self, max_threads=5):
        self._task_queue = []
        self._lock = threading.Lock()
        self._scheduler_event = threading.Event()
        self._scheduler_thread = threading.Thread(target=self._scheduler_loop, name="thread-pool-sch", daemon=True)
        self._executor = ThreadPoolExecutor(max_workers=max_threads, thread_name_prefix="thread-pool-exec")
        self._scheduler_thread.start()
        self._counter = 0

    def _scheduler_loop(self):
        while True:
            if self._task_queue:
                execute_at, _, task = self._task_queue[0]
                current_time = time.time()

                if execute_at > current_time:
                    # Head is still in future. Sleep
                    timeout = execute_at - current_time
                    self._scheduler_event.wait(timeout)
                    continue

                # Ready to execute the head
                heapq.heappop(self._task_queue)
                self._executor.submit(task)
            else:
                # queue is empty.
                self._scheduler_event.wait()
                self._scheduler_event.clear()

    def submit(self, target_function, delay_seconds):
        with self._lock:
            execute_at = time.time() + delay_seconds
            # tuple subitems are compared after comparing the first one.
            # So make sure there's a differentiator with counter.
            self._counter += 1
            heapq.heappush(self._task_queue, (execute_at, self._counter, target_function))
            self._scheduler_event.set()

    def close(self):
        self.running = False
        self._scheduler_event.set()
        self._executor.shutdown(wait=False)
        self._scheduler_thread.join()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


# # Example usage
# def print_message(message):
#     print(message)
#     time.sleep(5)
#     print("done")

# scheduler = ThreadPoolScheduler(max_threads=5)
# _n = 0

# def rr(txt):
#     global _n
#     print("rr", txt, _n)
#     _n += 1
#     scheduler.submit(lambda: rr("a1"), 0)
# scheduler.submit(lambda: rr("a1"), 0)
# time.sleep(5)  # Give some time for tasks to execute
