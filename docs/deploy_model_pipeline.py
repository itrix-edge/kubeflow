#!/usr/bin/env python3

import kfp
from kfp import dsl

def deployed_model_op(url, key):
    return dsl.ContainerOp(
        name='Deployed - Model',
        image='google/cloud-sdk:279.0.0',
        command=['sh', '-c'],
        arguments=['curl -X GET -k -v http://$0 | tee $2', url, key, '/tmp/results.txt'],
        file_outputs={
            'data': '/tmp/results.txt',
        }
    )

def echo2_op(text1):
    return dsl.ContainerOp(
        name='echo',
        image='library/bash:4.4.23',
        command=['sh', '-c'],
        arguments=['echo "Text 1: $0"', text1]
    )


@dsl.pipeline(
  name='Deployed pipeline',
  description='Trigger edge cluster to get model and prints the concatenated result.'
)
def download_and_join(
    url='',
    key='',
):

    deployed_task = deployed_model_op(url, key)

    echo_task = echo2_op(deployed_task.output)

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(download_and_join, __file__ + '.yaml')
