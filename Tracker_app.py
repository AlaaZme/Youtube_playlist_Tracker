import concurrent.futures


import Tracker_util


user_names = Tracker_util.get_config_users("user_list")
threads = []

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    future_to_url = {executor.submit(Tracker_util.user_iteration,user): user for user in user_names}
'''
for user_name in user_names:
    t = threading.Thread(target=Tracker_util.user_iteration, args=(user_name,))
    t.start()
    threads.append(t)

for thread in threads:
    thread.join()
    if thread.is_alive():
        print(thread.is_alive())
'''