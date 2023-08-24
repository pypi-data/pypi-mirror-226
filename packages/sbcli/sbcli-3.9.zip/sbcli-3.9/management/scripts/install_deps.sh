#!/usr/bin/env bash

function set_config() {
  sudo sed -i "s#\($1 *= *\).*#\1$2#" $3
}


sudo yum update -y
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install pkg-config git wget python3-pip yum-utils docker-ce docker-ce-cli \
  containerd.io docker-buildx-plugin docker-compose-plugin -y
#sudo pip install -r $TD/api/requirements.txt

sudo systemctl enable docker
sudo systemctl start docker

wget https://github.com/apple/foundationdb/releases/download/7.3.3/foundationdb-clients-7.3.3-1.el7.x86_64.rpm
sudo rpm -Uvh foundationdb-clients-7.3.3-1.el7.x86_64.rpm
rm -f foundationdb-clients-7.3.3-1.el7.x86_64.rpm

sudo mkdir -p /etc/foundationdb/data /etc/foundationdb/logs
sudo chown -R foundationdb:foundationdb /etc/foundationdb


DEV_IPS=($(hostname -I))
DEV_IP=${DEV_IPS[0]}

set_config ExecStart "/usr/bin/dockerd --containerd=/run/containerd/containerd.sock -H tcp://${DEV_IP}:2375 -H unix:///var/run/docker.sock -H fd://" /usr/lib/systemd/system/docker.service
sudo systemctl daemon-reload
sudo systemctl restart docker


##############################################################################


docker build -t spdk -f Dockerfile .

export HUGEMEM=4096
bash /home/ec2-user/spdk/scripts/setup.sh
modprobe nvme-fabrics
docker run --name spdkdev --privileged --net host -d -v /dev:/dev -v /var/tmp:/var/tmp -v /var/run/dpdk:/var/run/dpdk spdk /root/spdk/build/bin/nvmf_tgt

#docker run --name spdkrpc --privileged --net host -d -v /var/tmp:/var/tmp spdk /root/spdk/

#docker exec -it spdkdev /root/spdk/scripts/rpc_http_proxy.py 127.0.0.1 9009 spdkcsiuser spdkcsipass


