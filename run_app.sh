#!/bin/bash
export CONFIG_PATH=config/$2.cfg
PYTHONPATH=./ python $1 --host ${3-127.0.0.1}
