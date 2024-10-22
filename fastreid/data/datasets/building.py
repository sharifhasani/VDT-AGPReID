# encoding: utf-8
"""
@author:  Jinkai Zheng
@contact: 1315673509@qq.com
"""

from glob import glob
import os.path as osp
import random
import re

from .bases import ImageDataset
from ..datasets import DATASET_REGISTRY


@DATASET_REGISTRY.register()
class Building(ImageDataset):
    """Building.

    Reference:
        Liu et al. Deep relative distance learning: Tell the difference between similar vehicles. CVPR 2016.

    URL: `<https://pkuml.org/resources/pku-vehicleid.html>`_

    Train dataset statistics:
        - identities: 13164.
        - images: 113346.
    """
    dataset_dir = "building"
    dataset_name = "building"

    def __init__(self, root='datasets', verbose=True, **kwargs):
        super(Building, self).__init__()
        self.root = root
        self.dataset_dir = osp.join(self.root, self.dataset_dir)
        # self.train_dir = osp.join(self.dataset_dir, 'image_train')
        self.train_dir = osp.join(self.dataset_dir, "train")
        # self.train_list = None
        # self.train_list = osp.join(self.dataset_dir, 'name_train.txt')
        # self.query_dir = osp.join(self.dataset_dir, 'image_query')
        self.query_dir = osp.join(self.dataset_dir, "test")
        # self.query_list = osp.join(self.dataset_dir, 'name_query.txt')
        # self.gallery_dir = osp.join(self.dataset_dir, 'image_test')
        self.gallery_dir = osp.join(self.dataset_dir, "test")
        # self.gallery_list = osp.join(self.dataset_dir, 'name_test.txt')

        self.check_before_run()

        train = self.process_dir(dir_path=self.train_dir, type='all')
        query = self.process_dir(dir_path=self.query_dir, type='side')
        gallery = self.process_dir(dir_path=self.gallery_dir, type='sat')

        if verbose:
            print('=> Building loaded')
            self.print_dataset_statistics(train, query, gallery)

        self.train = train
        self.query = query
        self.gallery = gallery

        self.num_train_pids, self.num_train_imgs, self.num_train_cams = self.get_imagedata_info(self.train)
        self.num_query_pids, self.num_query_imgs, self.num_query_cams = self.get_imagedata_info(self.query)
        self.num_gallery_pids, self.num_gallery_imgs, self.num_gallery_cams = self.get_imagedata_info(self.gallery)

    def check_before_run(self):
        """Check if all files are available before going deeper"""
        if not osp.exists(self.dataset_dir):
            raise RuntimeError('"{}" is not available'.format(self.dataset_dir))
        if not osp.exists(self.train_dir):
            raise RuntimeError('"{}" is not available'.format(self.train_dir))
        if not osp.exists(self.query_dir):
            raise RuntimeError('"{}" is not available'.format(self.query_dir))
        if not osp.exists(self.gallery_dir):
            raise RuntimeError('"{}" is not available'.format(self.gallery_dir))

    def process_dir(self, dir_path, list_path=None, relabel=False, type: str='all'):
        img_paths = glob.glob(osp.join(dir_path, '*.jpg'))

        pattern = re.compile(r"([\\|\/]*)(\d*)_(sat|side)_(\d*).jpg$")

        pid_container = set()
        for img_path in img_paths:
            _temp, pid, category, camid = pattern.search(img_path).groups()    
            pid = int(pid)
            if pid == -1:
                continue  # junk images are just ignored
            pid_container.add(pid)
        pid2label = {pid: label for label, pid in enumerate(pid_container)}

        dataset = []

        if type == 'sat':
            pass
        elif type == 'side':
            pass
        elif type == 'all':
            pass
        else:
            raise ValueError("input error")
                
        for img_path in img_paths:
            _temp, pid, category, camid = pattern.search(img_path).groups()
                
            pid, camid = int(pid), int(camid)
            if pid == -1:
                continue  # junk images are just ignored
            # assert 0 <= pid <= 1501  # pid == 0 means background
            # assert 1 <= camid <= 20
            # camid -= 1  # index starts from 0
            # if relabel:
            #     pid = pid2label[pid]
            if category == type:
                dataset.append((img_path, pid, camid))
            elif type == 'all':
                dataset.append((img_path, pid, camid))

        return dataset
    
    def get_imagedata_info(self, data):
        pids, cams = [], []
        for _, pid, camid in data:
            pids.append(pid)
            cams.append(camid)
        pids = set(pids)
        cams = set(cams)
        num_pids = len(pids)
        num_cams = len(cams)
        num_imgs = len(data)
        return num_pids, num_imgs, num_cams
