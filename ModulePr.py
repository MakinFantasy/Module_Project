import json
import requests
from pprint import pprint
from datetime import datetime


class VkPhotos:
    def __init__(self, vk_id):
        self.url = "https://api.vk.com/method/"
        self.token = "958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008"
        self.id = vk_id
        self.params = {
            "access_token": self.token,
            "owner_id": self.id,
            "v": "5.131"
        }

    def get_photos(self, photos_count):
        list_get_photos = []
        dict_of_likes_url = {}
        get_photos_params = {
            "album_id": "profile",
            "extended": "1",
            "count": photos_count,
            "photo_sizes": "1"
        }
        get_photos_url = self.url + "photos.get"
        response = requests.get(get_photos_url, params={
            **self.params, **get_photos_params
        }).json()
        for items in response["response"]["items"]:
            photos_likes = str(items["likes"]["count"])
            photo_url = items["sizes"][len(items["sizes"]) - 1]["url"]
            date = items["date"]
            date = str(datetime.utcfromtimestamp(date).strftime('%Y-%m-%d_%H_%M_%S'))
            dict_of_likes_url["file_name"] = photos_likes
            dict_of_likes_url["sizes"] = items["sizes"][len(items["sizes"]) - 1]["type"]
            dict_of_likes_url["url"] = photo_url
            dict_of_likes_url["date"] = date
            list_get_photos.append(dict_of_likes_url)
            dict_of_likes_url = {}
        return list_get_photos


class YaDisk:
    def __init__(self, list_to_upload, token, vk_id):
        self.token = token
        self.url = "https://cloud-api.yandex.net/v1/disk/resources/"
        self.list_to_upload = list_to_upload
        self.headers = {
            'Authorization': self.token
        }
        self.id = vk_id

    def get_list_photos_yadisk(self):
        result_list = []
        response = requests.get(self.url + "files", headers=self.headers).json()
        for dict_params in response["items"]:
            name = dict_params["name"]
            result_list.append(name)
        return result_list

    def upload(self):
        photos_check = self.get_list_photos_yadisk()
        photos_upload_count = 0
        folder_create = requests.put(self.url, headers=self.headers, params={
            "path": self.id
        })
        if folder_create.status_code == 201 or folder_create.status_code == 409:
            if folder_create.status_code == 201:
                pprint(f"Папка {self.id} создана")
            else:
                pprint(f"Папка {self.id} уже существует")
            for value in self.list_to_upload:
                info = value["file_name"] + ".jpeg"
                file_name = self.id + "/" + value["file_name"] + ".jpeg"
                file_url = value["url"]
                params = {
                    "path": file_name,
                    "url": file_url
                }
                if info not in photos_check:
                    response = requests.post(self.url + "upload", headers=self.headers, params=params)
                    if response.status_code != 202:
                        pprint(f"Произошла ошибка {response.status_code} при загрузке {file_name}")
                    else:
                        pprint(f"Загрузка фото {info} прошла успешно")
                        photos_upload_count += 1
                else:
                    pprint(f"Файл с именем {info} уже существует")
        else:
            print(f"Произошла ошибка {folder_create.status_code}")
        pprint(f"Файлов загружено: {photos_upload_count}")
        pprint(f"Загрузка завершена")


def json_file(list_data):
    for check in list_data:
        for check_2 in list_data:
            if (check["file_name"] == check_2["file_name"]) and (check["url"] != check_2["url"]):
                check["file_name"] = check["file_name"] + "_" + "(" + check["date"] + ")"
                check_2["file_name"] = check_2["file_name"] + "_" + "(" + check_2["date"] + ")"
    return list_data


def rework_json_file(dict_file):
    info = dict_file
    for check_2 in info:
        check_2["file_name"] += ".jpeg"
        del check_2["date"]
        del check_2["url"]
    with open("data_file.json", "w") as file:
        json.dump(info, file, indent=5)
    return info


id_vk = "552934290"
ya_token = "AQAAAAAZJUXrAADLW5xzprLGbk6HuIyygQYecHU"
count = 50

user = VkPhotos(id_vk)
images = user.get_photos(count)
file_dict = json_file(images)

uploader = YaDisk(file_dict, ya_token, id_vk)
uploader.upload()
uploader.get_list_photos_yadisk()
print()
pprint(rework_json_file(file_dict))















