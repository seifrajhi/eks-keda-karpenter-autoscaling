
# EKS Keda Karpenter Autoscaling

This repository is a proof-of-concept implementation that uses Kubernetes to execute code in response to events, such as API requests. The workflow is driven by Keda, which scales Kubernetes pods based on incoming events like SQS messages. When Keda scales out pods that remain in a pending state, Karpenter steps in, using provisioners to decide whether to scale out additional nodes.

By integrating Keda and Karpenter with Amazon EKS, we can easily build event-driven workflows that orchestrate jobs running on Kubernetes with AWS services, such as Amazon SQS, with minimal code. All AWS resources, Kubernetes manifests, and Kubernetes add-ons are managed and installed using Terraform. We will be bootstrapping the components with EKS blueprints addons.

## Prerequisites

- Terraform
- Helm
- AWS CLI
- kubectl

## Setup

### Initialize Terraform

```sh
terraform init
terraform plan
terraform apply -auto-approve
```

After applying, we will have a VPC, EKS cluster with Karpenter, and a Fargate profile.

### Install Keda with Helm

Run the below commands to get the values file:

```sh
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
helm show values kedacore/keda > values.yaml
```

Before installing the release, update the values file (`values.yaml`):

```yaml
serviceAccount:
  annotations: 
    eks.amazonaws.com/role-arn: <POD_ROLE_ARN>
```

Now to deploy Keda, run:

```sh
helm install keda kedacore/keda --values values.yaml --namespace keda
```

### Create SQS Queue

```sh
aws sqs create-queue --queue-name keda-karpenter-scaling
```

### Deploy Test Application

```sh
kubectl create ns keda-karpenter-scaling
kubectl config set-context --current --namespace=keda-karpenter-scaling
kubectl create deployment nginx-deployment --image nginx --replicas=2 --requests=cpu=1,memory=3Gi
```

### Create ScaledObject

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: nginx-scaledobject
  namespace: keda-karpenter-scaling
spec:
  scaleTargetRef:
    name: nginx-deployment
  triggers:
  - type: aws-sqs-queue
    metadata:
      queueURL: https://sqs.eu-west-1.amazonaws.com/$AWS_ACCOUNT_ID/keda-karpenter-scaling
      queueLength: "5"
```

### Test the Setup

```sh
for i in {1..2}
do
  aws sqs send-message \
  --queue-url $(aws sqs get-queue-url --queue-name keda-karpenter-scaling) \
  --message-body "Keda and Karpenter demo"
done
```

## Conclusion

This setup demonstrates how to use Keda and Karpenter to create an event-driven architecture on Amazon EKS, scaling Kubernetes pods and nodes dynamically based on incoming events.

