# About
Super-NetOps is the new NetOps. This repo supports and auto-build integration
with Docker Hub. To use the Super-NetOps container, visit:
https://hub.docker.com/r/f5supernetops/f5-super-netops/

To learn more about Super-NetOps, read 'Does DevOps need a Super-NetOps': https://redtalks.live/2016/11/04/does-devops-need-a-super-netops/

# Use
The f5-super-netops container uses the Docker platform:

https://www.docker.com/products/overview#/install_the_platform

The following command will download the 'f5-super-netops' container, run it,
remap the SSH and HTTP ports to localhost:2222 and localhost:8080 respectively
and begin an interactive shell session:

`docker run -p 8080:80 -p 2222:22 -it f5supernetops/f5-super-netops`
