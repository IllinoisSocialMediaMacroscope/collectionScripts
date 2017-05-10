'''
Created on May 9, 2017

@author: npvance2
'''

import boto3

def main():
    # Enter file paths to images
    sourceImages = []
    # Your AWS tokens must be entered in you AWS config file and that account must have Rekognition permissions via IAM.
    client = boto3.client('rekognition')
    # Our source images
    for sourceImage in sourceImages:
        with open(sourceImage, 'rb') as source_image:
            source_bytes = source_image.read()
    
        response = client.detect_labels(Image={ 'Bytes': source_bytes },
                                        MaxLabels=5, #Max number of labels returned
                                        MinConfidence=75.0 #Minimum confidence of identification
        )
        print(sourceImage)
        for i in response['Labels']:
            label = i['Name']
            confidence = i['Confidence']
            if not label:
                label = ""
            if not confidence:
                confidence = 0.0
            print(label+" Detected "+str(confidence)+"% Match")
        print("")

if __name__ == '__main__':
    main()