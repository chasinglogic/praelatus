# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/xenial64"

  config.vm.define "database" do |db|
    db.vm.network "private_network", ip: "192.168.50.4"
    db.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/playbook.yml"
      ansible.sudo = true
      ansible.host_key_checking = false
      ansible.groups = {
        "database" => ["default"]
      }
    end
  end

  config.vm.define "rabbitmq" do |mq| 
    mq.vm.network "private_network", ip: "192.168.50.5"
    mq.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/playbook.yml"
      ansible.sudo = true
      ansible.host_key_checking = false
      ansible.groups = {
        "mqserver" => ["default"]
      }
    end
  end

  config.vm.define "app", primary: true do |app|
    app.vm.network "private_network", ip: "192.168.50.6"
    app.vm.network "forwarded_port", guest: 8080, host: 8080
    app.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/playbook.yml"
      ansible.sudo = true
      ansible.host_key_checking = false
      ansible.groups = {
        "appserver" => ["default"]
      }
    end
  end
end
