import requests

# base_url = "http://127.0.0.1:8000/"
# base_url = "http://127.0.0.1:8000/images/sort"

class RequestData():
    def __init__(self, base_url):
        self.base_url = base_url

    def next(self, number: int):
        url = self.base_url + "images/next"
        params = {"number" : number}
        try:
            response = requests.get(url, params=params)
        except:
            print("No connection to backend")
            return None
            
        return response.json()

    def reload(self):
        url = self.base_url + "images/reload"
        
        try:
            response = requests.get(url)
        except:
            print("No connection to backend")
            return None

        return response.json()

    def __sort(self, options):
        """Before sorting be sure that sketch is set"""
        url = self.base_url + "images/sort"
        # params = {}
        response = requests.post(url, json=options)
        return response.json()

    def __set_sketch(self, path, landmarks):
        url = self.base_url + "set-sketch"
        body = {"path": path, "landmarks": landmarks}
        response = requests.post(url, json=body)
        return response.json()

    def sort(self, options, path, landmarks):
        self.__set_sketch(path, landmarks)
        self.__sort(options)
        return self.reload()
    
    def add_sketch_to_gallery(self, path, landmarks):
        url = self.base_url + "sketch/add-to-gallery"
        body = {"path": path, "landmarks": landmarks}

        try:
            response = requests.post(url, json=body)
            print(response)
        except:
            print("No connection to backend")
            return None
        return response.json()

    
local_request = RequestData("http://127.0.0.1:8000/")


# print(local_request.next())
