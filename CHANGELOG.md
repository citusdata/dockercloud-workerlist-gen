### docker-workerlist-gen v0.9.0 (March 2, 2016) ###

* Initial release

* Based on `dockercloud-haproxy` `v1.1`

* Monitors Citus worker startup/shutdown

* Regenerates `pg_worker_list.conf` when workers change

* Sends `SIGHUP` to `master`

* Listens for Docker Cloud events

* Configurable via environment variables
