
import pkg.types.types  as types
import pkg.events.events as events
import logging, threading, signal, sys
import pkg.utils.common.common as common
import pkg.utils.common.pods as pods
import pkg.utils.exec.exec as litmusexec
import pkg.types.types  as types
import pkg.events.events as events
import logging
import pkg.utils.common.common as common
import pkg.utils.common.pods as pods
from datetime import datetime
import pkg.status.application as status
import pkg.maths.maths as maths

# signal object
class Signals(object):
	def __init__(self, timeSignal=None, sigSignal=None):
		self.timeSignal = timeSignal
		self.sigSignal = sigSignal




#PrepareLoadTest contains the prepration steps before chaos injection
def PrepareLoadTestExperiment(experimentsDetails , resultDetails, eventsDetails, chaosDetails, clients, statusApp):

	#Waiting for the ramp time before chaos injection
	if experimentsDetails.RampTime != 0 :
		logging.info("[Ramp]: Waiting for the %s ramp time before injecting chaos",experimentsDetails.RampTime)
		common.WaitForDuration(experimentsDetails.RampTime)
	# mode for chaos injection
	if experimentsDetails.Sequence.lower() == "serial":
		err = injectChaosInSerialMode(experimentsDetails, chaosDetails, eventsDetails, resultDetails, clients, statusApp)
		if err != None:
			return err
	elif experimentsDetails.Sequence.lower() == "parallel":
		err = injectChaosInParallelMode(experimentsDetails, chaosDetails, eventsDetails, resultDetails, clients, statusApp)
		if err != None:
			return err
	else:
		return ValueError("{} sequence is not supported".format(experimentsDetails.Sequence))

	#Waiting for the ramp time after chaos injection
	if experimentsDetails.RampTime != 0 :
		logging.info("[Ramp]: Waiting for the %s ramp time after injecting chaos",experimentsDetails.RampTime)
		common.WaitForDuration(experimentsDetails.RampTime)

	return None

# injectChaosInSerialMode delete the target application pods serial mode(one by one)
def injectChaosInSerialMode(experimentsDetails , chaosDetails , eventsDetails , resultDetails, clients, statusApp): 
			
	#ChaosStartTimeStamp contains the start timestamp, when the chaos injection begin
	ChaosStartTimeStamp = datetime.now()
	duration = (datetime.now() - ChaosStartTimeStamp).seconds
	
	while duration < experimentsDetails.ChaosDuration:
		# Get the target pod details for the chaos execution
		# if the target pod is not defined it will derive the random target pod list using pod affected percentage
		logging.info("[Info]: Application Endpoint is , %s", experimentsDetails.HOST)
		
		
		if experimentsDetails.EngineName != "" :
			msg = "Injecting " + experimentsDetails.ExperimentName + " chaos on application pod"
			types.SetEngineEventAttributes(eventsDetails, types.ChaosInject, msg, "Normal", chaosDetails)
			events.GenerateEvents(eventsDetails, chaosDetails, "ChaosEngine", clients)
		
		#Adding load to the Application by creating a deployment

		logging.info("[Info]: Adding Load to the Application  : %s", experimentsDetails.HOST)
		err = statusApp.addLoad(experimentsDetails)
		if err != None:
			return err

		if chaosDetails.Randomness:
			err = common.RandomInterval(experimentsDetails.ChaosInterval)
			if err != None:
				return err
        		
		else:
			#Waiting for the chaos interval after chaos injection
			if experimentsDetails.ChaosInterval != "":
				logging.info("[Wait]: Wait for the chaos interval %s",(experimentsDetails.ChaosInterval))
				waitTime = maths.atoi(experimentsDetails.ChaosInterval)
				common.WaitForDuration(waitTime)
        
		

        # Removing load from Application --- Deleting a deployment
		logging.info("[Status]: Remove Load from Application")
		err = statusApp.removeLoad(experimentsDetails)
		if err != None:
			return err

		#Verify the status of pod after the chaos injection
		
	
		logging.info("[Status]: Checking Application status")		
		err = statusApp.CheckApplicationStatus(experimentsDetails)
		if err != None:
			return err
			
		
		duration = (datetime.now() - ChaosStartTimeStamp).seconds

	logging.info("[Completion]: %s chaos is done",(experimentsDetails.ExperimentName))

	return None

# injectChaosInParallelMode delete the target application pods in parallel mode (all at once)
def injectChaosInParallelMode(experimentsDetails , chaosDetails , eventsDetails , resultDetails, clients, statusApp):
	
	
	#ChaosStartTimeStamp contains the start timestamp, when the chaos injection begin
	ChaosStartTimeStamp = datetime.now()
	duration = (datetime.now() - ChaosStartTimeStamp).seconds
	
	while duration < experimentsDetails.ChaosDuration:
		# Get the target pod details for the chaos execution
		# if the target pod is not defined it will derive the random target pod list using pod affected percentage
		logging.info("[Info]: Application Endpoint is , %s", experimentsDetails.HOST)
		
		if experimentsDetails.EngineName != "" :
			msg = "Injecting " + experimentsDetails.ExperimentName + " chaos on application pod"
			types.SetEngineEventAttributes(eventsDetails, types.ChaosInject, msg, "Normal", chaosDetails)
			events.GenerateEvents(eventsDetails, chaosDetails, "ChaosEngine",clients)
		
		#Deleting the application pod
		logging.info("[Info]: Adding Load to the Application  : %s", experimentsDetails.HOST)
		err = statusApp.addLoad(experimentsDetails)
		if err != None:
			return err

		if chaosDetails.Randomness:
			err = common.RandomInterval(experimentsDetails.ChaosInterval)
			if err != None:
				return err
        		
		else:
			#Waiting for the chaos interval after chaos injection
			if experimentsDetails.ChaosInterval != "":
				logging.info("[Wait]: Wait for the chaos interval %s",(experimentsDetails.ChaosInterval))
				waitTime = maths.atoi(experimentsDetails.ChaosInterval)
				common.WaitForDuration(waitTime)

        # Removing load from Application --- Deleting a deployment
		logging.info("[Status]: Remove Load from Application")
		err = statusApp.removeLoad(experimentsDetails)
		if err != None:
			return err

		
		#Verify the status of pod after the chaos injection
		logging.info("[Status]: Checking Application status")		
		err = statusApp.CheckApplicationStatus(experimentsDetails)
		if err != None:
			return err

		duration = (datetime.now() - ChaosStartTimeStamp).seconds

	logging.info("[Completion]: %s chaos is done",(experimentsDetails.ExperimentName))

	return None


