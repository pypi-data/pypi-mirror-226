from dataclasses import dataclass
import numpy as np
import struct
import gzip, pickle
from utils.pose_util import Coordinate
from utils.const import *
from utils.common_component import load_pickle_path
from enum import Enum
import pandas as pd
from zipfile import ZipFile
import sys

def get_bin_version(class_name):
    return getattr(sys.modules[__name__], class_name)

def get_pickle_version(class_name):
    return getattr(sys.modules[__name__], class_name)

def read_zip_file(zip_file):
    with ZipFile(zip_file, 'r') as zip:
        file_name = zip.filelist[0].filename
        data = zip.read(file_name)
    unpack_data = []
    for cell in range(0, int(len(data)), 4):
        unpack_data.append(struct.unpack('i', data[cell : cell+4])[0])
    return unpack_data

def read_bin_file(bin_file):
    unpack_data = []
    with open(bin_file, "rb") as f:
        data = f.read()
    for cell in range(0, int(len(data)), 4):
        unpack_data.append(struct.unpack('i', data[cell : cell+4])[0])
    return unpack_data

def pop_header(data):
    casting_data = []
    header = data.pop(0)
    version = get_bin_version(f"BinVersion{header}")
    line = version.row_len
    for line_cnt in range(0, len(data), line):
        casting_data.append(data[line_cnt : line_cnt + line])
    return casting_data, header

def bin_to_dataframe(bin_data):
    df = pd.DataFrame(bin_data)
    return df

def process_zip(file):
    bin_data = read_zip_file(file)
    data, header = pop_header(bin_data)
    df = bin_to_dataframe(data)
    return df, header

def process_bin(file):
    bin_data = read_bin_file(file)
    data, header = pop_header(bin_data)
    df = bin_to_dataframe(data)
    return df, header

def process_csv(file):
    df = pd.read_csv(file)
    return df

def get_header_data(file):
    if FileType.BIN.value in file:
        data, header = process_bin(file)
    elif FileType.ZIP.value in file:
        data, header = process_zip(file)
    elif FileType.CSV.value in file:
        header = 0
        data = process_csv(file)
    else:
        print('not defind file type')
        data = pd.DataFrame
        header = 0
    return header, data

class FileType(Enum):
    PICKLE = '.pickle'
    ZIP = '.zip'
    BIN = '.bin'
    CSV = '.csv'

class PickleType(Enum):
    ORIGIN = 0
    MLP = 1
    LSTM = 2
    VT = 3
    ORIGINPC = 999


class VersionCaster:
    def __init__(self, file):
        if FileType.PICKLE.value in file:
            data = load_pickle_path(file)
            header = data["header"]
            self.pickle_version = get_pickle_version(f"PickleVersion{header}")
            self.use_data = self.pickle_version.get_data(frame_data)
        else:
            data, header = process_bin(file)
            header, frame_data = get_header_data(file)
            self.bin_version = get_bin_version(f"BinVersion{header}")
            self.use_data = self.bin_version.get_data(frame_data)
    
    def make_pickle(self, path, pickle_type):
        pickle_data = self.use_data.copy()
        pickle_data['pickle_header'] = pickle_type
        with gzip.open(f"{path}.pickle", "wb") as f:
            pickle.dump(pickle_data, f)
    
    # labeling data 추가해서 저장 Pickle Type에 따라서 
    

class PickleVersion:
    def __init__(self):
        self.key = []

    def get_data(self, path):
        with gzip.open(path) as f:
            pickle_data = pickle.load(f)
        return pickle_data


class BinVersion:
    def __init__(self):
        self.header = 1010
        self.row_len = 42
        self.status_kind = ["UP", "DOWN"]
        self.info_index = {"time": 0, "status": 1, "pose": (2, 41), "reps": 42}
        self.body_list = [NOSE, LEFT_SHOULDER, RIGHT_SHOULDER, 
                LEFT_ELBOW, RIGHT_ELBOW, LEFT_WRIST, RIGHT_WRIST, 
                LEFT_HIP, RIGHT_HIP, LEFT_KNEE, RIGHT_KNEE, LEFT_ANKLE, RIGHT_ANKLE]
        
    def make_pickle(self, path, frame_data):
        data = self.get_data(frame_data)
        with gzip.open(path, "wb") as f:
            pickle.dump(data, f)

    def get_data(self, frame_data):
        frame_data = np.reshape(frame_data, (-1, self.row_len))
        info_index = self.info_index
        info_data = {i: [] for i in info_index.keys()}
        for frame in frame_data:
            for key in info_index.keys():
                if key == "pose":
                    zip_pose = frame[info_index[key][0]: info_index[key][1]]
                    zip_idx = 0
                    pose = []
                    for idx in range(33):
                        if idx in self.body_list:
                            pose.append(Coordinate(zip_pose[zip_idx * 3], zip_pose[zip_idx * 3 + 1], zip_pose[zip_idx * 3 + 2]))
                            zip_idx += 1
                        else:
                            pose.append(Coordinate(0, 0, 0))
                    info_data[key].append(pose)
                elif key == "status":
                    info_data[key].append(self.status_kind[frame[info_index[key]]])
                else:
                    info_data[key].append(frame[info_index[key]])
        info_data['header'] = self.header
        return info_data
    

class BinVersion1010(BinVersion):
    def __init__(self):
        super().__init__()

    def get_data(self, frame_data):
        return super().get_data(frame_data)

class BinVersion1110(BinVersion):
    def __init__(self):
        super().__init__()
        self.header = 1010
    def get_data(self, frame_data):
        return super().get_data(frame_data)

class BinVersion1110(BinVersion):
    def __init__(self):
        super().__init__()
        self.header = 1110
    def get_data(self, frame_data):
        return super().get_data(frame_data)

class BinVersion2113(BinVersion):
    def __init__(self):
        super().__init__()
        self.header = 2113
        self.info_index = {"time": 0, "status": 1, "reps": 2, "pose": (3, 69)}
        self.row_len = 69
        self.status_kind = ["UP", "MIDDLE", "DOWN", "RESTING"]
        body_list = [
            LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_ELBOW, RIGHT_ELBOW, LEFT_WRIST, RIGHT_WRIST, 
            LEFT_PINKY, RIGHT_PINKY, LEFT_INDEX, RIGHT_INDEX, LEFT_THUMB, RIGHT_THUMB, 
            LEFT_HIP, RIGHT_HIP, LEFT_KNEE, RIGHT_KNEE, LEFT_ANKLE, RIGHT_ANKLE,
            LEFT_HEEL, RIGHT_HEEL, LEFT_FOOT_INDEX, RIGHT_FOOT_INDEX,]
        self.landmark_range = len(body_list) * 3
    def get_data(self, frame_data):
        return super().get_data(frame_data)
