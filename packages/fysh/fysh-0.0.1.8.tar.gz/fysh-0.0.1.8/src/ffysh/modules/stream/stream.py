import math
import os.path
import typing
import uuid
from ..internals.project import flockfysh_path
from ..internals.errors import NotFoundException
from ..internals.api import _api_session
from ..internals import file
from ordered_set import OrderedSet
from ..asset.image import Image
from ..asset.asset import Asset
import asyncio
from zipfile import ZipFile
import shutil


class Stream:
    _stream_store = {}

    @staticmethod
    def _get_stream_path(stream_id: str):
        return flockfysh_path(os.path.join("streams", stream_id))

    @staticmethod
    def _generate_stream_id():
        while True:
            new_id = uuid.uuid4().hex
            if not os.path.exists(flockfysh_path(os.path.join("streams", new_id))):
                return new_id

    @staticmethod
    def load(saved_stream_id: str):
        cached_stream = Stream._stream_store.get(saved_stream_id, None)
        if cached_stream is not None:
            return cached_stream
        if not os.path.exists(Stream._get_stream_path(saved_stream_id)):
            raise NotFoundException("This stream does not exist!")
        saved_stream_info_path = os.path.join(Stream._get_stream_path(saved_stream_id), "info.json")
        saved_stream_info = file.read_json(saved_stream_info_path)
        saved_stream = Stream(_internal=True,
                              _stream_id=saved_stream_id,
                              _dataset_id=saved_stream_info["dataset_id"],
                              _queries=saved_stream_info["queries"],
                              _dataset_info=saved_stream_info["dataset_info"])
        Stream._stream_store[saved_stream_id] = saved_stream
        return saved_stream

    @staticmethod
    def _create(dataset_id: str, dataset_info, *,
                asset_stage: typing.Literal["completed", "feedback", "uploaded"] = None,
                asset_filename_search: str = None):
        _queries = {
            "stage": asset_stage,
            "displayName": asset_filename_search,
        }
        new_stream = Stream(_internal=True, _stream_id=Stream._generate_stream_id(), _dataset_id=dataset_id,
                            _dataset_info=dataset_info, _queries=_queries)
        file.write_json(new_stream.__stream_info_path,
                        {"dataset_id": new_stream.__dataset_id, "queries": new_stream.__queries,
                         "dataset_info": new_stream.__dataset_info})
        Stream._stream_store[new_stream.stream_id] = new_stream
        return new_stream

    @property
    def _stream_seek(self):
        if self.__stream_seek is None:
            try:
                self.__stream_seek = file.read_json(self.__stream_seek_path)
                result = self.__stream_seek["stream_seek"]
                return result
            except (IOError, KeyError, TypeError):
                self.__stream_seek = {"stream_seek": {}}
                file.write_json(self.__stream_seek_path, self.__stream_seek)
        return self.__stream_seek["stream_seek"]

    @_stream_seek.setter
    def _stream_seek(self, seek_structure=None):
        self.__stream_seek = {"stream_seek": seek_structure}
        file.write_json(self.__stream_seek_path, self.__stream_seek)

    @property
    def _item_ids(self):
        if self.__item_ids is None:
            if os.path.exists(self.__item_ids_path):
                data = file.read_json(self.__item_ids_path)
                self.__item_ids = OrderedSet(data)
            else:
                self.__item_ids = OrderedSet()
                file.write_json(self.__item_ids_path, list(self.__item_ids))
        return self.__item_ids

    @_item_ids.setter
    def _item_ids(self, item_ids=None):
        if item_ids is None:
            item_ids = []
        self.__item_ids = list(item_ids)
        file.write_json(self.__item_ids_path, self.__item_ids)
    
    @property
    def _iterator_start_index(self):
        if self.__iterator_start_index is None:
            if os.path.exists(self.__iterator_start_index_path):
                self.__iterator_start_index = file.read_json(self.__iterator_start_index_path)
            else:
                self.__iterator_start_index = 0
                file.write_json(self.__iterator_start_index_path, self.__iterator_start_index)
        return self.__iterator_start_index

    @_iterator_start_index.setter
    def _iterator_start_index(self, new_index):
        if not isinstance(new_index, int):
            raise TypeError("Iterator start index must be an integer.")
        self.__iterator_start_index = new_index
        file.write_json(self.__iterator_start_index_path, self.__iterator_start_index)

    @property 
    def _cache_size(self):
        return len(self.__item_data_cache)

    @property
    def _finished(self):
        if self.__finished is None:
            if os.path.exists(self.__stream_finished_path):
                self.__finished = file.read_json(self.__stream_finished_path)
            else:
                self.__finished = False
                file.write_json(self.__stream_finished_path, self.__finished)
            return self.__finished
        return self.__finished

    @_finished.setter
    def _finished(self, new_state):
        if not isinstance(new_state, bool):
            raise TypeError("Finished state must be true or false.")
        self.__finished = new_state
        file.write_json(self.__stream_finished_path, self.__finished)

    @property
    def finished(self):
        return self._finished

    def __init__(self, *_args,
                 _stream_id: str,
                 _dataset_id: str = None,
                 _queries=None,
                 _internal=False,
                 _dataset_info):
        if _queries is None:
            _queries = {}
        if not _internal:
            raise RuntimeError("This class cannot be called by the user.")
        self.__stream_id = _stream_id
        self.__dataset_id = _dataset_id
        self.__dataset_info = _dataset_info
        self.__queries = _queries
        self.__stream_path = Stream._get_stream_path(self.__stream_id)
        os.makedirs(self.__stream_path, exist_ok=True)
        self.__stream_info_path = os.path.join(self.__stream_path, "info.json")
        self.__stream_seek_path = os.path.join(self.__stream_path, "seek.json")
        self.__stream_finished_path = os.path.join(self.__stream_path, "finished.json")
        self.__item_ids_path = os.path.join(self.__stream_path, "item_ids.json")
        self.__item_data_path = os.path.join(self.__stream_path, "item_data")
        self.__iterator_start_index_path = os.path.join(self.__stream_path, "iterator_start_index.json")
        os.makedirs(self.__item_data_path, exist_ok=True)
        self.__item_data_cache = {}
        self.__stream_seek = None
        self.__item_ids = None
        self.__finished = None
        self.__iterator_start_index = None

    @property
    def _dataset_info(self):
        return self.__dataset_info

    @property
    def classes(self):
        return self.__dataset_info["classes"]

    @property
    def stream_id(self):
        return self.__stream_id

    @property
    def stream_queries(self):
        return self.__queries

    @property
    def dataset_id(self):
        return self.__dataset_id
    
    def __getitem(self, item_id):
        try:
            item = self.__item_data_cache[item_id]
            return item
        except KeyError:
            try:
                item = file.read_json(os.path.join(self.__item_data_path, f"{item_id}.json"))
                item_type = item["type"]
                if item_type == "image":
                    abstract_item = Image(
                        asset_id=item["_id"],
                        asset_mimetype=item["mimetype"],
                        annotation_data=item["annotation_data"],
                        asset_stage=item["stage"],
                        asset_workspace_path=item["path"],
                        _internal=True)
                else:
                    abstract_item = Asset(
                        asset_id=item["_id"],
                        asset_stage=item["stage"],
                        asset_mimetype=item["mimetype"],
                        asset_workspace_path=item["path"],
                        _internal=True)
                self.__item_data_cache[item_id] = abstract_item
                return self.__item_data_cache[item_id]
            except IOError:
                raise RuntimeError("This item is not found.")
    
    def getitem(self, item_id):
        try:
            item = self.__item_data_cache[item_id]
            return item
        except KeyError:
            try:
                item = file.read_json(os.path.join(self.__item_data_path, f"{item_id}.json"))
                item_type = item["type"]
                if item_type == "image":
                    abstract_item = Image(
                        asset_id=item["_id"],
                        asset_mimetype=item["mimetype"],
                        annotation_data=item["annotation_data"],
                        asset_stage=item["stage"],
                        asset_workspace_path=item["path"],
                        _internal=True)
                else:
                    abstract_item = Asset(
                        asset_id=item["_id"],
                        asset_stage=item["stage"],
                        asset_mimetype=item["mimetype"],
                        asset_workspace_path=item["path"],
                        _internal=True)
                self.__item_data_cache[item_id] = abstract_item
                return self.__item_data_cache[item_id]
            except IOError:
                raise RuntimeError("This item is not found.")

    def __getitem__(self, item):
        if isinstance(item, str):
            return self.__getitem(item)
        elif isinstance(item, int):
            item_no = item
            self.expand(item_no + 1)
            item_id = self._item_ids[item_no]
            return self.__getitem(item_id)
        elif isinstance(item, slice):
            cur_slice = item
            start = cur_slice.start
            stop = cur_slice.stop
            step = cur_slice.step
            if start is None:
                start = 0
            if stop is None or stop < 0 or start < 0:
                self.expand()
            else:
                self.expand(max(start + 1, stop + 1))
            return list(map(lambda item_id: self.__getitem(item_id), self._item_ids[start:stop:step]))

    def _save_item(self, obj):
        to_save = obj._to_dict()
        self.__item_data_cache[obj.id] = obj
        file.write_json(os.path.join(self.__item_data_path, f"{obj.id}.json"), to_save)

    def __iter__(self):
        return self.create_iterator(pre_download=True)

    def create_iterator(self, *, start_index: int = 0, chunk_size: int = None, pre_download: bool = False,
                        batch_size: int = 20, reset=False, save=False):
        if chunk_size is not None:
            if not isinstance(chunk_size, int):
                raise AssertionError("Chunk size must be an integer.")
            if chunk_size <= 0:
                raise AssertionError("Chunk size must be greater than 0.")
        if chunk_size is not None:
            self.free()

        async def download_current_page(current_page):
            coroutines = []
            for item in current_page:
                item: Asset
                coroutines.append(item._download())
            await asyncio.gather(*coroutines)

        def process_current_page(current_page):
            if pre_download:
                asyncio.run(download_current_page(current_page))
            if save:
                self.download(whole=False, chunk=True, assets=current_page, reset=reset)
            self._iterator_start_index = len(self._item_ids)
            for item in current_page:
                yield item

        def purge_older_chunks(index):
            if chunk_size is not None:
                self.free(0, math.floor(index / chunk_size) * chunk_size)

        prev_len = start_index
        while True:
            current_page = []
            for i in range(prev_len, len(self._item_ids)):
                current_item_id = self._item_ids[i]
                item = self[current_item_id]
                if len(current_page) >= batch_size:
                    for item in process_current_page(current_page):
                        yield item
                    current_page = []
                    purge_older_chunks(i)
                current_page.append(item)
            for item in process_current_page(current_page):
                yield item
            purge_older_chunks(prev_len)
            prev_len = len(self._item_ids)
            try:
                self.next_assets(batch_size)
            except StopIteration:
                return 

    @property
    def dataset(self):
        from ..dataset.dataset import Dataset
        return Dataset(self.dataset_id)

    def next_assets(self, count: int = 20):
        if self.finished:
            raise StopIteration("Stream has ended.")
        
        response = _api_session.get(f'/api/datasets/{self.dataset_id}/assets', data={
            "stage": self.__queries.get("stage", None),
            "next": self._stream_seek.get("next", None),
            "limit": count
        })

        json_result = response.json()["data"]
                
        result = json_result["data"]
        cursor = json_result["meta"]
        if response.status_code >= 500:
            raise RuntimeError("There is a server error. Please try again later.")

        asset_objects = []

        async def process_response():
            # Download cycle
            for asset in result:
                asset_type = asset["type"]
                if asset_type == "image":
                    asset_obj = Image(
                        asset_id=asset["_id"],
                        annotation_data=asset["annotationData"],
                        asset_url=asset["url"],
                        asset_mimetype=asset["mimetype"],
                        asset_stage=asset["stage"],
                        _internal=True)
                else:
                    asset_obj = Asset(
                        asset_id=asset["_id"],
                        asset_url=asset["url"],
                        asset_stage=asset["stage"],
                        asset_mimetype=asset["mimetype"],
                        _internal=True)
                asset_objects.append(asset_obj)

        asyncio.run(process_response())

        for asset_object in asset_objects:
            self._save_item(asset_object)
            self._item_ids.append(asset_object.id)
        self._item_ids = self._item_ids

        if not cursor["hasNext"]:
            self._finished = True
        else:
            self._stream_seek = cursor

        return asset_objects

    def expand(self, length=None):
        while length is None or len(self._item_ids) < length:
            try:
                self.next_assets(20)
            except StopIteration:
                break

    def free(self, start=None, end=None, ignore_errors=False):
        for asset_id in self._item_ids[start:end]:
            asset = self.__getitem(asset_id)
            asset.free(ignore_errors=ignore_errors)
        self.__item_data_cache = {}

    def _construct_yolov5_yaml(self):
        names = "\n".join(f"  {index}: {class_name}" for index, class_name in enumerate(self.classes))
        output = f'''path: ../dataset
train: train/images
val: valid/images

names:
{names}
        '''
        return output

    def download(self, whole=False, chunk=False, assets=False, reset=False):
        save_location = os.path.join(os.getcwd(), os.path.join('downloads', self.stream_id))
        if not os.path.exists(os.path.join(os.getcwd(), 'downloads')):
            os.mkdir(os.path.join(os.getcwd(), 'downloads'))
        if not os.path.exists(save_location):
            os.mkdir(save_location)
        elif reset:
            shutil.rmtree(save_location)
            os.mkdir(save_location)

        if whole:
            self.expand()
        if not chunk:
            for asset in self:
                shutil.copy(asset.path, save_location)
        else:
            if not isinstance(assets, list):
                print('[ERROR] Assets must be a list.')
                return
            for asset in assets:
                shutil.copy(asset.path, save_location)
        
        print(f'\n[SUCCESS] Dataset saved to {save_location}.')

    # def to_yolov5_zip(self, save_location: str, confidence_level: float = 0.4):
    #     with ZipFile(save_location, "w", allowZip64=True) as new_zip:
    #         root_path = os.path.join("/", "dataset")
    #         asset: Image
    #         for asset in self:
    #             rand_output = random.random()
    #             if rand_output < confidence_level:
    #                 asset_type = "train"
    #             else:
    #                 asset_type = "valid"
    #             new_zip.write(asset.path, os.path.join(root_path, asset_type, "images", asset.filename))
    #             new_zip.writestr(os.path.join(root_path, asset_type, "labels", f'{asset.id}.txt'),
    #                              asset.pytorch_annotation_string)
    #         new_zip.writestr(os.path.join(root_path, "dataset.yaml"), self._construct_yolov5_yaml())
    #
    # def to_yolov5_model(self, save_location: str, confidence_level: float = 0.4):
    #     shutil.rmtree(save_location, ignore_errors=True)
    #     root_path = os.path.join(save_location, "dataset")
    #     os.makedirs(root_path)
    #     asset: Image
    #     for asset in self:
    #         rand_output = random.random()
    #         if rand_output < confidence_level:
    #             asset_type = "train"
    #         else:
    #             asset_type = "valid"
    #         image_path = os.path.join(root_path, asset_type, "images")
    #         label_path = os.path.join(root_path, asset_type, "labels")
    #         os.makedirs(image_path, exist_ok=True)
    #         os.makedirs(label_path, exist_ok=True)
    #         shutil.copy2(asset.path, os.path.join(image_path, asset.filename))
    #         with open(os.path.join(label_path, f'{asset.id}.txt'), "w",
    #                   encoding="UTF-8") as file:
    #             file.write(asset.pytorch_annotation_string)
    #     with open(os.path.join(root_path, 'dataset.yaml'), 'w') as file:
    #         file.write(self._construct_yolov5_yaml())
