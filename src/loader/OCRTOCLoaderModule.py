import math
import os
import glob
import sys
import random
import json
import pandas as pd

import bpy
import numpy as np
from mathutils import Matrix, Vector

from src.camera.CameraInterface import CameraInterface
from src.loader.LoaderInterface import LoaderInterface
from src.utility.Utility import Utility
from src.utility.Config import Config
from src.utility.loader.ObjectLoader import ObjectLoader


class OCRTOCLoaderModule(LoaderInterface):
    """ Loads the 3D models of any BOP dataset and allows replicating BOP scenes

    - Interfaces with the bob_toolkit, allows loading of train, val and test splits
    - Relative camera poses are loaded/computed with respect to a reference model
    - Sets real camera intrinsics

    **Configuration**:

    .. csv-table::
       :header: "Parameter", "Description"

       "cam_type", "Camera type. Type: string. Optional. Default value: ''."
       "sys_paths", "System paths to append. Type: list."
       "bop_dataset_path", "Full path to a specific bop dataset e.g. /home/user/bop/tless. Type: string."
       "mm2m", "Specify whether to convert poses and models to meters. Type: bool. Optional. Default: False."
       "split", "Optionally, test or val split depending on BOP dataset. Type: string. Optional. Default: test."
       "scene_id", "Optionally, specify BOP dataset scene to synthetically replicate. Type: int. Default: -1 (no scene "
                   "is replicated, only BOP Objects are loaded)."
       "sample_objects", "Toggles object sampling from the specified dataset. Type: boolean. Default: False."
       "num_of_objs_to_sample", "Amount of objects to sample from the specified dataset. Type: int. If this amount is "
                                "bigger than the dataset actually contains, then all objects will be loaded. Type: int."
       "obj_instances_limit", "Limits the amount of object copies when sampling. Type: int. Default: -1 (no limit)."
       "obj_ids", "List of object ids to load. Type: list. Default: [] (all objects from the given BOP dataset if "
                  "scene_id is not specified)."
       "model_type", "Optionally, specify type of BOP model. Type: string. Default: "". Available: [reconst, cad or eval]."
    """

    def __init__(self, config):
        LoaderInterface.__init__(self, config)

        self.bop_dataset_name = "OCRTOC"

        with open(self.config.get_string('camera_config_path')) as f:
            self.camera_info = json.load(f)  # keys: cx, cy, fx, fy, depth_scale, height, width

        self.sample_objects = self.config.get_bool("sample_objects", False)
        if self.sample_objects:
            self.num_of_objs_to_sample = self.config.get_int("num_of_objs_to_sample")
            self.obj_instances_limit = self.config.get_int("obj_instances_limit", -1)

        self.dataset = self.config.get_string("dataset", "/home/lsy/dataset/ocrtoc")
        self.allow_duplication = self.config.get_bool("allow_duplication", False)

        self.scale = 1
        self.obj_df = pd.read_csv(os.path.join(self.dataset, 'objects.csv'))

    def run(self):
        # bpy.context.scene.world["category_id"] = 0
        bpy.context.scene.render.resolution_x = self.camera_info['width']
        bpy.context.scene.render.resolution_y = self.camera_info['height']

        # Collect camera and camera object
        cam_ob = bpy.context.scene.camera
        cam = cam_ob.data
        cam['loaded_intrinsics'] = np.array([
            [self.camera_info['fx'], 0, self.camera_info['cx']],
            [0, self.camera_info['fy'], self.camera_info['cy']],
            [0, 0, 1]
        ])
        cam['loaded_resolution'] = self.camera_info['width'], self.camera_info['height']

        config = Config({})
        camera_module = CameraInterface(config)
        camera_module._set_cam_intrinsics(cam, config)

        loaded_objects = []

        # only load all/selected objects here, use other modules for setting poses
        # e.g. camera.CameraSampler / object.ObjectPoseSampler
        obj_ids = list(range(self.obj_df.shape[0]))
        # if sampling is enabled
        if self.sample_objects:
            loaded_ids = {}
            loaded_amount = 0
            if self.obj_instances_limit != -1 and len(obj_ids) * self.obj_instances_limit < self.num_of_objs_to_sample:
                raise RuntimeError("{}'s {} split contains {} objects, {} object where requested to sample with "
                                    "an instances limit of {}. Raise the limit amount or decrease the requested "
                                    "amount of objects.".format(self.bop_dataset_path, self.split, len(obj_ids),
                                                                self.num_of_objs_to_sample,
                                                                self.obj_instances_limit))
            while loaded_amount != self.num_of_objs_to_sample:
                obj_id = random.choice(obj_ids)
                if obj_id not in loaded_ids.keys():
                    loaded_ids.update({obj_id: 0})
                # if there is no limit or if there is one, but it is not reached for this particular object
                if self.obj_instances_limit == -1 or loaded_ids[obj_id] < self.obj_instances_limit:
                    cur_obj = self._load_mesh(obj_id, scale=self.scale)
                    loaded_ids[obj_id] += 1
                    loaded_amount += 1
                    loaded_objects.append(cur_obj)
        else:
            for obj_id in obj_ids:
                cur_obj = self._load_mesh(obj_id, scale=self.scale)
                loaded_objects.append(cur_obj)
        self._set_properties(loaded_objects)

    def _load_mesh(self, obj_id, scale=1):
        """ Loads BOP mesh and sets category_id.

        :param obj_id: The obj_id of the BOP Object. Type: int.
        :return: Current object. Type: bpy.types.Object.
        """

        model_path = glob.glob(os.path.join(self.dataset, self.obj_df['location'][obj_id], 'visual_meshes', '*.dae'))[0]
        # model_path = glob.glob(os.path.join(self.dataset, self.obj_df['location'][obj_id], 'meshes', '*.obj'))[0]
        # texture_paths = glob.glob(os.path.join(self.dataset, self.obj_df['location'][obj_id], 'meshes', '*.png'))
        # if not texture_paths:
        #     texture_paths = glob.glob(os.path.join(self.dataset, self.obj_df['location'][obj_id], 'meshes', '*.jpg'))

        # Gets the objects if it is already loaded
        cur_obj = self._get_loaded_obj(model_path)
        # if the object was not previously loaded - load it, if duplication is allowed - duplicate it
        if cur_obj is None:
            # bpy.ops.import_scene.obj(filepath=model_path)
            bpy.ops.wm.collada_import(filepath=model_path)
            cur_obj = bpy.context.selected_objects[-1]
        elif self.allow_duplication:
            bpy.ops.object.duplicate({"object": cur_obj, "selected_objects": [cur_obj]})
            cur_obj = bpy.context.selected_objects[-1]

        scale = 1.0
        cur_obj.scale = Vector((scale, scale, scale))
        cur_obj['category_id'] = obj_id + 1  # 0 is the category id for background
        cur_obj['model_path'] = model_path
        cur_obj['name'] = self.obj_df['object'][obj_id]
        cur_obj['supercategory'] = self.obj_df['class'][obj_id]
        # if texture_paths:
        #     self._load_texture(cur_obj, texture_paths[0])

        cur_obj["is_bop_object"] = True
        cur_obj["bop_dataset_name"] = self.bop_dataset_name
        return cur_obj

    def _get_loaded_obj(self, model_path):
        """ Returns the object if it has already been loaded.

        :param model_path: Model path of the new object. Type: string.
        :return: Object if found, else return None. Type: bpy.types.Object/None.
        """
        for loaded_obj in bpy.context.scene.objects:
            if 'model_path' in loaded_obj and loaded_obj['model_path'] == model_path:
                return loaded_obj
        return

    def _load_texture(self, cur_obj, texture_file_path):
        """
        Load the textures for the ycbv objects, only those contain texture information

        :param cur_obj: The object to use. Type: bpy.types.Object.
        :param texture_file_path: path to the texture file (most likely ".png")
        """
        mat = bpy.data.materials.new(name="bop_" + self.bop_dataset_name + "_texture_material")

        mat.use_nodes = True

        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        color_image = nodes.new('ShaderNodeTexImage')
        if not os.path.exists(texture_file_path):
            raise Exception("The texture path for the ycbv object could not be loaded from the "
                            "file: {}".format(texture_file_path))
        color_image.image = bpy.data.images.load(texture_file_path, check_existing=True)

        principled = Utility.get_the_one_node_with_type(nodes, "BsdfPrincipled")
        links.new(color_image.outputs["Color"], principled.inputs["Base Color"])

        if cur_obj.data.materials:
            # assign to 1st material slot
            cur_obj.data.materials[0] = mat
        else:
            # no slots
            cur_obj.data.materials.append(mat)
