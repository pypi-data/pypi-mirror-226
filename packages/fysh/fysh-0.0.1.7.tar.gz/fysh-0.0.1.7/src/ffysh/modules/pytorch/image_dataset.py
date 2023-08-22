from ..stream.stream import Stream
from .ffysh_dataset import FfyshDataset
from ..asset.asset import Asset


with optional_dependencies("warn"):
    from torchvision import transforms
    from PIL import Image


    class ImageDataset(FfyshDataset):
        def __init__(self, dataset=None):
            super().__init__(dataset=dataset)        

        def __len__(self):
            return super().__len__()
        
        def __getitem__(self, index):
            asset_string = super().__getitem__(index)
            asset = self.stream.getitem(item_id=asset_string)
            image = Image.open(asset.path)
            resize = transforms.Resize((640, 640))
            image = resize(image)
            convert_tensor = transforms.ToTensor()
            image_tensor = convert_tensor(image)
            return image_tensor