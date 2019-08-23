import time
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
#from models import Biometric
import sys
## Enrolls new finger
##

def enroll(name):
    ## Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
        
        if ( f.verifyPassword() == False ):
            return {'error' : 'The given fingerprint sensor password is wrong!'}
        
    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        return {"error" : str(e)}
    
        ## Gets some sensor information
        print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

    ## Tries to enroll new finger
    try:
        print('Waiting for finger...')
        
        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass
        
        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)
            
        ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]

        if ( positionNumber >= 0 ):
            print('Template already exists at position #' + str(positionNumber))
            return {"error" : "Template already exists at position #" + str(positionNumber)}
            
        print('Remove finger...')
        time.sleep(2)
            
        print('Waiting for same finger again...')

        ## Wait that finger is read again
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(0x02)

        ## Compares the charbuffers
        if ( f.compareCharacteristics() == 0 ):
            return {'error' : 'Fingers do not match'}
        
        ## Creates a template
        f.createTemplate()

        ## Saves template at new position number
        positionNumber = f.storeTemplate()
        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))
        
        ## Loads the found template to charbuffer 1
        f.loadTemplate(positionNumber, 0x01)

        ## Downloads the characteristics of template loaded in charbuffer 1
        characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
        ## Hashes characteristics of template
        credential_hash = hashlib.sha256(characterics).hexdigest()
        return {"error" : None, "pos" :str(positionNumber), "cred_hash" : credential_hash }
    except Exception as e:
        print('Operation failed.. Exception message: ' + str(e))
        return {"error" : str(e)}

def search_person():
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            return {'error' : 'The given fingerprint sensor password is wrong!'}

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        return {"error" : + str(e)}

        ## Gets some sensor information
    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

    ## Tries to search the finger and calculate hash
    try:
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

        ## Searchs template
        result = f.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if ( positionNumber == -1 ):
            return {"error" : "No match found!"}
        else:
            print('Found template at position #' + str(positionNumber))
        ## OPTIONAL stuff
        ##
        
        ## Loads the found template to charbuffer 1
        f.loadTemplate(positionNumber, 0x01)

        ## Downloads the characteristics of template loaded in charbuffer 1
        characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

        ## Hashes characteristics of template
        print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())
        return {"error" : None, "pos" : str(positionNumber), "accuracy_score" : str(accuracyScore)}
    except Exception as e:
        print('Operation failed!')
        return {"error" : str(e)}

def delete_person(position_number):
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
        
        if ( f.verifyPassword() == False ):
            return {"error" : "The given fingerprint sensor password is wrong!"}
        
    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        return {"error" : str(e)}

    ## Gets some sensor information
    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

    ## Tries to delete the template of the finger
    try:
        positionNumber = position_number

        if ( f.deleteTemplate(positionNumber) == True ):
            print('Template deleted!')
            return {"error" : None}

    except Exception as e:
        print('Exception message: ' + str(e))
        return {"error": str(e)}
