import logging
import os
import boto3
from .aws_rekognition import start_model, stop_model

logger = logging.getLogger("artitone_rekognition")


def detect_labels(bytes):
    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_S3_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_S3_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_S3_REGION_NAME"),
    )

    project_arn = os.getenv("AWS_REKOGNITION_PROJECT_ARN")
    texture_model_arn = os.getenv("AWS_REKOGNITION_MODEL_ARN")
    version_name = os.getenv("AWS_REKOGNITION_VERSION_NAME")
    min_inference_units = 1
    # start_model(session, project_arn, model_arn, version_name, min_inference_units)

    client = session.client("rekognition")
    texture_response = client.detect_custom_labels(
        Image={
            "Bytes": bytes,
            # 'S3Object': {'Bucket': bucket, 'Name': photo}
        },
        ProjectVersionArn=texture_model_arn,
    )

    # stop_model(session, model_arn)
    texture = texture_response["CustomLabels"][0]["Name"]
    labels = []
    # for label in texture_response['CustomLabels']:
    #     labels.append(label['Name'])
    #     logger.debug(f"Label: {label['Name']} ({label['Confidence']})")

    return texture, labels
