############################################################
# Dockerfile to build f5-super-netops enablement container
# Based on Alpine Linux, seasoned with tools and workflows
############################################################

# Start with an awesome, tiny Linux distro.
FROM alpine
MAINTAINER Nathan Pearce, Hitesh Patel

# setuid so things like ping work
RUN chmod +s /bin/busybox

# Add in S6 overlay so we can run some services
ADD https://github.com/just-containers/s6-overlay/releases/download/v1.19.1.1/s6-overlay-x86.tar.gz /tmp/
RUN gunzip -c /tmp/s6-overlay-x86.tar.gz | tar -xf - -C /

# Add go-dnsmasq so resolver works
ADD https://github.com/janeczku/go-dnsmasq/releases/download/1.0.7/go-dnsmasq-min_linux-amd64 /usr/sbin/go-dnsmasq
RUN chmod +x /usr/sbin/go-dnsmasq

# Start S6 init
ENTRYPOINT ["/init"]
CMD ["/start"]

# Add useful APKs
RUN apk add --update openssh bash curl git python2 py2-requests py2-sphinx py-pip nodejs

# Add node http-server
RUN npm install -g http-server

# Setup various users and passwords
RUN adduser -h /home -u 1000 -s /bin/bash snops -D
RUN echo 'snops:default' | chpasswd
RUN echo 'root:default' | chpasswd

# Copy in base FS from repo
COPY fs /

# Expose SSH and HTTP
EXPOSE 22 80

# Enable cloning/install of useful repositories on boot
ENV SNOPS_AUTOCLONE 1
ENV SNOPS_GH_BRANCH master
