import Tracker_util
import threading

user_names = Tracker_util.get_config_users("user_list")
threads = []

for user_name in user_names:
    t = threading.Thread(target=Tracker_util.user_iteration, args=(user_name,))
    t.start()
    threads.append(t)

for thread in threads:
    thread.join()
    if not thread.is_alive():
        print(thread.is_alive())
