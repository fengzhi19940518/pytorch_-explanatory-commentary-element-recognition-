# @Author : bamtercelboo
# @Datetime : 2018/1/30 15:58
# @File : DataConll2003_Loader.py
# @Last Modify Time : 2018/1/30 15:58
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :
    FUNCTION :
"""
import re
import random
import torch
from Dataloader.Instance import Instance

from DataUtils.Common import *
import os
torch.manual_seed(seed_num)
random.seed(seed_num)


class DataLoaderHelp(object):
    """
    DataLoaderHelp
    """

    @staticmethod
    def _clean_str(string):
        """
        Tokenization/string cleaning for all datasets except for SST.
        Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
        """
        string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
        string = re.sub(r"\'s", " \'s", string)
        string = re.sub(r"\'ve", " \'ve", string)
        string = re.sub(r"n\'t", " n\'t", string)
        string = re.sub(r"\'re", " \'re", string)
        string = re.sub(r"\'d", " \'d", string)
        string = re.sub(r"\'ll", " \'ll", string)
        string = re.sub(r",", " , ", string)
        string = re.sub(r"!", " ! ", string)
        string = re.sub(r"\(", " \( ", string)
        string = re.sub(r"\)", " \) ", string)
        string = re.sub(r"\?", " \? ", string)
        string = re.sub(r"\s{2,}", " ", string)
        return string.strip().lower()

    @staticmethod
    def _normalize_word(word):
        """
        :param word:
        :return:
        """
        new_word = ""
        for char in word:
            if char.isdigit():
                new_word += '0'
            else:
                new_word += char
        return new_word

    @staticmethod
    def _sort(insts):
        """
        :param insts:
        :return: sorted insts by the size of inst.words_size
        """
        sorted_insts = []
        sorted_dict = {}
        for id_inst, inst in enumerate(insts):
            sorted_dict[id_inst] = inst.words_size
        dict = sorted(sorted_dict.items(), key=lambda d: d[1], reverse=True)
        for key, value in dict:
            sorted_insts.append(insts[key])
        print("Sort Finished.")
        return sorted_insts


class DataLoader(DataLoaderHelp):
    """
    DataLoader
    """
    def __init__(self, path, shuffle, config):
        """
        :param path: data path list
        :param shuffle:  shuffle bool
        :param config:  config
        """

        print("Loading Data......")
        self.data_list = []
        self.max_count = config.max_count
        self.path = path
        self.shuffle = shuffle
        # char feature
        self.pad_char = [char_pad, char_pad]
        # self.pad_char = []
        self.max_char_len = config.max_char_len

    def dataLoader(self):
        """
        :return:
        """
        path = self.path
        shuffle = self.shuffle
        assert isinstance(path, list), "Path Must Be In List"
        print("Data Path {}".format(path))
        for id_data in range(len(path)):
            print("Loading Data Form {}".format(path[id_data]))
            insts = self._Load_Each_Data(path=path[id_data], shuffle=shuffle)
            if shuffle is True and id_data == 0:
                print("shuffle train data......")
                random.shuffle(insts)
            # sorted(inst)
            if id_data == 0:
                insts = self._sort(insts)
            # sorted_insts = self.sort(insts)
            self.data_list.append(insts)
        # return train/dev/test data
        if len(self.data_list) == 3:
            return self.data_list[0], self.data_list[1], self.data_list[2]
        elif len(self.data_list) == 2:
            return self.data_list[0], self.data_list[1]

    def _Load_Each_Data(self, path=None, shuffle=False):
        """
        :param path:
        :param shuffle:
        :return:
        """
        assert path is not None, "The Data Path Is Not Allow Empty."
        insts = []
        with open(path, encoding="UTF-8") as f:
            inst = Instance()
            for line in f.readlines():
                line = line.strip()
                if line == "" and len(inst.words) != 0:
                    inst.words_size = len(inst.words)
                    insts.append(inst)
                    inst = Instance()
                else:
                    line = line.strip().split("\t")
                    word = line[0]
                    char = self._add_char_(word)
                    word = self._normalize_word(word)
                    inst.chars.append(char)
                    inst.words.append(word)
                    inst.labels.append(line[-1])
                if len(insts) == self.max_count:
                    break
            if len(inst.words) != 0:
                inst.words_size = len(inst.words)
                insts.append(inst)
            # print("\n")
        return insts

    """
    英文字母提取字符
    """
    # def _add_char(self, word):
    #     """
    #     :param word:
    #     :return:
    #     """
    #     char = []
    #     # char feature
    #     for i in range(len(word)):
    #         char.append(word[i])
    #     if len(char) > self.max_char_len:
    #         half = self.max_char_len // 2
    #         word_half = word[:half] + word[-(self.max_char_len - half):]
    #         char = word_half
    #     else:
    #         for i in range(self.max_char_len - len(char)):
    #             char.append(char_pad)
    #     return char

    """
    汉字提取偏旁部首
    """
    def strokes_dict(self, path):
        f = open(path, "r", encoding="utf-8")
        stroke_dict = {}
        for line in f.readlines():
            line = line.strip().split("\t")
            stroke_dict[line[0]] = line[-1]
        return stroke_dict


    def _add_char_(self, word):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        strokefile = os.path.join(cur_dir, 'all_sentences_strokes.txt')
        stroke_dict = self.strokes_dict(strokefile)
        char = []
        if word in stroke_dict:
            strokes = stroke_dict.get(word)
            for ch in strokes:
                char.append(ch)
            if len(strokes) > self.max_char_len:
                half = self.max_char_len // 2
                word_half = strokes[:half] + strokes[(self.max_char_len-half)]
                char = word_half
            else:
                for i in range(self.max_char_len - len(strokes)):
                    char.append(char_pad)
        return char

