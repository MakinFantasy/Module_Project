import requests
from pprint import pprint
import json


class VkPhotos:
    def __init__(self, vk_id,):
        self.vk_id = vk_id
        self.url = "https://api.vk.com/method/"
        self.access_token = "958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008"
        self.vk_params = {
            "access_token": self.access_token,
            "owner_id": self.vk_id,
            "v": "5.131"
        }

    def get_phots_from_vk(self, photos_count):
        info_list = []
        likes_dict ={}
        photos_params ={
            "album_id": "profile",
            "extended": "1",
            "count": photos_count,
            "photo_size": "1"
        }

        photos_url = self.url + "photos.get"
        response = requests.get(photos_url, params = {
            **self.vk_params,
            **photos_params
        }).json()
        for item in response["response"]["items"]:
            likes = str(item["likes"]["count"])
            photo_url = item["sizes"][-1]["url"]
            likes_dict["file_name"] = likes
            likes_dict["sizes"] = item["sizes"][-1]["type"]
            likes_dict["url"] = photo_url
            info_list.append(likes_dict)
        return info_list



