#!/bin/bash


ps aux | grep aigc |  awk '{print $2}' | xargs kill -9