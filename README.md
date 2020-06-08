# kubeflow
kubeflow for itrix-edge

## Run a prediction
```
MODEL_NAME=flowers-sample
INPUT_PATH=@./input.json
INGRESS_GATEWAY=istio-ingressgateway
CLUSTER_IP=$(kubectl -n istio-system get service $INGRESS_GATEWAY -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
SERVICE_HOSTNAME=$(kubectl get inferenceservice ${MODEL_NAME} -o jsonpath='{.status.url}' | cut -d "/" -f 3)

curl -v -H "Host: ${SERVICE_HOSTNAME}" http://$CLUSTER_IP/v1/models/$MODEL_NAME:predict -d $INPUT_PATH
```

## Deploying Kubeflow with Ksonnet

Initialize a Ksonnet app. Set the namespace for its default environment.
```
NAMESPACE=kubeflow
kubectl create namespace ${NAMESPACE}

APP_NAME=my-kubeflow
ks init ${APP_NAME}
cd ${APP_NAME}
ks env set default --namespace ${NAMESPACE}
```
Install Kubeflow components
```
export GITHUB_TOKEN=99510f2ccf40e496d1e97dbec9f31cb16770b884
ks registry add kubeflow github.com/katacoda/kubeflow-ksonnet/tree/master/kubeflow
ks pkg install kubeflow/argo
ks pkg install kubeflow/core
ks pkg install kubeflow/seldon
ks pkg install kubeflow/tf-serving
```
Create templates for core components
```
ks generate kubeflow-core kubeflow-core --namespace=kubeflow
```
Deploy Kubeflow
```
ks apply default -c kubeflow-core
kubectl apply -f ~/kubeflow.yaml -n kubeflow
```
view status
```
kubectl get pods -n kubeflow
NAME                                                           READY   STATUS      RESTARTS   AGE
admission-webhook-bootstrap-stateful-set-0                     1/1     Running     0          24m
admission-webhook-deployment-64cb96ddbf-29k25                  1/1     Running     0          23m
application-controller-stateful-set-0                          1/1     Running     0          24m
argo-ui-778676df64-x8wtl                                       1/1     Running     0          24m
centraldashboard-cc58bf567-2qnww                               1/1     Running     0          23m
jupyter-web-app-deployment-89789fd5-xjwxb                      1/1     Running     0          24m
katib-controller-6b789b6cb5-8zcq6                              1/1     Running     1          24m
katib-db-manager-64f548b47c-f5h7h                              1/1     Running     1          24m
katib-mysql-57884cb488-zf8xd                                   1/1     Running     0          24m
katib-ui-5c5cc6bd77-nqtmm                                      1/1     Running     0          24m
kfserving-controller-manager-0                                 2/2     Running     2          24m
metacontroller-0                                               1/1     Running     0          24m
metadata-db-76c9f78f77-jmqtr                                   1/1     Running     0          24m
metadata-deployment-674fdd976b-jt7bm                           1/1     Running     0          24m
metadata-envoy-deployment-5688989bd6-2xsvd                     1/1     Running     0          24m
metadata-grpc-deployment-5579bdc87b-8crrq                      1/1     Running     1          24m
metadata-ui-9b8cd699d-5jmkq                                    1/1     Running     0          24m
minio-755ff748b-2jtls                                          1/1     Running     0          24m
ml-pipeline-79b4f85cbc-56tcd                                   1/1     Running     0          24m
ml-pipeline-ml-pipeline-visualizationserver-5fdffdc5bf-lf646   1/1     Running     0          24m
ml-pipeline-persistenceagent-645cb66874-fb8xz                  1/1     Running     1          24m
ml-pipeline-scheduledworkflow-6c978b6b85-nfmq8                 1/1     Running     0          24m
ml-pipeline-ui-6995b7bccf-md9qg                                1/1     Running     0          24m
ml-pipeline-viewer-controller-deployment-8554dc7b9f-vwzmg      1/1     Running     1          24m
mysql-598bc897dc-94dm8                                         1/1     Running     0          24m
notebook-controller-deployment-7db57b9ccf-4hzv2                1/1     Running     1          24m
profiles-deployment-5d87dd4f87-4f26h                           2/2     Running     0          24m
pytorch-operator-5fd5f94bdd-nkc7b                              1/1     Running     0          24m
seldon-controller-manager-679fc777cd-7n4hz                     1/1     Running     0          24m
spark-operatorcrd-cleanup-gxmdf                                0/2     Completed   4          24m
spark-operatorsparkoperator-c7b64b87f-k4g74                    1/1     Running     0          24m
spartakus-volunteer-6b767c8d6-85z4n                            1/1     Running     0          24m
tensorboard-6544748d94-4mr5h                                   1/1     Running     0          24m
tf-job-operator-7d7c8fb8bb-fcq8v                               1/1     Running     0          24m
workflow-controller-945c84565-rgpqq                            1/1     Running     0          24m
```
