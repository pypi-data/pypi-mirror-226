
from ..utils.imports import optional_dependencies
from ..stream.stream import Stream
from ..dataset.dataset import Dataset


with optional_dependencies("warn"):
    import torch   

    class FfyshDataset(torch.utils.data.Dataset):
        def __init__(self, dataset=None):
            if dataset is None:
                raise Exception("No dataset ID was provided.")
            if not isinstance(dataset, Dataset):
                raise Exception("Dataset must be of type Dataset.")
            self.stream = dataset.create_stream()
        
        def __len__(self):
            return self.stream.dataset.length
        
        def __getitem__(self, index):
            if index >= len(self.stream._item_ids):
                next(self.stream.create_iterator(start_index=self.stream._iterator_start_index, batch_size=(index - self.stream._iterator_start_index + 1), pre_download=True))
            return self.stream._item_ids[index]