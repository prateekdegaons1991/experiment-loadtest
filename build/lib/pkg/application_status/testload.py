def open_pod(self, cmd: list, 
                pod_name: str, 
                namespace: str='bots', 
                image: str=f'{repository}:{tag}', 
                restartPolicy: str='Never', 
                serviceAccountName: str='bots-service-account'):
    '''
    This method launches a pod in kubernetes cluster according to command
    '''
    
    api_response = None
    try:
        api_response = self.core_v1.read_namespaced_pod(name=pod_name,
                                                        namespace=namespace)
    except ApiException as e:
        if e.status != 404:
            print("Unknown error: %s" % e)
            exit(1)
    if not api_response:
        print(f'From {os.path.basename(__file__)}: Pod {pod_name} does not exist. Creating it...')
        # Create pod manifest
        pod_manifest = {
            'apiVersion': 'v1',
            'kind': 'Pod',
            'metadata': {
                'labels': {
                    'bot': current-bot
                },
                'name': pod_name
            },
            'spec': {
                'containers': [{
                    'image': image,
                    'pod-running-timeout': '5m0s',
                    'name': f'container',
                    'args': cmd,
                    'env': [
                        {'name': 'env_variable', 'value': env_value},
                    ]
                }],
                # 'imagePullSecrets': client.V1LocalObjectReference(name='regcred'), # together with a service-account, allows to access private repository docker image
                'restartPolicy': restartPolicy,
                'serviceAccountName': bots-service-account
            }
        }
        
        print(f'POD MANIFEST:\n{pod_manifest}'
        api_response = self.core_v1.create_namespaced_pod(body=pod_manifest,                                                          namespace=namespace
        while True:
            api_response = self.core_v1.read_namespaced_pod(name=pod_name,
                                                            namespace=namespace)
            if api_response.status.phase != 'Pending':
                break
            time.sleep(0.01)
        
        print(f'From {os.path.basename(__file__)}: Pod {pod_name} in {namespace} created.')
        return pod_name