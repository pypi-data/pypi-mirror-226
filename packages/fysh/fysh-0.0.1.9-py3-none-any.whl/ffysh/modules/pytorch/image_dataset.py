
from ..utils.imports import optional_dependencies
from ..stream.stream import Stream
from ..asset.asset import Asset



with optional_dependencies("warn"):
    from torchvision import transforms
    from PIL import Image

    from .ffysh_dataset import FfyshDataset


    class ImageDataset(FfyshDataset):
        def __init__(self, dataset=None, resize_amount = 640):
            super().__init__(dataset=dataset)        
            self.resize_amount = resize_amount

        def __len__(self):
            return super().__len__()
        
        def __getitem__(self, index):
            asset_string = super().__getitem__(index)
            asset = self.stream.getitem(item_id=asset_string)
            image = Image.open(asset.path)
            resize = transforms.Resize((self.resize_amount, self.resize_amount))
            image = resize(image)
            convert_tensor = transforms.ToTensor()
            image_tensor = convert_tensor(image)
            return image_tensor