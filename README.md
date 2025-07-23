# redborder-producers
Scripts to produce synthetic data for demos

This is a collection of scripts to produce synthetic data for demos. This repo borns from synthetic_producer repo, but hardcoding the values and randomizing the data at the same time the data still has sense. This repo needs its own space because of how much special the data need to be on a production machine such a demo as experience ng, which goes farther than usual development machines.

# Requirements

This is an auxiliar package for redborder-manager, which is expected to be installed
* redborder-manager

Additionally each required module is expected to be enabled. 

Particularly with intrusion, which needs to be patched on the logstash condition if ips sensor is not claimed. So check file /etc/logstash/pipelines.yml to see intrusion-pipeline is there. If not, open this file: /var/chef/cookbooks/rb-manager/libraries/get_pipelines.rb, comment the condition in order to always make intrusion pipeline available, and update the cookbook with knife cookbook upload rb-manager

# Setup
The configuration files tweak the properties of the producers, but there are some that really need to be changed:
* /usr/lib/redborder/producers/py/sensors.py => Configure this by reading the sensor properties on the manager and pass them to this file.

# Main command
rb_producer_simulator.sh: Start one or multiple producers in pararell by using screen instances, one for each data source.

## Usage
You can run the script with always the action argument to run every producers at once:
```bash
rb_producer_simulator.sh -a <start|stop|restart>
```

But if you want to run only one producer, you can use the argument -s:
```bash
rb_producer_simulator.sh -a <start|stop|restart> -s <traffic|scanner|vault>
```

Check usage to confirm with the helper:
```bash
rb_producer_simulator.sh -h
```

# Building the rpm package
On Release section, you can find already stable rpms, but if you want to build the rpm from the source code. You can execute the following command on top of the repository path:

```bash
sudo make rpm
```

For this feature, mock is required to be installed.