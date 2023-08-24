import json, os
from copy import deepcopy
import numpy as np
import pandas as pd
from tqdm import tqdm

from mmengine.registry import DATASETS
from typing import List, Union, Callable, Optional, Sequence

from shapely.geometry import box, Polygon, MultiPolygon

from mmengine.dataset import BaseDataset, Compose
from multiprocessing import Pool


@DATASETS.register_module()
class EngineMask(BaseDataset):
    def __init__(self,
                 data_path: str,
                 raster_dir_path: str,
                 vector_dir_path: str,
                 split: str = "train",
                 class_title: str = None,
                 slice: bool = False,
                 window: tuple = None,
                 stride: tuple = None,
                 pipeline: List[Union[dict, Callable]] = [],
                 max_refetch: int = 1000,
                 ignore_index: int = 255,
                 reduce_zero_label: bool = False,
                 serialize_data: bool = True,
                 lazy_init: bool = False,
                 indices: Optional[Union[int, Sequence[int]]] = None,
                 test_mode: bool = False):
        self.raster_data_path = f"{data_path}/{raster_dir_path}"
        self.vector_data_path = f"{data_path}/{vector_dir_path}"

        self.split = split
        self.slice = slice 
        self.window = window 
        self.stride = stride
        self.class_title = class_title
        self.ignore_index = ignore_index
        self.reduce_zero_label = reduce_zero_label
        self.serialize_data = serialize_data
        self._indices = indices
        self.test_mode = test_mode

        self.pipeline = Compose(pipeline)
        self.max_refetch = max_refetch

        if not lazy_init:
            self.full_init()

    def _slice_image_info(self, vec_map, img_map):
        data_infos = []
        img_height = vec_map["images"][0]["height"]
        img_width = vec_map["images"][0]["width"]
        for slice_y in range(0, img_height, self.stride[0]):
            if (slice_y + self.window[0]) < img_height:
                for slice_x in range(0, img_width, self.stride[1]):
                    if (slice_x + self.window[1]) < img_width:
                        new_info = deepcopy(img_map)
                        new_info["slice_x"] = slice_x
                        new_info["slice_y"] = slice_y
                        new_info["slice_w"] = self.window[1]
                        new_info["slice_h"] = self.window[0]
                        data_infos.append(new_info)
                    elif slice_x < img_width and self.window[1] < img_width:
                        new_info = deepcopy(img_map)
                        new_info["slice_y"] = slice_y
                        slice_x = img_width - self.window[1] - 1
                        new_info["slice_x"] = slice_x
                        new_info["slice_w"] = self.window[1]
                        new_info["slice_h"] = self.window[0]
                        data_infos.append(new_info)
                    elif self.window[1] >= img_width:
                        new_info = deepcopy(img_map)
                        new_info["slice_y"] = slice_y
                        slice_x = 0
                        new_info["slice_x"] = slice_x
                        new_info["slice_w"] = img_width
                        new_info["slice_h"] = self.window[0]
                        data_infos.append(new_info)

            elif slice_y < img_height and self.window[0] < img_height:
                slice_y = img_height - self.window[0] - 1
                for slice_x in range(0, img_width, self.stride[1]):
                    if (slice_x + self.window[1]) < img_width:
                        new_info = deepcopy(img_map)
                        new_info["slice_x"] = slice_x
                        new_info["slice_y"] = slice_y
                        new_info["slice_w"] = self.window[1]
                        new_info["slice_h"] = self.window[0]
                        data_infos.append(new_info)
                    elif slice_x < img_width and self.window[1] < img_width:
                        new_info = deepcopy(img_map)
                        new_info["slice_y"] = slice_y
                        slice_x = img_width - self.window[1] - 1
                        new_info["slice_x"] = slice_x
                        new_info["slice_w"] = self.window[1]
                        new_info["slice_h"] = self.window[0]
                        data_infos.append(new_info)
                    elif self.window[1] >= img_width:
                        new_info = deepcopy(img_map)
                        new_info["slice_y"] = slice_y
                        slice_x = 0
                        new_info["slice_x"] = slice_x
                        new_info["slice_w"] = img_width
                        new_info["slice_h"] = self.window[0]
                        data_infos.append(new_info)

            elif self.window[0] >= img_height:
                slice_y = 0
                for slice_x in range(0, img_width, self.stride[1]):
                    if (slice_x + self.window[1]) < img_width:
                        new_info = deepcopy(img_map)
                        new_info["slice_x"] = slice_x
                        new_info["slice_y"] = slice_y
                        new_info["slice_w"] = self.window[1]
                        new_info["slice_h"] = img_height
                        data_infos.append(new_info)
                    elif slice_x < img_width and self.window[1] < img_width:
                        new_info = deepcopy(img_map)
                        new_info["slice_y"] = slice_y
                        slice_x = img_width - self.window[1] - 1
                        new_info["slice_x"] = slice_x
                        new_info["slice_w"] = self.window[1]
                        new_info["slice_h"] = img_height
                        data_infos.append(new_info)
                    elif self.window[1] >= img_width:
                        new_info = deepcopy(img_map)
                        new_info["slice_y"] = slice_y
                        slice_x = 0
                        new_info["slice_x"] = slice_x
                        new_info["slice_w"] = img_width
                        new_info["slice_h"] = img_height
                        data_infos.append(new_info)

        return data_infos

    def _load_vector_file(self, vec_path):
        vec_map = json.load(open(vec_path))

        file_name = vec_map["images"][0]["file_name"].split("/")[-1]
        file_path = os.path.join(self.raster_data_path, file_name)

        img_map = {
            "img_path": file_path,
            "img_id": vec_map["info"]["id"],
            "height": vec_map["images"][0]["height"],
            "width": vec_map["images"][0]["width"],
            "reduce_zero_label": self.reduce_zero_label,
            "seg_fields": [],
            "mask": vec_map["properties"][self.class_title_idx]['labels'][0]
        }

        if self.slice:
            return self._slice_image_info(vec_map, img_map)
        else:
            img_map["slice_x"] = 0
            img_map["slice_y"] = 0
            img_map["slice_w"] = img_map["width"]
            img_map["slice_h"] = img_map["height"]


        return img_map

    def load_data_list(self):
        meta_path = os.path.join(self.vector_data_path, "metadata.json")
        metadata = json.load(open(meta_path, "r"))

        if not self.class_title:
            self.CLASSES = metadata["label:metadata"][0]["options"]
            self.class_title = metadata["label:metadata"][0]["title"].replace(" ", "-").lower()
            self.class_title_idx = 0
        else:
            for idx, question in enumerate(metadata["label:metadata"]):
                if question["title"] == self.class_title:
                    self.CLASSES = question["options"]
                    self.class_title = self.class_title.replace(" ", "-").lower()
                    self.class_title_idx = idx 

        self._metainfo = {
            "title": metadata["title"],
            "description": metadata["description"],
            "tags": metadata["tags"],
            "problemType": metadata["problemType"] if "problemType" in metadata else None,
            "question_title": metadata["label:metadata"][self.class_title_idx]["title"],
            "question_description": metadata["label:metadata"][self.class_title_idx]["description"],
            "classes": metadata["label:metadata"][self.class_title_idx]["options"],
            "reduce_zero_label": self.reduce_zero_label
        }

        vec_path_list = [os.path.join(self.vector_data_path, vec_file) for vec_file in metadata["dataset"][self.split]]

        pool = Pool(16)
        data_list = list(tqdm(pool.imap(self._load_vector_file, vec_path_list), total=len(vec_path_list)))
        if self.slice:
            data_list = [item for sublist in data_list for item in sublist]
        pool.close()

        heights = []
        widths = []

        for img in data_list:
            heights.append(img['slice_h'])
            widths.append(img['slice_w'])            

        print (f"Number of masks: {len(data_list)}")
        print (f"Minimum image size, Height : {min(heights)} Width : {min(widths)}")
        print (f"Maximum image size, Height : {max(heights)} Width : {max(widths)}")
        print (f"Average image size, Height : {np.mean(heights)} Width : {np.mean(widths)}")

        return data_list