# ExperimentDetails is for collecting all the experiment-related details
class ExperimentDetails(object):
	def __init__(self, ExperimentName=None, EngineName=None, ChaosDuration=None, ChaosInterval=None, RampTime=None, Force=None, ChaosLib=None, 
		ChaosServiceAccount=None,Pod_Name=None,Image=None,LOAD_FILE=None,RUN_TIME=None,SPAWN_RATE=None,USERS=None, HOST=None, PATH1=None, PATH2=None, PATH3=None, AppNS=None, AppLabel=None, ChaosInjectCmd=None, AppKind=None, InstanceID=None, ChaosNamespace=None, ChaosPodName=None, Timeout=None, 
		Delay=None, Sequence=None, LIBImagePullPolicy=None, TargetContainer=None, UID=None):
		self.ExperimentName      = ExperimentName 
		self.EngineName          = EngineName
		self.ChaosDuration       = ChaosDuration
		self.ChaosInterval       = ChaosInterval
		self.RampTime            = RampTime
		self.ChaosLib            = ChaosLib
		self.AppNS               = AppNS
		self.AppLabel            = AppLabel
		self.AppKind             = AppKind
		self.InstanceID          = InstanceID
		self.ChaosUID            = UID
		self.Timeout             = Timeout
		self.Delay               = Delay
		self.LIBImagePullPolicy  = LIBImagePullPolicy
		self.ChaosNamespace      = ChaosNamespace
		self.ChaosPodName        = ChaosPodName
		self.HOST                = HOST
		self.PATH1               = PATH1
		self.PATH2               = PATH2
		self.PATH3               = PATH3
		self.Image               = Image
		self.LOAD_FILE           = LOAD_FILE
		self.SPAWN_RATE          = SPAWN_RATE
		self.USERS               = USERS
		self.RUN_TIME            = RUN_TIME
		self.Pod_Name            = Pod_Name