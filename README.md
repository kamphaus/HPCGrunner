# Python Runner & Aggregator for HPCG

This python script will read a configuration file and run the HPCG benchmark according to this configuration.
Finally it will aggregate the results and generate diagrams.

## Installation

Check out from github: `git clone https://github.com/kamphaus/HPCGrunner.git`

## Prerequisites

You need the following software:
* HPCG http://hpcg-benchmark.org/
* Python 2.7
* Python modules:
  * pyyaml
  * numpy
  * pubnub
  * python-matplotlib

## Usage

Edit `config.yml` and `environment.yml`.

Execute `python runner.py`
