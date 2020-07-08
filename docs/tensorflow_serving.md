# tensorflow serving 

download image
```
docker pull tensorflow/serving:latest
```
### download example models from source
```
git clone https://github.com/tensorflow/serving
```

### Start TensorFlow Serving container and open the REST API port
```
docker run -p 8501:8501 --mount type=bind,source="pwd"/serving/tensorflow_serving/servables/tensorflow/testdata/saved_model_half_plus_two_cpu,target=/models/half_plus_two -e MODEL_NAME=half_plus_two -t tensorflow/serving &
```

### Query the model using the predict API
```
curl -d '{"instances": [1.0, 2.0, 5.0]}' -X POST http://localhost:8501/v1/models/half_plus_two:predict
```
### Returns 
```
{ "predictions": [2.5, 3.0, 4.5] }
```
