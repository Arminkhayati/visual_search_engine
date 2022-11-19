# Visual Search Engine

A visual search engine powered by **YOLO v3** and **fastapi**.
In this project, a text-based description is received from users and the images that match that description are retrieved and displayed in the order of priority. That is what we do with Google to find the images we want but in more simple manner in our case.

Code uses tensorflow 2.x and the base model is taken from this [repository](https://github.com/anushkadhiman/YOLOv3-TensorFlow-2.x).

## Installation

First, clone or download this GitHub repository: 
```
git clone https://github.com/Arminkhayati/visual_search_engine.git
cd visual_search_engine
````
then prepare the environment:
```
pip install -r ./requirements.txt
`````
or

```
conda env create -f environment.yml
`````

Then download weights and place them in this directory `vse/model/model_data`:

```
# yolov3
wget https://pjreddie.com/media/files/yolov3.weights

# yolov3-tiny
wget https://pjreddie.com/media/files/yolov3-tiny.weights
``````

## Running code

To run the server just activate your environment then run this command:

For testing:
```
uvicorn main:app --reload
``````


For mannually running server:
```
uvicorn main:app --host 0.0.0.0 --port 80
``````

