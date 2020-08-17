# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-18.04"
  config.vm.box_version = ">=0" #DeffaultVersion
  config.vm.network "forwarded_port", guest: 8000, host: 9000, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 8080, host: 9090, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 5000, host: 6000, host_ip: "127.0.0.1"

  # Work around disconnected virtual network cable.
  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--cableconnected1", "on"]
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get -qqy update

    # Work around https://github.com/chef/bento/issues/661
    # apt-get -qqy upgrade
    DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade

    apt-get -qqy install make zip unzip postgresql

    echo '==========='
    echo '==========='
    echo 'creating python3'
    echo '  '
    apt install software-properties-common
    add-apt-repository ppa:deadsnakes/ppa -y 
    apt update
    apt-get -qqy install python3.8 python3-pip
    update-alternatives --install /usr/bin/python python /usr/bin/python3.8 10



    pip3 install --upgrade pip
    pip3 install flask packaging oauth2client redis passlib flask-httpauth
    pip3 install sqlalchemy flask-sqlalchemy psycopg2 bleach requests

    echo '==========='
    echo '==========='
    echo '======= Python DONE ===='

    # apt-get -qqy install python python-pip
    # pip2 install --upgrade pip
    # pip2 install flask packaging oauth2client redis passlib flask-httpauth
    # pip2 install sqlalchemy flask-sqlalchemy psycopg2 bleach requests

    echo '==========='
    echo '==========='
    echo '======= Creating Postgres settings ===='
    echo '  '
    su -u postgres bash -c "psql -c \"CREATE USER vagrant WITH PASSWORD 'vagrant';\""
    su -u postgres bash -c "psql -c \"ALTER USER vagrant with SUPERUSER;\""
    vagrant -c 'createdb catalog'

    echo '==========='
    echo '==========='
    echo '======= DONE ===='  
    
    vagrantTip="[35m[1mThe shared directory is located at /vagrant\\nTo access your shared files: cd /vagrant[m"
    echo -e $vagrantTip > /etc/motd

    wget http://download.redis.io/redis-stable.tar.gz
    tar xvzf redis-stable.tar.gz
    cd redis-stable
    make
    make install

    # Install PGAdmin
    # sudo apt-get install postgresql-11 pgadmin4 --y 

    echo "Done installing your virtual machine!"
  SHELL
end
