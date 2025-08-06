from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """return all pictures from the data list"""
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """return a picture by id"""
    picture = next((item for item in data if item["id"] == id), None)
    if picture:
        return jsonify(picture), 200
    else:
        return {"message": "picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """create a new picture"""
    picture = request.get_json()
    
    # Check if picture with same id already exists
    existing_picture = next((item for item in data if item["id"] == picture["id"]), None)
    if existing_picture:
        return {"Message": f"picture with id {picture['id']} already present"}, 302
    
    # Add the new picture to data
    data.append(picture)
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """update a picture by id"""
    picture_data = request.get_json()
    
    # Find the picture to update
    for i, picture in enumerate(data):
        if picture["id"] == id:
            data[i] = picture_data
            return jsonify(picture_data), 200
    
    # Picture not found
    return {"message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """delete a picture by id"""
    global data
    
    # Find and remove the picture
    for i, picture in enumerate(data):
        if picture["id"] == id:
            data.pop(i)
            return "", 204
    
    # Picture not found
    return {"message": "picture not found"}, 404
