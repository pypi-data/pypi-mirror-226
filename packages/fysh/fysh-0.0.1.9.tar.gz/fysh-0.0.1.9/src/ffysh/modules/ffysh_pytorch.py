import os
import time
import zipfile
from sys import getsizeof

import numpy as np
import psutil
import torch as T
from PIL import Image


class DatasetStreamLoader:

    def __init__(self, file, batch_size, buffer_batches, shuffle=False):
        self.batch_size = batch_size
        self.buffer_batches = buffer_batches
        self.buffer_size = batch_size * buffer_batches
        self.shuffle = shuffle

        self.ptr = 0    # points into images and labels
        self.fin = zipfile.ZipFile(file, 'r')

        self.images_paths = sorted([path for path in self.fin.namelist(
        ) if path.startswith('Dataset/images/') and path.endswith('.jpg')])
        self.labels_paths = sorted([path for path in self.fin.namelist(
        ) if path.startswith('Dataset/labels/') and path.endswith('.txt')])

        # scale up dataset size for testing purposes: 10,000 * x
        # self.images_paths = [path for path in self.images_paths for i in range(100)]
        # self.labels_paths = [path for path in self.labels_paths for i in range(100)]

        self.images_paths_index = 0
        self.labels_paths_index = 0

        self.images = None
        self.labels = None

        # os.path.basename(self.images_paths[i]) # gets absolute path, useful
        # for matching label with image
        self.memory_message()
        self.reload_data()

    def memory_message(self):
        free_mem = psutil.virtual_memory().free
        # assumes all images in dataset has same dimensions
        example_image = np.asarray(Image.open(self.fin.open(
            self.images_paths[self.images_paths_index])))
        image_size = example_image.nbytes
        batch_mem = image_size * self.batch_size
        buffer_batch_mem = image_size * self.buffer_size

        print(
            f"\n\nWARNING: You have a total of {(free_mem / (1024 ** 2)):.2f} MB of memory "
            f"available on your machine. Each batch of {self.batch_size} images will "
            f"consume {(batch_mem / (1024 ** 2)):.2f} MB of memory. Each buffer "
            f"of {self.buffer_batches} batches (a total of {self.buffer_size} images) will consume "
            f"{(buffer_batch_mem / (1024 ** 2)):.2f} MB of memory. Please make sure "
            f"you have enough memory for at least one buffer, as memory is freed up "
            f"after each buffer is completed.\n\n")

    def reload_data(self):
        xy_lst = []
        ct = 0  # number of files read

        while ct < self.buffer_size:
            if self.images_paths_index >= len(self.images_paths):
                return False

            image_archived = self.fin.open(
                self.images_paths[self.images_paths_index])
            image = np.asarray(Image.open(image_archived))

            label_archived = self.fin.open(
                self.labels_paths[self.labels_paths_index])
            label = np.asarray([line.split() for line in label_archived.read().decode(
                'utf-8').splitlines()], dtype=np.float32)

            xy_lst.append((image, label))
            self.images_paths_index += 1
            self.labels_paths_index += 1
            ct += 1

        if self.shuffle:
            np.random.shuffle(xy_lst)

        images_mat = np.array([xy[0] for xy in xy_lst])
        labels_mat = np.array([xy[1] for xy in xy_lst])

        self.images = T.tensor(images_mat, dtype=T.uint8).to()
        self.labels = T.tensor(labels_mat, dtype=T.float32).to()

        return True

    def __iter__(self):
        return self

    def __next__(self):
        print('index: ', self.images_paths_index)
        if self.ptr + self.batch_size > self.buffer_size:
            self.ptr = 0
            res = self.reload_data()
            if not res:
                raise StopIteration

        start = self.ptr
        end = self.ptr + self.batch_size
        x = self.images[start:end]
        y = self.labels[start:end]
        self.ptr += self.batch_size
        return (x, y)


def main(batch_size, buffer_batches, dataset):
    np.random.seed(1)

    dataset_file = dataset

    dataloader = DatasetStreamLoader(
        dataset_file,
        batch_size,
        buffer_batches,
        shuffle=True)

    max_epochs = 1
    for epoch in range(max_epochs):
        print('epoch: ', epoch)
        for (index, batch) in enumerate(dataloader):
            print('batch: ', index)
            print('images: ', batch[0].shape)
            print('labels: ', batch[1].shape)
            print()


if __name__ == '__main__':
    start_time = time.time()

    # batch_size * buffer_batches should divide the number of images in the
    # dataset to avoid dropping data, and should be less than the number of
    # images in the dataset
    batch_size = 64
    buffer_batches = 16

    main(batch_size, buffer_batches)
    print('time elapsed: ', time.time() - start_time)
