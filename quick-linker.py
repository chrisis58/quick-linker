import os
import re
import threading
import time
import numpy as np
import yaml

np.seterr(divide='ignore',invalid='ignore')

class Show:
    def __init__(self, name, info):
        self.task_name = name
        if not os.path.isdir(info.get('src')) or not os.path.isdir(info.get('dest')):
            raise RuntimeError("path is not invalid!")

        self.enable = info.get("enable", True)

        self.src = info.get('src')
        self.dest = info.get('dest')

        tmp = os.path.split(self.src)
        self.season = tmp[1]
        self.season = int(re.search(r"\d+", self.season).group(0))
        tmp = os.path.split(tmp[0])
        self.name = tmp[1]

        rename = info.get("rename")
        if rename is not None:
            self.do_rename = rename.get("enable", False)
            self.meta = rename.get("meta")
            if rename.get("name") is not None:
                self.name = rename.get("name")
            if rename.get("season") is not None:
                self.season = rename.get("season")

        self.season = "{:0>2d}".format(self.season)

        self.episode_list = os.listdir(self.src)
        if info.get('exclude') is not None:
            for item in info.get('exclude'):
                self.episode_list = list(filter(lambda x: item not in x, self.episode_list))
        if info.get('mute') is not None:
            for item in info.get('mute'):
                episode_list = [t.replace(item, "") for t in self.episode_list]
        else:
            episode_list = self.episode_list

        self.episode_list_extracted = [re.compile("\d+\.?\d*").findall(epi) for epi in episode_list]

        confidence = {}
        for item in [len(item) for item in self.episode_list_extracted]:
            if confidence.get(item) is None:
                confidence[item] = 1
            else:
                confidence[item] = confidence[item] + 1
        max_count = -1
        num_length = -1
        for length,count in confidence.items():
            if max_count < count:
                max_count = count
                num_length = length

        for i in range(len(self.episode_list_extracted)):
            if len(self.episode_list_extracted[i]) != num_length:
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
        if not self.do_rename:
            for epi in self.episode_list:
                if not os.path.exists(os.path.join(self.dest, epi)):
                    print("make hard link: {src} \n              ==> {dest}".format(src=os.path.join(self.src, epi), dest=os.path.join(self.dest, epi)))
                    os.link(os.path.join(self.src, epi), os.path.join(self.dest, epi))
        else:
            for i in range(len(self.episode_list)):
                if self.meta is None:
                    new_file_name = "{name} - S{season}E{episode}{extension}"
                    new_file_name = new_file_name.format(name=self.name,
                                         season=self.season,
                                         episode=self.episode_list_extracted[i],
                                         extension=Show.get_whole_ext(self.episode_list[i]))
                else:
                    new_file_name = "{name} - S{season}E{episode} - {meta}{extension}"
                    new_file_name = new_file_name.format(name=self.name,
                                         season=self.season,
                                         episode=self.episode_list_extracted[i],
                                         meta=self.meta,
                                         extension=Show.get_whole_ext(self.episode_list[i]))
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
        with open("config.yml", encoding='utf-8') as yml:
            data = yaml.load(yml, Loader=yaml.FullLoader)
    except FileNotFoundError:
        try:
            with open("config.yaml", encoding='utf-8') as yml:
                data = yaml.load(yml, Loader=yaml.FullLoader)
        except FileNotFoundError:
            print("config file cannot be find!")

    config = data.get("config")

    if config is not None and config.get("watchdog") is not None and config.get("watchdog", False):
        thread_list = []
        for task_name in data['tasks']:
            task_info = data['tasks'][task_name]

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

            show = Show(task_name, task_info)
            show.do_hard_link()
