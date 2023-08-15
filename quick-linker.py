import os
import re
import threading
import time
import numpy as np
import yaml



class Show:
    def __init__(self, name, info):
        self.task_name = name
        if not os.path.isdir(info.get('src')) or not os.path.isdir(info.get('dest')):
            raise RuntimeError("path is invalid!")

        self.enable = info.get("enable", True)

        self.src = info.get('src')
        self.dest = info.get('dest')
        self.exclude = info.get('exclude')
        self.mute = info.get("mute")

        tmp = os.path.split(self.src)
        season = tmp[1]
        season = int(re.search(r"\d+", season).group(0))
        tmp = os.path.split(tmp[0])
        name = tmp[1]

        self.rename = info.get("rename", {})
        self.rename.setdefault("season", season)
        self.rename['season'] = "{:0>2d}".format(self.rename['season'])
        self.rename.setdefault("name", name)

        self.episode_list = []
        self.episode_list_extracted = []

    def extract(self):
        np.seterr(divide='ignore', invalid='ignore')

        self.episode_list = os.listdir(self.src)
        if len(self.episode_list) == 0 or not self.rename.get("enable", False):
            return

        if self.exclude is not None:
            for item in self.exclude:
                self.episode_list = list(filter(lambda x: item not in x, self.episode_list))
        episode_list = self.episode_list
        if self.mute is not None:
            for item in self.mute:
                episode_list = [t.replace(item, "") for t in episode_list]

        self.episode_list_extracted = [re.compile("\d+\.?\d*").findall(epi) for epi in episode_list]

        length = np.argmax(np.bincount([len(item) for item in self.episode_list_extracted]))

        for i in range(len(self.episode_list_extracted)).__reversed__():
            if len(self.episode_list_extracted[i]) != length:
                self.episode_list_extracted.remove(self.episode_list_extracted[i])
                self.episode_list.remove(self.episode_list[i])
        self.episode_list_extracted = np.asarray(self.episode_list_extracted, dtype=float)

        diff = np.r_[self.episode_list_extracted[1:, :], np.zeros((1, self.episode_list_extracted.shape[1]), dtype=float)]
        diff = self.episode_list_extracted - diff
        diff = (diff / diff).astype(int)
        diff[diff == -2147483648] = 0
        confidence = np.sum(diff, axis=0).reshape((1, diff.shape[1]))
        episode_index = np.argmax(confidence)
        self.episode_list_extracted = self.episode_list_extracted[:, episode_index].reshape(-1).tolist()
        self.episode_list_extracted = ["{:0>2g}".format(i) for i in self.episode_list_extracted]

    def do_hard_link(self):
        if not self.enable:
            return
        print("task {task_name} start".format(task_name=self.task_name))
        self.extract()
        if not self.rename.get("enable", False):
            for epi in self.episode_list:
                if not os.path.exists(os.path.join(self.dest, epi)):
                    print("make hard link: {src} \n              ==> {dest}".format(src=os.path.join(self.src, epi), dest=os.path.join(self.dest, epi)))
                    os.link(os.path.join(self.src, epi), os.path.join(self.dest, epi))
        else:
            for i in range(len(self.episode_list)):
                info_dict = self.rename.copy()
                info_dict['episode'] = self.episode_list_extracted[i]
                info_dict['extension'] = Show.get_whole_ext(self.episode_list[i])
                new_file_name = (self.rename.get("format") + "{extension}").format(**info_dict)

                if not os.path.exists(os.path.join(self.dest, new_file_name)):
                    print("make hard link: {src} \n              ==> {dest}".format(src=os.path.join(self.src, self.episode_list[i]),
                          dest=os.path.join(self.dest, new_file_name)))
                    os.link(os.path.join(self.src, self.episode_list[i]), os.path.join(self.dest, new_file_name))
        print("task end")

    def start_watchdog(self):
        if not self.enable:
            return
        print("watchdog for {} start".format(self.task_name))
        self.create_watchdog().start()

    def create_watchdog(self):
        from watchdog.observers import Observer
        observer = Observer()
        observer.schedule(self.create_custom_handler(), path=self.src, recursive=False)
        return observer

    def create_custom_handler(self):
        from watchdog.events import FileSystemEventHandler
        class custom_handler(FileSystemEventHandler):
            def __init__(self, show_obj):
                self.show = show_obj

            def on_created(self, event):
                self.show.do_hard_link()
        return custom_handler(self)

    @staticmethod
    def get_whole_ext(file):
        info = os.path.splitext(file)
        if info[1] in [".ass", '.srt', '.ssa', '.sub']:
            ext = ""
            while len(info[1]) > 0:
                file = info[0]
                ext = info[1] + ext
                info = os.path.splitext(file)
            return ext
        else:
            return info[1]


if __name__ == "__main__":
    try:
        with open("config.yml", encoding='utf-8', mode='r') as yml:
            data = yaml.load(yml, Loader=yaml.FullLoader)
    except FileNotFoundError:
        try:
            with open("config.yaml", encoding='utf-8', mode='r') as yml:
                data = yaml.load(yml, Loader=yaml.FullLoader)
        except FileNotFoundError:
            print("config file cannot be find!")
            exit()

    config = data.get("config", {})
    config_global = config.get("global", {})

    if config.get("watchdog") is not None and config.get("watchdog").get("enable", False):
        if config.get("watchdog").get("one-instance", True):
            try:
                with open("pid", mode='r') as pid_file:
                    pid_str = pid_file.readline()
                    os.kill(int(pid_str), 9)
            except (FileNotFoundError, PermissionError):
                pass
            with open("pid", mode='a') as pid_file:
                pid_file.seek(0)
                pid_file.truncate()
                pid_file.write(os.getpid().__str__())

        thread_list = []
        for task_name in data['tasks']:
            task_info = data['tasks'][task_name]

            task_info.setdefault("mute", config_global.get("mute"))
            task_info.setdefault("exclude", config_global.get("exclude"))
            rename = task_info.get("rename", {})
            if rename.get("enable", False):
                rename.setdefault("format", config_global.get("format", "{name} - S{season}E{episode}"))

            show = Show(task_name, task_info)

            thread = threading.Thread(target=lambda x: x.start_watchdog(), args=(show, ))
            thread.daemon = True
            thread_list.append(thread)
            thread.start()
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            for thread in thread_list:
                thread.join()
    else:
        for task_name in data['tasks']:
            task_info = data['tasks'][task_name]

            task_info.setdefault("mute", config_global.get("mute"))
            task_info.setdefault("exclude", config_global.get("exclude"))

            show = Show(task_name, task_info)
            show.do_hard_link()
