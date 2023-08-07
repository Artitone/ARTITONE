import boto3

def start_model(session, project_arn, model_arn, version_name, min_inference_units):

    client=session.client('rekognition')

    try:
        # Start the model
        print('Starting model: ' + model_arn)
        response=client.start_project_version(ProjectVersionArn=model_arn, MinInferenceUnits=min_inference_units)
        # Wait for the model to be in the running state
        project_version_running_waiter = client.get_waiter('project_version_running')
        project_version_running_waiter.wait(ProjectArn=project_arn, VersionNames=[version_name])

        #Get the running status
        describe_response=client.describe_project_versions(ProjectArn=project_arn,
            VersionNames=[version_name])
        for model in describe_response['ProjectVersionDescriptions']:
            print("Status: " + model['Status'])
            print("Message: " + model['StatusMessage']) 
    except Exception as e:
        print(e)
        
    print('Model Start...')
    # project_arn='arn:aws:rekognition:us-east-1:141376400952:project/artitone_labeller/1690734433420'
    # model_arn='arn:aws:rekognition:us-east-1:141376400952:project/artitone_labeller/version/artitone_labeller.2023-08-03T17.54.34/1691099674800'
    # min_inference_units=1 
    # version_name='artitone_labeller.2023-08-03T17.54.34'
    # start_model(project_arn, model_arn, version_name, min_inference_units)


def stop_model(session, model_arn):

    client=session.client('rekognition')

    print('Stopping model:' + model_arn)

    #Stop the model
    try:
        response=client.stop_project_version(ProjectVersionArn=model_arn)
        status=response['Status']
        print ('Status: ' + status)
    except Exception as e:  
        print(e)  

    print('Model Stopped...')