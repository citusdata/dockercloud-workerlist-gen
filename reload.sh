#!/bin/sh
kill -USR1 $(cat /tmp/dockercloud-workerlistgen.pid)
