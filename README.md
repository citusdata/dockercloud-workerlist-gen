# dockercloud-workerlist-gen

[![Image Size](https://img.shields.io/imagelayers/image-size/citusdata/dockercloud-workerlist-gen/latest.svg)][image size]
[![Release](https://img.shields.io/github/release/citusdata/dockercloud-workerlist-gen.svg)][release]
[![License](https://img.shields.io/github/license/citusdata/dockercloud-workerlist-gen.svg)][license]

----------

**NOTE: THIS SOFTWARE IS NOT PRODUCTION-READY. DOCKER CLOUD WORKERLIST GENERATION IS A PROOF-OF-CONCEPT AND REQUIRES MORE POLISH BEFORE PRODUCTION DEPLOYMENT.**

----------

`dockercloud-workerlist-gen` provides the functionality of [`workerlist-gen`][workerlist-gen], but in the cloud. Based on the [`dockercloud-haproxy`][dockercloud-haproxy] codebase, it listens to Docker Cloud events to automatically regenerate the Citus worker list file any time a Citus container is destroyed or added.

## Function

`dockercloud-workerlist-gen` is a Python program which listens to Docker Cloud events, regenerating a Citus worker list file any time an cloud container is created or destroyed.

Unlike `workerlist-gen`, there is no expectation that the worker containers be colocated with other Citus containers: the only restriction is that all nodes be in the same “stack”, and that containers running `dockercloud-workerlist-gen` be deployed alongside any Citus master containers. This is easily accomplished with deployment tags.

## Usage

Though it is unlikely to be very useful, you can put this image on a local container:

```bash
docker run citusdata/dockercloud-workerlist-gen

# Traceback (most recent call last):
#   File "/usr/local/bin/dockercloud-workerlistgen", line 9, in <module>
#     load_entry_point('dockercloud-workerlistgen==0.9.0', 'console_scripts', 'dockercloud-workerlistgen')()
#   File "/usr/local/lib/python2.7/dist-packages/workerlistgen/main.py", line 61, in main
#     autoreload = set_autoreload(WORKERLISTGEN_CONTAINER_URI, WORKERLISTGEN_SERVICE_URI, API_AUTH)
#   File "/usr/local/lib/python2.7/dist-packages/workerlistgen/main.py", line 41, in set_autoreload
#     raise RuntimeError(msg)
# RuntimeError: dockercloud/workerlistgen 0.9.0 is not running in Docker Cloud
```

The better place to deploy this would be in a Docker Cloud stack. This image needs links to the workers it should be monitoring, as well as the `global` role, to ensure it can access the Docker Cloud API. The master and worker services should be deployed to nodes with those tags (master or worker), and the config container should be deployed alongside the master service (using master tags).

As with `workerlist-gen`, this container needs access to the Docker socket (at `/tmp/docker.sock`), as well as access to the config volume exposed by a Citus master container.

### Config Example

As the above rules are somewhat complex, the following config block may help by showing all of them in place at once.

```yaml
config:
  image: 'citusdata/dockercloud-workerlist-gen:latest'
  volumes: ['/var/run/docker.sock:/tmp/docker.sock']
  volumes_from: ['master']
  roles: ['global']
  tags: ['master']
  links: ['worker']
```

### Options

The default values should usually be sufficient, but just in case, some simple options are provided:

  * `CITUS_CONFDIR` — Output directory for worker list file (default: `/etc/citus`)
  * `CITUS_SERVICE_NAME` — Service name to restart after configuration changes (default: `master`)
  * `DEBUG` — For more verbose log output (default: `false`)

## License

Copyright © 2016 Citus Data, Inc.

Licensed under the Apache License, Version 2.0 (the “License”); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an “AS IS” BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

[image size]: https://imagelayers.io/?images=citusdata%2Fdockercloud-workerlist-gen:latest
[release]: https://github.com/citusdata/dockercloud-workerlist-gen/releases/latest
[license]: LICENSE
[workerlist-gen]: https://github.com/citusdata/workerlist-gen
[dockercloud-haproxy]: https://github.com/docker/dockercloud-haproxy
