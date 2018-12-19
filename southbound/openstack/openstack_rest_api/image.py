import json

import rest_requests
from openstack_config import image_url

# class Images(object):
#     """The class is about image in the cloud platform."""

    # def __init__():
    #     """Class flavors initialization."""
images_url = image_url + "/images"

def getImagesList():
    """Get list of images."""
    code, res = rest_requests.get(images_url)
    if code != 200:
        # TODO: log
        return None
    return res["images"]

def getImage(image_id):
    """Get a image."""
    code, res = rest_requests.get(images_url + "/" + image_id)
    if code != 200:
        # TODO: log
        return None
    return res

# def createImages(para_json):
#     """Create a Network."""
#     code, res = rest_requests.post(images_url, para_json)
#     if code != 201:
#         # TODO: log
#         return None
#     return res["network"]

def deleteImage(image_id):
    """Delete a Image."""
    code = rest_requests.get(images_url + "/" + image_id)
    if code != 204:
        # TODO: log
        return False
    return True