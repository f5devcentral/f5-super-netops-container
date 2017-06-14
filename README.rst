README
======

Status
------

**Master:** |badge_rtd_latest| |badge_travis_master|

**Develop:** |badge_rtd_develop| |badge_travis_develop|

About
-----

Super-NetOps is the new NetOps. This repo supports and auto-build integration
with Docker Hub.

Docker Repo: https://hub.docker.com/r/f5devcentral/f5-super-netops-container/
GitHub Repo: https://github.com/f5devcentral/f5-super-netops-container

To learn more about Super-NetOps, read 'Does DevOps need a Super-NetOps':

https://redtalks.live/2016/11/04/does-devops-need-a-super-netops/

Use
---

The f5-super-netops container uses the Docker platform:

https://www.docker.com/products/overview#/install_the_platform

The following command will download the 'f5-super-netops-container', run it,
remap the SSH and HTTP ports to localhost:2222 and localhost:8080 respectively
and begin an interactive shell session:

`docker run -p 8080:80 -p 2222:22 -it f5devcentral/f5-super-netops-container:base`


.. |badge_travis_master| image:: https://www.travis-ci.org/f5devcentral/f5-super-netops-container.svg?branch=master
   :target: https://www.travis-ci.org/f5devcentral/f5-super-netops-container

.. |badge_travis_develop| image:: https://www.travis-ci.org/f5devcentral/f5-super-netops-container.svg?branch=develop
   :target: https://www.travis-ci.org/f5devcentral/f5-super-netops-container

.. |badge_rtd_latest| image:: https://readthedocs.org/projects/f5-super-netops-container/badge/?version=latest
   :target: http://f5-super-netops-container.readthedocs.io/en/latest/?badge=latest

.. |badge_rtd_develop| image:: https://readthedocs.org/projects/f5-super-netops-container/badge/?version=develop
   :target: http://f5-super-netops-container.readthedocs.io/en/develop/?badge=develop
