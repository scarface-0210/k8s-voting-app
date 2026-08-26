#!/bin/bash

set -e

echo "=== Updating system ==="
sudo apt-get update
sudo apt-get upgrade -y

echo "=== Disabling swap ==="
sudo swapoff -a
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab

echo "=== Loading kernel modules ==="
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

echo "=== Configuring Kubernetes networking ==="
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward = 1
EOF

sudo sysctl --system

echo "=== Installing containerd ==="
sudo apt-get install -y containerd

sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml > /dev/null

sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' \
    /etc/containerd/config.toml

sudo systemctl restart containerd
sudo systemctl enable containerd

echo "=== Installing Kubernetes repository ==="
sudo apt-get install -y apt-transport-https ca-certificates curl gpg

sudo mkdir -p -m 755 /etc/apt/keyrings

curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.34/deb/Release.key |
sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.34/deb/ /' |
sudo tee /etc/apt/sources.list.d/kubernetes.list > /dev/null

echo "=== Installing Kubernetes ==="
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl

sudo apt-mark hold kubelet kubeadm kubectl

echo "=== Initializing Kubernetes cluster ==="
sudo kubeadm init --pod-network-cidr=10.244.0.0/16

echo "=== Configuring kubectl ==="
mkdir -p "$HOME/.kube"

sudo cp -i /etc/kubernetes/admin.conf "$HOME/.kube/config"

sudo chown "$(id -u):$(id -g)" "$HOME/.kube/config"

echo "=== Installing Flannel CNI ==="
kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml

echo "=== Allowing workloads on control-plane ==="
kubectl taint nodes --all node-role.kubernetes.io/control-plane- || true

echo "=== Kubernetes installation complete ==="

echo ""
echo "=== Node status ==="
kubectl get nodes

echo ""
echo "=== All pods ==="
kubectl get pods -A
