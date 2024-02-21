import Tracker_util
import yaml
from selenium import webdriver
from datetime import datetime


with open("config.yaml", "r") as f:
    config_data = yaml.safe_load(f)

parent_dir = config_data["parent-dir"]
user_names = config_data["user_list"]
today = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M')

for user in user_names:

    new_user = Tracker_util.is_new_user(user)
    driver = webdriver.Chrome()
    driver.get(f'https://www.youtube.com/@{user}/playlists')
    details = driver.find_elements(by="id", value="details")

    for detail in details:
        line = detail.get_attribute("innerHTML").find("Updated")
        x = (detail.get_attribute("innerHTML")[152:252]).split("\" ")
        playlist_name = x[0]
        href = x[1].split(";pp")
        link = (href[0][6:]).replace('amp;', '').replace('amp', '')

        if new_user:
            with open(f"{parent_dir}\\{user}\\{playlist_name}_{today}", "w", encoding="utf-8") as file1:
                Tracker_util.write_playlist(link, user, file1)

        elif line != -1:
            with open(f"{parent_dir}\\{user}\\{playlist_name}_{today}_diff", "w", encoding="utf-8") as file2:
                Tracker_util.write_playlist(link, user, file2)
                file2.close()
            Tracker_util.manage_playlist(user, playlist_name)

        else:
            pass