from PIL import Image
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EKS, EC2
from diagrams.aws.integration import SQS
from diagrams.aws.network import VPC
from diagrams.aws.general import Client
from diagrams.k8s.compute import Pod, Deployment
from diagrams.k8s.network import Service
from diagrams.custom import Custom

keda_img = Image.open("keda.png")

keda_img = keda_img.resize((3000, 3000))
keda_img.save("keda_resized.png")
keda_resized = "keda_resized.png"

karpenter_img = Image.open("karpenter.png")
karpenter_img = karpenter_img.resize((3000, 3000))
karpenter_img.save("karpenter_resized.png")

karpenter_resized = "karpenter_resized.png"

# Create the diagram
with Diagram("EKS Scaling with Keda and Karpenter based on number of messages in the SQS queue"):
    client = Client("User")

    with Cluster("AWS Cloud"):
        with Cluster("VPC"):
            sqs = SQS("Message Queue")

            with Cluster("EKS Cluster"):
                keda = Custom("Keda", keda_resized)  # Use resized Keda image
                karpenter = Custom("Karpenter", karpenter_resized)  # Use resized Karpenter image
                
                with Cluster("Workloads"):
                    service = Service("Service")
                    pods = [Pod("Pod1"), Pod("Pod2"), Pod("Pod3")]

                sqs >> Edge(label="Message triggers scaling") >> keda
                keda >> service >> pods
                keda >> karpenter

            karpenter >> EC2("New Nodes")

    client >> Edge(label="Requests") >> service
