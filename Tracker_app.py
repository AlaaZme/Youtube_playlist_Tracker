import concurrent.futures
import Tracker_util


def main():
    user_names = Tracker_util.get_config_users("user_list")
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_user = {executor.submit(Tracker_util.user_iteration, user): user for user in user_names}

if __name__ == "__main__":
    main()
