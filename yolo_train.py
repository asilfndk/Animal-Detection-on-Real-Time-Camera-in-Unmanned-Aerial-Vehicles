#IMPORT ANIMAL DRONE DATASET FROM ROBOFLOW

from roboflow import Roboflow

rf = Roboflow(api_key="lpnLA6gQ9PQq5C0pGjuV")
project = rf.workspace("dog-pictures").project("safari-animals")
version = project.version(1)
dataset = version.download("yolov8")

#TRAIN YOLO MODEL

from ultralytics import YOLO

# Load a model
model = YOLO('yolov8m.pt')  # load a pretrained model (recommended for training)

# Use the model
results = model.train(data='safari-animals-1/data.yaml', epochs=30)  # train the model
results = model.val()  # evaluate model performance on the validation set