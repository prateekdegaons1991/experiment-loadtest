import requests
from requests.api import delete, request
import logging
from os import path
import pkg.utils.client.client as client
from kubernetes import client, config, watch
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
import time

class Application(object):
    def __init__(self):
        self.clients = client

      
	
    def CheckApplicationStatus(self, experimentsDetails):
        print(experimentsDetails.HOST)
        if experimentsDetails.HOST == "" or experimentsDetails.PATH1 == "" or experimentsDetails.PATH2 == "" or experimentsDetails.PATH3 == "" :
            return ValueError("Provided Application Endpoint or Paths are empty")

        err = self.checkAppStatus(experimentsDetails)
        if err != None:
            return err
        logging.info("[Info]: Application Endpoint status and sub paths of Application Endpoint has been checked")
    
        
    def checkAppStatus(self,experimentsDetails):

        try:
            response = requests.get(experimentsDetails.HOST)

            if ( response.status_code == 200):
                print("Application Endpoint is Healthy")
            #    response1 = requests.get(experimentsDetails.HOST+experimentsDetails.PATH1)
            #    response2 = requests.get(experimentsDetails.HOST+experimentsDetails.PATH2)
            #    response3 = requests.get(experimentsDetails.HOST+experimentsDetails.PATH3)
#
            #    if response1.status_code == 200 & response2.status_code == 200 & response3.status_code == 200 :
            #        print("Sub Path of Application Endpoint is Healthy")
            #    else:
            #        return("Sub Path of Application Endpoint is UnHealthy")
            
            else:
                return("Application Endpoint is Unhealthy")

        except Exception as exp:
            return ValueError(exp)

    def addLoad(self, experimentsDetails):

        err = self.createHelperPod(experimentsDetails)
        if err != None:
            return err
        logging.info("[Info]:Helper Pod is created")

    #checking the status of the helper pods, wait till the pod comes to running state else fail the experiment
        err = self.CheckPodStatus(experimentsDetails, 0, experimentsDetails.Timeout, experimentsDetails.Delay)
        if err != None:
            return err
        logging.info("[Info]:Helper Pod is Running")    

    
        
    
    def removeLoad(self, experimentsDetails):

        err = self.deleteHelperPod(experimentsDetails)
        if err != None:
            return err
        logging.info("[Info]:Helper Pod is deleted")
    

    def createHelperPod(self, experimentsDetails):

        config.load_kube_config()
        core_v1 = core_v1_api.CoreV1Api()
        #name = 'loadtest-4'
        resp = None
        #image = 'prateekdegaons/load-test:latest'
        
        try:
            resp = core_v1.read_namespaced_pod(name=experimentsDetails.Pod_Name,
                                                    namespace='default')
                                                
        except ApiException as e:
            if e.status != 404:
                print("Unknown error: %s" % e)
                exit(1)

        if not resp:
            print("Pod %s does not exist. Creating it..." % experimentsDetails.Pod_Name)
            pod_manifest = {
                'apiVersion': 'v1',
                'kind': 'Pod',
                'metadata': {
                    'name': experimentsDetails.Pod_Name
                },
                'spec': {
                    'containers': [{
                        'image': experimentsDetails.Image,
                        'name': experimentsDetails.Pod_Name,
                        'env': [
                            {'name': 'PATH1', 'value': experimentsDetails.PATH1},
                            {'name': 'PATH2', 'value': experimentsDetails.PATH2},
                            {'name': 'PATH3', 'value': experimentsDetails.PATH3},
                            {'name': 'HOST', 'value': experimentsDetails.HOST},
                            {'name': 'LOAD_FILE', 'value': experimentsDetails.LOAD_FILE}, 
                            {'name': 'SPAWN_RATE', 'value': experimentsDetails.SPAWN_RATE}, 
                            {'name': 'USERS', 'value': experimentsDetails.USERS},
                            {'name':'RUN_TIME', 'value': experimentsDetails.RUN_TIME},
                        ]
                        #"args": [
                        #    "/bin/sh",
                        #    "-c",
                        #    "while true;do date;sleep 5; done"
                        #]
                    }],
                    'restartPolicy': 'OnFailure',
                    'imagePullPolicy': 'Always'
                    
                }
            }
            resp = core_v1.create_namespaced_pod(body=pod_manifest,
                                                    namespace='default')
            
            while True:
                resp = core_v1.read_namespaced_pod(name=experimentsDetails.Pod_Name,
                                                        namespace='default')
                if resp.status.phase != 'Pending':
                    break
                time.sleep(1)
            print("Done.")
        else:
            print("pod already exist")

    # CheckPodStatus checks the running status of the application pod
    def CheckPodStatus(self,experimentsDetails,tries,timeout,delay):
        return self.CheckPodStatusPhase(experimentsDetails,tries,timeout,delay)

    def CheckPodStatusPhase(self,experimentsDetails, init, timeout, delay):

        config.load_kube_config()
        core_v1 = core_v1_api.CoreV1Api()

        try:
            resp = core_v1.read_namespaced_pod(name=experimentsDetails.Pod_Name,
                                                    namespace='default')
            
            if str(resp.status.phase) != 'Running':
                raise Exception("Pod is not yet in Running state") 

            logging.info("[status]: The status of Pods are as follows Pod : %s status : %s", resp.metadata.name, resp.status.phase)
			     

        except Exception as exp:
            if init > timeout:
                return ValueError(exp)
            time.sleep(delay)
            return self.CheckPodStatusPhase(experimentsDetails,init + delay, timeout, delay)
		    
	    
        return None

    def deleteHelperPod(self,experimentsDetails):
        GracePeriod=0
        try:
            config.load_kube_config()
            core_v1 = core_v1_api.CoreV1Api()
            logging.info("[Info]: Killing the following pods, PodName : %s", experimentsDetails.Pod_Name)
            if experimentsDetails.Force:
                core_v1.delete_namespaced_pod(name=experimentsDetails.Pod_Name,
                                                    namespace='default',grace_period_seconds=GracePeriod)
                print("Force deleting")
            else:
                core_v1.delete_namespaced_pod(name=experimentsDetails.Pod_Name,
                                                    namespace='default')

				
        except Exception as exp:
            return ValueError(exp)

    def CheckPodComplete(self,experimentsDetails, init, timeout, delay):

        config.load_kube_config()
        core_v1 = core_v1_api.CoreV1Api()

        try:
            resp = core_v1.read_namespaced_pod(name=experimentsDetails.Pod_Name,
                                                    namespace='default')
            
            if str(resp.status.phase) != 'Completed':
                raise Exception("Pod is not yet in Completed state") 

            logging.info("[status]: The status of Pods are as follows Pod : %s status : %s", resp.metadata.name, resp.status.phase)

        except Exception as exp:
            print("1")
            if init > timeout:
                return ValueError(exp)
            time.sleep(delay)
            return self.CheckPodComplete(experimentsDetails,init + delay, timeout, delay)
		    
	    
        return None








			
	


    


    #def addLoad(self, experimentsDetails):
    #    try:
    #        
    #        config.load_kube_config()
#
    #        with open(path.join(path.dirname(__file__), "load.yaml")) as f:
    #            dep = yaml.safe_load(f)
    #            k8s_apps_v1 = client.AppsV1Api()
    #            resp = k8s_apps_v1.create_namespaced_deployment(
    #                body=dep, namespace="default")
    #            print("Deployment created. status='%s'" % resp.metadata.name)
#
    #    except Exception as exp:
    #        return ValueError(exp)
#
#
    #    
#
    #    
    ##### Delete deployment
    #def removeLoad(self):
#
    #    try:
#
    #        config.load_kube_config()
    #        with open(path.join(path.dirname(__file__), "load.yaml")) as f:
    #            dep = yaml.safe_load(f)
    #            k8s_apps_v1 = client.AppsV1Api()
    #            k8s_apps_v1.delete_namespaced_deployment(name=dep["metadata"]["name"], namespace="default")
    #            print("Deployment deleted. status='%s'" % dep["metadata"]["name"])
    #            
    #    except Exception as exp:
    #        return ValueError(exp)
#
#
    #   
 

