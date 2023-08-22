import mimetypes
import os
import typing
from ..internals.project import flockfysh_path
import aiofiles
import asyncio
import aiohttp
from ..internals.api import _api_session

#IOModeParameters = typing.Union[str, bytes, os.PathLike[str], os.PathLike[bytes], int, typing.Literal[
 #   "rb+", "r+b", "+rb", "br+", "b+r", "+br", "wb+", "w+b", "+wb", "bw+", "b+w", "+bw", "ab+", "a+b", "+ab", "ba+", "b+a", "+ba", "xb+", "x+b", "+xb", "bx+", "b+x", "+bx", "rb", "br", "rbU", "rUb", "Urb", "brU", "bUr", "Ubr", "wb", "bw", "ab", "ba", "xb", "bx"]]


class Asset:
    def __init__(self, *, asset_id: str, asset_url: str = None, asset_workspace_path: str = None, asset_stage: str,
                 asset_mimetype: str, file_name: str,
                 _internal=False):
        if not _internal:
            raise RuntimeError("You cannot call this class.")

        self.__asset_id = asset_id
        self._asset_workspace_path = asset_workspace_path
        
        
        self.display_name = file_name

        if self._asset_workspace_path is None:
            extension = mimetypes.guess_extension(asset_mimetype)
            if extension:
                abs_path = os.path.join(flockfysh_path("assets"), f"{self.__asset_id}{extension}")
            else:
                abs_path = os.path.join(flockfysh_path("assets"), f"{self.__asset_id}")
            
            self._asset_workspace_path = os.path.relpath(abs_path, flockfysh_path("."))

        #print("PATH: ", os.path.join(flockfysh_path("."), self._asset_workspace_path))


        self.__asset_mimetype = asset_mimetype
        self.__asset_url = asset_url
        self.__asset_stage = asset_stage

    async def _download(self):
        if not self.__asset_url:
            try:
                data = _api_session.get(f"/api/datasets/getByAssetId/{self.id}").json()
                print(data)
                self.__asset_url = data["data"]["url"]
            except Exception as e:
                raise RuntimeError("Asset has been deleted. You'll need to create a new stream.")
        os.makedirs(flockfysh_path("assets"), exist_ok=True)
        temp_path = os.path.join(flockfysh_path("assets"), f'{self.__asset_id}.tmp')
        async with aiohttp.ClientSession() as client:
            async with client.get(self.__asset_url) as response:
                if os.path.exists(self.path):
                    return
                async with aiofiles.open(temp_path, "wb") as file:
                    async for chunk, _ in response.content.iter_chunks():
                        await file.write(chunk)
        os.rename(temp_path, self.path)

    @property
    def id(self):
        return self.__asset_id

    @property
    def path(self):
        if not self._asset_workspace_path:
            return None
        else:
            return os.path.join(flockfysh_path("."), self._asset_workspace_path)

    @property
    def is_downloaded(self):
        return os.path.exists(self.path)

    @property
    def mimetype(self):
        return self.__asset_mimetype

    @property
    def stage(self):
        return self.__asset_stage


    @property
    def filename(self):
        return os.path.basename(self.path)

    def free(self, ignore_errors=False):
        try:
            os.remove(self.path)
        except FileNotFoundError:
            return
        except Exception as e:
            if ignore_errors:
                return
            else:
                raise e

    def open(self, mode = "rb", **kwargs):
        if not self.path or not os.path.exists(self.path):
            asyncio.run(self._download())
        return open(self.path, mode=mode, **kwargs)

    async def async_open(self, mode = "rb", **kwargs):
        if not self.path or not os.path.exists(self.path):
            await self._download()
        return aiofiles.open(self.path, mode=mode, **kwargs)

    def _to_dict(self):
        return {
            "_id": self.id,
            "path": self._asset_workspace_path,
            "stage": self.stage,
            "type": "generic",
            "mimetype": self.mimetype,
        }

    def __repr__(self):
        return f"Generic asset {self.__asset_id}"
