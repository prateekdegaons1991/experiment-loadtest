
import os
import pkg.types.types as types
import pkg.maths.maths as maths

#GetENV fetches all the env variables from the runner pod
def GetENV(experimentsDetails):
	experimentsDetails.ExperimentName =  os.getenv("EXPERIMENT_NAME", "load-test-chaos")
	experimentsDetails.ChaosNamespace = os.getenv("CHAOS_NAMESPACE", "litmus")
	experimentsDetails.EngineName = os.getenv("CHAOSENGINE", "")
	experimentsDetails.ChaosDuration = maths.atoi(os.getenv("TOTAL_CHAOS_DURATION", "30"))
	experimentsDetails.ChaosInterval = os.getenv("CHAOS_INTERVAL", "120")
	experimentsDetails.RampTime = maths.atoi(os.getenv("RAMP_TIME", "0"))
	experimentsDetails.ChaosLib = os.getenv("LIB", "litmus")
	experimentsDetails.AppNS = os.getenv("APP_NAMESPACE", "")
	experimentsDetails.AppLabel = os.getenv("APP_LABEL", "")
	experimentsDetails.AppKind = os.getenv("APP_KIND", "")
	experimentsDetails.ChaosUID = os.getenv("CHAOS_UID", "")
	experimentsDetails.InstanceID = os.getenv("INSTANCE_ID", "")
	experimentsDetails.ChaosPodName = os.getenv("POD_NAME", "")
	experimentsDetails.Force = (os.getenv("FORCE", "false") == 'false')
	experimentsDetails.Delay = maths.atoi(os.getenv("STATUS_CHECK_DELAY", "3"))
	experimentsDetails.Timeout = maths.atoi(os.getenv("STATUS_CHECK_TIMEOUT", "240"))
	experimentsDetails.TargetPods = os.getenv("TARGET_PODS", "")
	experimentsDetails.PodsAffectedPerc = maths.atoi(os.getenv("PODS_AFFECTED_PERC", "0"))
	experimentsDetails.Sequence = os.getenv("SEQUENCE", "parallel")
	experimentsDetails.HOST = os.getenv("HOST","https://prateeks-blog.herokuapp.com")
	experimentsDetails.PATH1 = os.getenv("PATH1", "/about")
	experimentsDetails.PATH2 = os.getenv("PATH2", "/register")
	experimentsDetails.PATH3 = os.getenv("PATH3", "/")
	experimentsDetails.Image = os.getenv("Image","prateekdegaons/load-test:latest")
	experimentsDetails.LOAD_FILE= os.getenv("LOAD_FILE","/config/locustfile.py")
	experimentsDetails.SPAWN_RATE= os.getenv("SPAWN_RATE","100")
	experimentsDetails.USERS = os.getenv("USERS", "1000")
	experimentsDetails.RUN_TIME = os.getenv("RUN_TIME", "1m")
	experimentsDetails.Pod_Name = os.getenv("LOAD_POD_NAME", "loadtest")


#InitialiseChaosVariables initialise all the global variables
def InitialiseChaosVariables(chaosDetails, experimentsDetails):
	appDetails = types.AppDetails()
	appDetails.AnnotationCheck = (os.getenv("ANNOTATION_CHECK", "false") == 'true')
	appDetails.AnnotationKey = os.getenv("ANNOTATION_KEY", "litmuschaos.io/chaos")
	appDetails.AnnotationValue = "true"
	appDetails.Kind = experimentsDetails.AppKind
	appDetails.Label = experimentsDetails.AppLabel
	appDetails.Namespace = experimentsDetails.AppNS

	chaosDetails.ChaosNamespace = experimentsDetails.ChaosNamespace
	chaosDetails.ChaosPodName = experimentsDetails.ChaosPodName
	chaosDetails.ChaosUID = experimentsDetails.ChaosUID
	chaosDetails.EngineName = experimentsDetails.EngineName
	chaosDetails.ExperimentName = experimentsDetails.ExperimentName
	chaosDetails.InstanceID = experimentsDetails.InstanceID
	chaosDetails.Timeout = experimentsDetails.Timeout
	chaosDetails.Delay = experimentsDetails.Delay
	chaosDetails.AppDetail = appDetails
	chaosDetails.Randomness = (os.getenv("RANDOMNESS", "false") == 'true')
