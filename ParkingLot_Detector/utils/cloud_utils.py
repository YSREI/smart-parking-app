import requests
import json
import time


''' #以后上传别的东西（比如照片、debug日志）时备用。
class CloudStorage:
    def __init__(self, api_url):
        """
        初始化云存储接口
        :param api_url: Firebase Realtime Database URL, like https://your-project-id.firebaseio.com/
        """
        if not api_url.endswith('/'):
            api_url += '/'
        self.api_url = api_url
        print(f" 成功初始化 Firebase REST API: {self.api_url}")

    def upload_json(self, data, node_path):
        """
        上传一段JSON数据到Firebase指定路径
        :param data: 要上传的数据 (dict)
        :param node_path: Firebase的节点路径，比如 "parking-lots/lot-a/snapshot/image1"
        """
        url = f"{self.api_url}{node_path}.json"
        try:
            response = requests.put(url, json=data)
            if response.status_code == 200:
                print(f" 成功上传到Firebase节点: {node_path}")
            else:
                print(f" 上传失败，状态码 {response.status_code}: {response.text}")
        except Exception as e:
            print(f" 上传异常: {e}")
            '''


class CloudUploader:
    def __init__(self, api_url, lot_id):
        self.api_url = api_url.rstrip('/')
        self.lot_id = lot_id

    def upload_parking_status(self, occupied, empty):
        """上传停车场整体空位信息"""
        data = {
            "occupied": occupied,
            "empty": empty,
            "timestamp": int(__import__("time").time())
        }
        url = f"{self.api_url}/parking-lots/{self.lot_id}/availability.json"
        response = requests.put(url, json=data)
        return response.status_code == 200

    def upload_spaces_status(self, results):
        """上传每个车位的占用状态"""
        for spot_id, spot_info in results.items():
            self.upload_single_space(spot_id, spot_info["status"])

    def upload_single_space(self, space_id, status):
        """上传单个车位状态"""
        data = {
            "status": status
        }
        url = f"{self.api_url}/parking-lots/{self.lot_id}/spaces/{space_id}.json"
        response = requests.put(url, json=data)
        if response.status_code != 200:
            print(f"上传车位 {space_id} 状态失败：{response.status_code}")