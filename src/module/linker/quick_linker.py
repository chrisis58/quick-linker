import os.path
from os import link, listdir, path

import numpy as np
import re

from src.module.bean import QuickLinkerConfig
from src.module.linker import Linker

class QuickLinker(Linker):

    def __init__(self, config: QuickLinkerConfig):
        self._config = config


    def ln(self, src: str, dest: str) -> None:
        file_list = listdir(src)
        ln_dict = self.extract(file_list)

        for file in file_list:
            target = path.join(dest, ln_dict.get(file, file))
            if not os.path.exists(target):
                link(path.join(src, file), target)


    def extract(self, file_list: list[str]) -> dict[str, str]:
        """
        根据传入的文件名列表进行解析，抽取其中对应的剧集集数。

        :param file_list: 待解析的文件名列表
        :return: 字符串字典，用于映射解析前后的文件名
        """
        np.seterr(divide='ignore', invalid='ignore')

        for item in self._config.exclude:
            file_list = list(filter(lambda x: item not in x, file_list))
        if len(file_list) == 0 or not self._config.enable:
            return dict()

        tmp_list = file_list.copy()

        for item in self._config.mute:
            tmp_list = [t.replace(item, "") for t in file_list]

        tmp_list = [re.compile("\d+\.?\d*").findall(item) for item in tmp_list] # 抽取所有数字
        length = np.argmax(np.bincount([len(item) for item in tmp_list]))       # 找到合适的包含数字的个数

        for i in range(len(tmp_list)).__reversed__():
            if len(tmp_list[i]) != length:
                file_list.remove(file_list[i])
                tmp_list.remove(tmp_list[i])

        tmp_list = np.asarray(tmp_list, dtype=float)

        diff = np.r_[tmp_list[1:, :], np.zeros((1, tmp_list.shape[1]), dtype=float)]
        diff = tmp_list - diff
        diff = (diff / diff).astype(int)
        diff[diff == -2147483648] = 0
        confidence = np.sum(diff, axis=0).reshape((1, diff.shape[1]))
        episode_index = np.argmax(confidence) # 获取数字矩阵中代表`剧集集数`的数字的下标
        episode_list = tmp_list[:, episode_index].reshape(-1).tolist()

        ln_dict = dict()
        for index, episode in enumerate(episode_list):
            ln_dict[file_list[index]] = self.get_full_name(int(episode)) + get_whole_ext(file_list[index])

        return ln_dict

    def get_full_name(self, episode: int) -> str:
        return self._config.format.format(
            name = self._config.name,
            season = self._config.season,
            episode = episode,
            meta = self._config.meta
        )