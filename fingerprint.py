import time
import sys
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
from display import Sender


class Fingerprint:

    @classmethod
    def _get_sensor(cls):
        if not hasattr(cls, '_sensor'):
            cls._sensor = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
            cls._lcd = Sender()
        return cls._sensor, cls._lcd
    
    def __init__(self):
        try:
            self.sensor, self.lcd = self._get_sensor()
        
            if ( self.sensor.verifyPassword() == False ):
                return {'error' : 'The given fingerprint sensor password is wrong!'}
        
        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            return {"error" : 'The fingerprint sensor could not be initialized!'}

    def search_record(self):
        try:
            print('Waiting for finger...')
            self.lcd.set("Waiting for finger",1)
            while ( self.sensor.readImage() == False ):
                pass
            self.sensor.convertImage(0x01)
            result = self.sensor.searchTemplate()
            positionNumber = result[0]
            accuracyScore = result[1]
            if ( positionNumber == -1 ):
                self.lcd.set("No match found!!!!!",1)
                return {"error" : "No match found!!!!!"}
            else:
                print('Found template at position #' + str(positionNumber))
                self.sensor.loadTemplate(positionNumber, 0x01)
                characterics = str(self.sensor.downloadCharacteristics(0x01)).encode('utf-8')
                print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())
                self.lcd.set("Found template at " + str(positionNumber),1)
                return {"error" : None, "pos" : str(positionNumber), "accuracy_score" : str(accuracyScore)}
        except Exception as e:
            print('Operation failed!')
            self.lcd.set('Operation failed !!!!!!!', 1)
            return {"error" : str(e)}


    def enroll(self):
        print('Currently used templates: ' + str(self.sensor.getTemplateCount()) +'/'+ str(self.sensor.getStorageCapacity()))
        try:
            print('Waiting for finger...')
            self.lcd.set("Waiting for finger..",1) 
            while ( self.sensor.readImage() == False ):
                pass
            self.sensor.convertImage(0x01)
            result = self.sensor.searchTemplate()
            positionNumber = result[0]
            if ( positionNumber >= 0 ):
                print('Template already exists at position #' + str(positionNumber))
                return {"error" : "Template already exists at position #" + str(positionNumber)}
            print('Remove finger...')
            self.lcd.set("Remove finger ......",1)
            time.sleep(2)
            print('Waiting for same finger again...')
            self.lcd.set("Waiting for same ",1)
            self.lcd.set("finger again ...", 2)
            while ( self.sensor.readImage() == False ):
                pass
            self.sensor.convertImage(0x02)
            if ( self.sensor.compareCharacteristics() == 0 ):
                self.lcd.set("Fingers do not match !", 1)
                return {'error' : 'Fingers do not match'}
            self.sensor.createTemplate()
            positionNumber = self.sensor.storeTemplate()
            print('Finger enrolled successfully!')
            self.lcd.set("Finger enrolled successfully!", 1)
            self.lcd.set("successfully!", 2)
            print('New template position #' + str(positionNumber))
            self.sensor.loadTemplate(positionNumber, 0x01)
            characterics = str(self.sensor.downloadCharacteristics(0x01)).encode('utf-8')
            credential_hash = hashlib.sha256(characterics).hexdigest()
            return {"error" : None, "pos" :str(positionNumber), "cred_hash" : credential_hash }
        except Exception as e:
            print('Operation failed.. Exception message: ' + str(e))
            return {"error" : 'Operation failed !!!'}
        
    def delete_record(self, position_number):
        print('Currently used templates: ' + str(self.sensor.getTemplateCount()) +'/'+ str(self.sensor.getStorageCapacity()))
        try:
            if ( self.sensor.deleteTemplate(position_number) == True ):
                print('Template deleted!')
                return {"error" : None}
        except Exception as e:
            print('Exception message: ' + str(e))
            return {"error": str(e)}

def execute_sensor():
    finger_obj = Fingerprint()
    return finger_obj
