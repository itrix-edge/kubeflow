# kubeflow
kubeflow for itrix-edge

## Create the InferenceService

Labeled kubeflow namespace before deploy the InferenceService
```
$ kubectl label namespace kubeflow serving.kubeflow.org/inferenceservice=enabled
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
```
MODEL_NAME=flowers-sample
INPUT_PATH=@./input.json
INGRESS_GATEWAY=istio-ingressgateway
CLUSTER_IP=$(kubectl -n istio-system get service $INGRESS_GATEWAY -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
SERVICE_HOSTNAME=$(kubectl get inferenceservice ${MODEL_NAME} -o jsonpath='{.status.url}' | cut -d "/" -f 3)

curl -v -H "Host: ${SERVICE_HOSTNAME}" http://$CLUSTER_IP/v1/models/$MODEL_NAME:predict -d $INPUT_PATH
```

