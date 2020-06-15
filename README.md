# kubeflow
kubeflow for itrix-edge

## Create the InferenceService

Labeled kubeflow namespace before deploy the InferenceService
```
$ kubectl label namespace kfserving-test serving.kubeflow.org/inferenceservice=enabled
```
Apply the CRD
```
$ kubectl apply -f tensorflow.yaml -n kubeflow
```
Expected Output
```
inferenceservice.serving.kubeflow.org/flowers-sample configured
```

## Kfserving run a prediction

Convert the test picture test.png to base64
```
$ cat test.png | base64  #Copy the result to the value of base64 in input.json below
```
Save the following file as input.json
```
{
    "instances": [
        {
            "image_bytes": {
                "b64": "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAABC0lEQVR4nGNgGHCg0/NvOw8Oudqnf//+dcQq5bLk5j+g5OMlfphyDt/+/v33dxtQehuGrMcHoPA/F9FNX//+/WyCJvfi798f9714GRjKgYp8USUfAIUawCyVa3//vrBAkmJb+Pvv3xIWCEcNqC4DSbIJaGYDVI6BfRGKpMrNv3/vI7htf/8eQPAu//t3XwfBbf//7z+cEw70oTmSJUCdf+Gcor9/v0njkgQGWiuSXNh+YCAhSX4QgLFZvSuAQfTBEy455e/PXDEQQ0h+1o6/ILAPYU4mkHurDQjO/gNL/a2TQUiyXfkLBf9BxKcQRiQXMBjOg0q+uXC8cQlalDCwZ7z5+3fJoww7hoEGAMUNp28BRiGTAAAAAElFTkSuQmCC"
            }
        }
    ]
}
```

prediction
```
MODEL_NAME=flowers-sample
INPUT_PATH=@./input.json
INGRESS_GATEWAY=istio-ingressgateway
CLUSTER_IP=$(kubectl -n istio-system get service $INGRESS_GATEWAY -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
SERVICE_HOSTNAME=$(kubectl get inferenceservice ${MODEL_NAME} -o jsonpath='{.status.url}' | cut -d "/" -f 3)

curl -v -H "Host: ${SERVICE_HOSTNAME}" http://$CLUSTER_IP/v1/models/$MODEL_NAME:predict -d $INPUT_PATH
```
## Install Kfserving independent
```
git clone https://github.com/kubeflow/kfserving.git
```
```
TAG=v0.3.0
$ kubectl apply -f ./install/$TAG/kfserving.yaml
```
Test KFServing Installation
```
kubectl get po -n kfserving-system
NAME                             READY   STATUS    RESTARTS   AGE
kfserving-controller-manager-0   2/2     Running   2          13m
```

