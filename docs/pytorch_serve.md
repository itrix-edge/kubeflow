
##  using pytorch serve

1. clone torchserve source
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
