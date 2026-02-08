variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "europe-west1"
}

variable "zone" {
  description = "GCP zone"
  type        = string
  default     = "europe-west1-b"
}

variable "vm_name" {
  description = "Name of the simulation VM"
  type        = string
  default     = "infra-agent-sim-vm"
}
