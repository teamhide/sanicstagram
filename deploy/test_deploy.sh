#!/bin/bash
echo "[*] Deploy Start"
latest_task=`aws ecs list-task-definitions --family-prefix ue-task | grep arn | tail -n 1 | sed 's/"//g' | awk -F ":" '{print $7}' `
appspec='{
  "version": 1,
  "Resources": [
    {
      "TargetService": {
        "Type": "AWS::ECS::Service",
        "Properties": {
          "TaskDefinition": "TASK_DEFINITION_ADDR/TASK_DEFINITION_NAME:'${latest_task}'",
          "LoadBalancerInfo": {
            "ContainerName": "CONTAINER_NAME",
            "ContainerPort": CONTAINER_PORT
          }
        }
      }
    }
  ]
}'
echo $appspec > ${PWD}/deploy/test_appspec.yaml
echo "[*] Create appspec.yaml"
sleep 1
aws s3 cp ./deploy/test_appspec.yaml s3://S3_ADDR/appspec.yaml
echo "[*] Upload appspec.yaml to S3 Done"
sleep 3
aws deploy \
create-deployment \
--application-name CODEDEPLOY_APPLICATION_NAME \
--deployment-group-name CODEDEPLOY_GROUP_NAME \
--s3-location bucket=charmy-test,bundleType=yaml,key=appspec.yaml
echo "[*] Deploy Done"