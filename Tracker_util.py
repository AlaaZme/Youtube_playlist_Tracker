import concurrent.futures
import os
from selenium import webdriver
from time import sleep
from datetime import datetime
import mail_gmail
import yaml


def get_config_users(data):
    with open("config.yaml", "r") as f:
        config_data = yaml.safe_load(f)
    return config_data[data]


parent_dir = get_config_users('parent-dir')

today = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M')


def user_iteration(user):
    driver = webdriver.Chrome()
    driver.get(f'https://www.youtube.com/@{user}/playlists')
    details = driver.find_elements(by="id", value="details")

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        var = {executor.submit(parse_details, detail, user): detail for detail in details}


def parse_details(detail, user):
    new_user = is_new_user(user)
    line = detail.get_attribute("innerHTML").find("Updated")
    x = (detail.get_attribute("innerHTML")[152:252]).split("\" ")
    playlist_name = x[0]
    href = x[1].split(";pp")
    link = (href[0][6:]).replace('amp;', '').replace('amp', '')

    if new_user:
        with open(f"{parent_dir}\\{user}\\{playlist_name}_{today}", "w", encoding="utf-8") as file1:
            write_playlist(link, file1)

    elif line != -1:
        with open(f"{parent_dir}\\{user}\\{playlist_name}_{today}_diff", "w", encoding="utf-8") as file2:
            write_playlist(link, file2)
            file2.close()
        manage_playlist(user, playlist_name)


def write_playlist(link, file):
    driver2 = webdriver.Chrome()
    driver2.get(f'https://www.youtube.com/{link}')
    sleep(5)
    items = driver2.find_elements(by="id", value="playlist-items")
    playlist = driver2.find_elements(by="xpath", value="//*[@id=\"video-title\"]")
    i = 1
    for track in playlist:
        if track.get_attribute("title") and i <= len(items):
            file.write(f"{track.get_attribute('title')}\n")
            i += 1
    sleep(1)


def is_new_user(user_name):
    path = os.path.join(parent_dir, user_name)
    if os.path.isdir(path):
        return 0
    else:
        os.mkdir(path)
        return 1


def manage_playlist(user_name, playlist_prefix):
    path = os.path.join(parent_dir, user_name)
    list_dates = []
    files = [filename for filename in os.listdir(path) if filename.startswith(playlist_prefix)]

    if len(files) < 2:
        print(f"found: {user_name} new Playlist")
        if files:
            playlist_path = os.path.join(path, files[0])
            os.rename(playlist_path, playlist_path.replace("_diff", ""))
        mail_gmail.send_gmail(user_name, playlist_prefix)
        return

    for file in files:
        temp = file.replace("_diff", "").split("_")
        temp_dict = {"play": temp[0], "time": temp[1]}
        dict_dates = temp_dict
        list_dates.append(dict_dates)

    new_list = sorted(list_dates, key=lambda dict_dates: dict_dates['time'], reverse=True)

    file_list = []
    for i in range(len(new_list)):
        file_list.append(
            [filename for filename in os.listdir(path) if
             filename.startswith(f"{new_list[i]['play']}_{new_list[i]['time']}")])
        if i > 1:
            my_str = ' '.join((map(str, file_list[i])))
            new_path = os.path.join(path, my_str)
            if "diff" in new_path:
                os.remove(new_path)

        i += 1

    list1 = file_list[0]
    list2 = file_list[1]
    compare_lists(user_name, playlist_prefix, list1, list2)


def write_diff_in_list(user_name, playlist_prefix, list1, list2):
    today_date = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M')
    res = []
    f1 = open(
        f"{parent_dir}\\{user_name}\\_changeLog_{playlist_prefix}"
        f"", "a", encoding="utf-8")
    if len(list1) >= len(list2):
        for song in list1:
            if song not in list2:
                res.append(song)
                line_to_file = f"added  {today_date} {song} "
                if res:
                    f1.writelines(line_to_file)
    if len(list1) <= len(list2):
        for song in list2:
            if song not in list1:
                res.append(song)
                line_to_file = f" deleted {today} {song} "
                if res:
                    f1.writelines(line_to_file)
    f1.close()
    if res:
        print(f"found for : {user_name}")
        mail_gmail.send_gmail(user_name, playlist_prefix)


def compare_lists(user_name, playlist_prefix, file1, file2):
    list1 = []
    list2 = []
    with open(f"{parent_dir}\\{user_name}\\{file1[0]}", "r", encoding="utf-8") as f:
        for line in f.readlines():
            list1.append(line)

        with open(f"{parent_dir}\\{user_name}\\{file2[0]}", "r", encoding="utf-8") as f2:
            for line in f2.readlines():
                list2.append(line)

    write_diff_in_list(user_name, playlist_prefix, list1, list2)
