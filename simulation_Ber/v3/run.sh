#!/bin/bash

files=("FSK21.m" "2FSK2.m" "4FSK1.m" "4FSK2.m" "MSK1.m" "MSK2.m")


matlab -batch 'FSK21' &
matlab -batch 'FSK22' &
matlab -batch 'FSK41' &
matlab -batch 'FSK42' &
matlab -batch 'MSK1' &
matlab -batch 'MSK2' &
