# -*- mode: ruby -*-
# vi: set ft=ruby :

# What need to setting up when recreate environment:
# internal_ip and project_name just below
# project_name in provision\group_vars\all.yml, MUST match Vagrant's project_name

internal_ip = "172.28.128.21"
project_name = "privategames"

Vagrant.configure(2) do |config|

  #config.vm.box = "bento/ubuntu-16.04"
  config.vm.box = "boxcutter/ubuntu1610"
  #config.vm.box = "ubuntu/yakkety64"
  config.vm.network "private_network", ip: internal_ip
  config.vm.hostname = project_name

  config.vm.provider :virtualbox do |v|
    v.memory = 1024
    v.gui = false
    v.name = project_name
  end

  # for supress "stdin: is not a tty error"
  config.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"

  config.vm.synced_folder ".", "/home/vagrant/" + project_name, id: "vagrant-root",
    owner: "vagrant",
    group: "vagrant",
    mount_options: ["dmode=775,fmode=664"]

  config.vm.provision "shell", inline: <<-SHELL
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -q
    apt-get autoremove -y
  SHELL
    # apt-get install python-dev libyaml-dev -y -q
    # curl -s https://bootstrap.pypa.io/get-pip.py | sudo python -

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    mkdir --parents /home/vagrant/log
    touch /home/vagrant/log/ansible.log
  SHELL

  # Run Ansible from the Vagrant VM
  config.vm.provision :ansible_local do |ansible|
    ansible.playbook       = "provision.yml"
    ansible.verbose        = true
    ansible.install        = true
    ansible.install_mode   = 'pip'
    ansible.limit          = 'development'
    ansible.provisioning_path = "/home/vagrant/" + project_name + "/provision"
    ansible.inventory_path = "/home/vagrant/" + project_name + "/provision/inventories"
  end

end
