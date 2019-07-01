#!/bin/bash

rq info --config settings  2> /dev/null

while [ $? != 0 ]; do sleep 1; rq info --config settings  2> /dev/null ; done 

rq worker --config settings parse
