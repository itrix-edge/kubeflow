
#  Torch serve

#### clone torchserve from source
```
git clone https://github.com/pytorch/serve.git
cd serve/docker
```
### install Torch-serve  and model-archiver on host
```
sudo apt install openjdk-11-jdk
conda create -n torchserve

source activate torchserve
conda install psutil pytorch torchvision torchtext -c pytorch
conda install cudatoolkit=10.1

git clone https://github.com/pytorch/serve.git
cd serve     
pip install .
cd model-archiver
pip install .
```

### use model-archiver on host to packae model and sevre
package model
```
torch-model-archiver --model-name densenet161_ts --version 1.0  --serialized-file densenet161.pt --extra-files examples/image_classifier/index_to_name.json --handler image_classifier
```
move to model_store
```
mkdir model_store
chmod 777 model_store
mv densenet161_ts.mar model_store/
```
start serving from host
```
torchserve --start --model-store model_store --models densenet161=densenet161_ts.mar
```
predict
```
curl http://localhost:8080/predictions/densenet161 -T examples/image_classifier/kitten.jpg
```
## Docker
#### creating docker image 

To enable docker BuildKit by default, set daemon configuration in /etc/docker/daemon.json feature to true and restart the daemon and restart docker:
```
{ "features": { "buildkit": true } }
```

CPU based :
```
DOCKER_BUILDKIT=1 docker build --file Dockerfile -t torchserve:latest .
```
GPU based :
```
DOCKER_BUILDKIT=1 docker build --file Dockerfile --build-arg BASE_IMAGE=nvidia/cuda:10.1-cudnn7-runtime-ubuntu18.04 -t torchserve:latest .
```

#### running torchserve 
CPU  based :
```
docker run --rm -it -p 8080:8080 -p 8081:8081 pytorch/torchserve:latest-cpu
```
GPU based :
```
docker run --rm -it --gpus '"device=1,2"' -p 8080:8080 -p 8081:8081 pytorch/torchserve:latest-gpu
```
###  how to use model-archiver in container to package model 
running torchserve and mount testdata 
```
cd /serve/examples/image_classifier
wget https://download.pytorch.org/models/densenet161-8d451a50.pth
```
```
docker run --rm -it -p 8080:8080 -p 8081:8081 --name mar -v /root/model-store:/home/model-server/model-store -v /root/serve/examples:/home/model-server/examples  pytorch/torchserve:0.1.1-cpu
```
enter the container
```
docker exec -ti <container> sh
```
use model-archiver to package model data
```
torch-model-archiver --model-name densenet161 --version 1.0 --model-file /home/model-server/examples/image_classifier/densenet_161/model.py --serialized-file /home/model-server/examples/image_classifier/densenet161-8d451a50.pth --export-path /home/model-server/model-store --extra-files /home/model-server/examples/image_classifier/index_to_name.json --handler image_classifier
```
start serving
```
torchserve --stop

torchserve --start --model-store model-store --models densenet161=densenet161.mar
```
here are a error about model snapshot
https://github.com/pytorch/serve/issues/383
To solve this error, add args (--no-config-snapshots)
```
torchserve --start --model-store model-store --models densenet161=densenet161.mar --no-config-snapshots
```
### docker run torchserve on production env

```
docker run --rm --shm-size=1g \
        --ulimit memlock=-1 \
        --ulimit stack=67108864 \
        -p8080:8080 \
        -p8081:8081 \
        --mount type=bind,source=/path/to/model/store,target=/tmp/models <container> torchserve --model-store=/tmp/models 
```

#### example inference
The following code completes all three steps:
```
curl -O https://s3.amazonaws.com/model-server/inputs/kitten.jpg
curl http://localhost:8080/predictions/densenet161 -T kitten.jpg
```
The predict endpoint returns a prediction response in JSON. It will look something like the following result:
```
[
  {
    "tiger_cat": 0.46933549642562866
  },
  {
    "tabby": 0.4633878469467163
  },
  {
    "Egyptian_cat": 0.06456148624420166
  },
  {
    "lynx": 0.0012828214094042778
  },
  {
    "plastic_bag": 0.00023323034110944718
  }
]
```



