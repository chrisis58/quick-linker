import os
import re
import numpy as np
import yaml

np.seterr(divide='ignore',invalid='ignore')

class Show:
    def __init__(self, src, dest, name=None, season=None, meta=None):
        if not os.path.isdir(src) or not os.path.isdir(dest):
            raise RuntimeError("path is not invalid!")

        self.src = src
        self.dest = dest
        self.meta = meta

        tmp = os.path.split(self.src)
        self.season = tmp[1]
        self.season = int(re.search(r"\d+", self.season).group(0))
        tmp = os.path.split(tmp[0])
        self.name = tmp[1]

        if name is not None:
            self.name = name
        if season is not None:
            self.season = season
        self.season = "{:0>2d}".format(self.season)

        self.episode_list = os.listdir(self.src)
        self.episode_list_extracted = [re.compile("\d+").findall(epi) for epi in self.episode_list]
        self.episode_list_extracted = np.mat(self.episode_list_extracted, dtype=int)

        diff = np.r_[self.episode_list_extracted[1:, :], np.zeros((1, self.episode_list_extracted.shape[1]), dtype=int)]
        diff = self.episode_list_extracted - diff
        diff = (diff / diff).astype(int)
        diff[diff == -2147483648] = 0
        confidence = np.sum(diff, axis=0).reshape((1, diff.shape[1]))
        episode_index = np.argmax(confidence)
        self.episode_list_extracted = self.episode_list_extracted[:, episode_index].reshape(-1).tolist()[0]
        self.episode_list_extracted = ["{:0>2d}".format(i) for i in self.episode_list_extracted]

    def do_hard_link(self, name_reconstruct=False):
        if not name_reconstruct:
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
                                         extension=os.path.splitext(self.episode_list[i])[1])
                else:
                    new_file_name = "{name} - S{season}E{episode} - {meta}{extension}"
                    new_file_name = new_file_name.format(name=self.name,
                                         season=self.season,
                                         episode=self.episode_list_extracted[i],
                                         meta=self.meta,
                                         extension=os.path.splitext(self.episode_list[i])[1])
                if not os.path.exists(os.path.join(self.dest, new_file_name)):
                    print("make hard link: {src} \n              ==> {dest}".format(src=os.path.join(self.src, self.episode_list[i]),
                          dest=os.path.join(self.dest, new_file_name)))
                    os.link(os.path.join(self.src, self.episode_list[i]), os.path.join(self.dest, new_file_name))


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

    for task_name in data['tasks']:
        task_info = data['tasks'][task_name]
        print("task {task_name} start".format(task_name=task_name))

        if task_info.get("rename") is not None and task_info.get("rename").get("enable", False):
            show = Show(task_info['src'],
                        task_info['dest'],
                        name=task_info.get("rename").get("name", None),
                        season=task_info.get("rename").get("season", None),
                        meta=task_info.get("rename").get("meta", None))
        else:
            show = Show(task_info['src'], task_info['dest'])

        show.do_hard_link(name_reconstruct=task_info.get("rename") is not None and task_info.get("rename").get("enable", False))
        print("task end")

