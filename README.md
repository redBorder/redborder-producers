# redborder-producers
Scripts to produce synthetic data for demos

This is a collection of scripts to produce synthetic data for demos. This repo borns from synthetic_producer repo, but hardcoding the values and randomizing the data at the same time the data still has sense. This repo needs its own space because of how much special the data need to be on a production machine such a demo as experience ng, which goes farther than usual development machines.

# Requirements

At least one of these packages must be installed:
* redborder-manager
* redborder-proxy
* redborder-ips
# Main command
rb_start_synthetic_producers.sh: Starts the producers in pararell by using screen instances, one for each data source. The command is not part of this repo, but it is the main command to start the producers. It is particullar for live and not tested. Needs to be generalized.
