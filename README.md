# redborder-producers
Scripts to produce synthetic data for demos

This is a collection of scripts to produce synthetic data for demos. This repo borns from synthetic_producer repo, but hardcoding the values and randomizing the data at the same time the data still has sense. This repo needs its own space because of how much special the data need to be on a production machine such a demo as experience ng, which goes farther than usual development machines.

# Requirements

This is an auxiliar package for redborder-manager, si is expecte to be installed
* redborder-manager

# Setup
The configuration files tweak the properties of the producers, but there are some that really need to be changed:
* /etc/redborder/producers/sensors.py => Configure this by reading the sensor properties on the manager and pass them to this file.

# Main command
rb_start_synthetic_producers.sh: Starts the producers in pararell by using screen instances, one for each data source. The command is not part of this repo, but it is the main command to start the producers. It is particullar for live and not tested. Needs to be generalized.

# Building the rpm package
On Release section, you can find already stable rpms, but if you want to build the rpm from the source code. You can execute the following command on top of the repository path:

```bash
sudo make rpm
```

For this feature, mock is required to be installed.