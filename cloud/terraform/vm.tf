resource "google_compute_instance" "sim_vm" {
  name         = var.vm_name
  machine_type = "e2-standard-2"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
      size  = 30
    }
  }

  network_interface {
    network = "default"

    access_config {}
  }

  metadata = {
    enable-oslogin = "TRUE"
  }

  tags = ["infra-agent-sim"]
}
