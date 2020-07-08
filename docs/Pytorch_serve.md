
#  Torch serve

1. clone torchserve from source
```
git clone https://github.com/pytorch/serve.git
cd serve/docker
```
2. creating image 

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

3. running torchserve 
CPU  based :
```
docker run --rm -it -p 8080:8080 -p 8081:8081 pytorch/torchserve:latest-cpu
```
GPU based :
```
docker run --rm -it --gpus '"device=1,2"' -p 8080:8080 -p 8081:8081 pytorch/torchserve:latest-gpu
```

4. example inference
The following code completes all three steps:
```
curl -O https://s3.amazonaws.com/model-server/inputs/kitten.jpg
curl http://127.0.0.1:8080/predictions/densenet161 -T kitten.jpg
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
actually result
```
root@k8s-worker-r530:~# curl http://127.0.0.1:8080/predictions/densenet161 -T kitten.jpg
{
  "code": 404,
  "type": "ModelNotFoundException",
  "message": "Model not found: densenet161"
}
```

5. how to use a model
