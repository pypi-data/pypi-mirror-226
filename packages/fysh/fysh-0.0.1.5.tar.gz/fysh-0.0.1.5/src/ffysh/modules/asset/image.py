from .asset import Asset


class Image(Asset):
    def __init__(self, annotation_data: dict, **super_kwargs):
        super().__init__(**super_kwargs)
        self.__annotation_data = annotation_data

    @property
    def annotation_data(self):
        return self.__annotation_data

    def __repr__(self):
        return f"Image {self.id}"

    def _to_dict(self):
        return {
            "_id": self.id,
            "annotation_data": self.annotation_data,
            "path": self._asset_workspace_path,
            "stage": self.stage,
            "mimetype": self.mimetype,
            "type": "image",
        }

    # @property
    # def pytorch_annotation_string(self):
    #     output = []
    #     for annotation_object in self.annotation_data:
    #         output.append(
    #             f'{annotation_object["class"]} {" ".join(str(item) for item in annotation_object["boundingBox"])}')
    #     return "\n".join(output)
