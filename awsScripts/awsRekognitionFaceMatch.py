'''
Created on May 9, 2017

@author: npvance2
'''
import boto3

SIMILARITY_THRESHOLD = 0.0

def main():
    # Your AWS tokens must be entered in you AWS config file and that account must have Rekognition enabled via IAM.
    client = boto3.client('rekognition')
    #Enter Path for image to be compared against
    sourceImage = ""
    #Enter images to be compared into list
    imageCompareArray = [""]
    for image in imageCompareArray:
        # Our source image
        with open(sourceImage, 'rb') as source_image:
            source_bytes = source_image.read()
    
        # Our target image
        with open(image, 'rb') as target_image:
            target_bytes = target_image.read()
    
        response = client.compare_faces(
                       SourceImage={ 'Bytes': source_bytes },
                       TargetImage={ 'Bytes': target_bytes },
                       SimilarityThreshold=SIMILARITY_THRESHOLD
        )
        print(sourceImage+" vs "+image)
        for i in response['FaceMatches']:
            simScore = i['Similarity']
            if not simScore:
                simScore = 0.0
            print(str(simScore)+"% Match")

if __name__ == '__main__':
    main()