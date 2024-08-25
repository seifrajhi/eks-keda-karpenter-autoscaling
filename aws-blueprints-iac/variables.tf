variable "name" {
  description = "Name of the VPC and EKS Cluster"
  default     = "eks-keda-karpenter"
  type        = string
}

variable "region" {
  description = "Region"
  type        = string
  default     = "eu-west-1"
}

variable "eks_cluster_version" {
  description = "EKS Cluster version"
  default     = "1.29"
  type        = string
}

variable "vpc_cidr" {
  description = "VPC CIDR"
  default     = "10.1.0.0/16"
  type        = string
}
