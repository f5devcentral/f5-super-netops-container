############################################################
# Dockerfile to build f5-super-netops:base enablement container
# Based on Alpine Linux, seasoned with tools and workflows
############################################################

# Start with an awesome, tiny Linux distro.
FROM alpine:3.5

LABEL maintainer "h.patel@f5.com, n.pearce@f5.com"

ENV SNOPS_REPO https://github.com/f5devcentral/f5-super-netops-container.git

# Set the SNOPS image name
ENV SNOPS_IMAGE base

# setuid so things like ping work
RUN chmod +s /bin/busybox

# Add in S6 overlay so we can run some services
ADD https://github.com/just-containers/s6-overlay/releases/download/v1.19.1.1/s6-overlay-x86.tar.gz /tmp/
RUN gunzip -c /tmp/s6-overlay-x86.tar.gz | tar -xf - -C / && rm -f /tmp/s6-overlay-x86.tar.gz

# Add go-dnsmasq so resolver works
ADD https://github.com/janeczku/go-dnsmasq/releases/download/1.0.7/go-dnsmasq-min_linux-amd64 /usr/sbin/go-dnsmasq
RUN chmod +x /usr/sbin/go-dnsmasq

# Start S6 init
ENTRYPOINT ["/init"]
CMD ["/snopsboot/start"]

# Add useful APKs
#RUN apk add --update openssh bash curl git vim nano python2 py2-requests py2-sphinx py-pip nodejs nodejs-npm
RUN apk add --update openssh bash curl git vim nano python2 py2-requests py2-sphinx py-pip nodejs enchant

# Upgrade pip
RUN pip install --upgrade pip

# Add node http-server
RUN npm install -g http-server

# Setup various users and passwords
RUN adduser -h /home/snops -u 1000 -s /bin/bash snops -D
RUN echo 'snops:default' | chpasswd
RUN echo 'root:default' | chpasswd

# Copy in base FS from repo
COPY fs /

# Expose SSH and HTTP
EXPOSE 22 80

# Set Git Credentials
# !!WARNING!! - password is stored in plaintext
ENV SNOPS_GIT_USERNAME ""
ENV SNOPS_GIT_PASSWORD ""
ENV SNOPS_GIT_HOST "github.com"

# Set our default host redirect ports
ENV SNOPS_HOST_HTTP 8080
ENV SNOPS_HOST_SSH  2222

# Enable cloning/install of useful repositories on boot
ENV SNOPS_AUTOCLONE 0

# The GitHub branch to target for dynamic resources
ENV SNOPS_GH_BRANCH master

# ENV variable used by various scripts to detect the container environment
ENV SNOPS_ISALIVE 1

# Enabled if you would like a dev install of reveal-js
ENV SNOPS_REVEALJS_DEV 0

# Expose reveal-js dev server port
EXPOSE 8000

RUN chmod 777 /tmp

##############################################install go ################################
RUN apk add --no-cache ca-certificates

ENV GOLANG_VERSION 1.9.4

# no-pic.patch: https://golang.org/issue/14851 (Go 1.8 & 1.7)
COPY *.patch /go-alpine-patches/

RUN set -eux; \
	apk add --no-cache --virtual .build-deps \
		bash \
		gcc \
		musl-dev \
		openssl \
		go \
	; \
	export \
# set GOROOT_BOOTSTRAP such that we can actually build Go
		GOROOT_BOOTSTRAP="$(go env GOROOT)" \
# ... and set "cross-building" related vars to the installed system's values so that we create a build targeting the proper arch
# (for example, if our build host is GOARCH=amd64, but our build env/image is GOARCH=386, our build needs GOARCH=386)
		GOOS="$(go env GOOS)" \
		GOARCH="$(go env GOARCH)" \
		GOHOSTOS="$(go env GOHOSTOS)" \
		GOHOSTARCH="$(go env GOHOSTARCH)" \
	; \
# also explicitly set GO386 and GOARM if appropriate
# https://github.com/docker-library/golang/issues/184
	apkArch="$(apk --print-arch)"; \
	case "$apkArch" in \
		armhf) export GOARM='6' ;; \
		x86) export GO386='387' ;; \
	esac; \
	\
	wget -O go.tgz "https://golang.org/dl/go$GOLANG_VERSION.src.tar.gz"; \
	echo '0573a8df33168977185aa44173305e5a0450f55213600e94541604b75d46dc06 *go.tgz' | sha256sum -c -; \
	tar -C /usr/local -xzf go.tgz; \
	rm go.tgz; \
	\
	cd /usr/local/go/src; \
	for p in /go-alpine-patches/*.patch; do \
		[ -f "$p" ] || continue; \
		patch -p2 -i "$p"; \
	done; \
	./make.bash; \
	\
	rm -rf /go-alpine-patches; \
	apk del .build-deps; \
	\
	export PATH="/usr/local/go/bin:$PATH"; \
	go version

ENV GOPATH /go
ENV PATH $GOPATH/bin:/usr/local/go/bin:$PATH

RUN mkdir -p "$GOPATH/src" "$GOPATH/bin" && chmod -R 777 "$GOPATH"

COPY go-wrapper /usr/local/bin/



#############installing terraform###############
ENV TERRAFORM_VERSION=0.11.3


WORKDIR /home/snops

RUN apk update && \
    apk add bash ca-certificates git openssl unzip wget && \
    cd /tmp && \
    wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /usr/bin && \
    rm -rf /tmp/terraform* && \
    rm -rf /var/cache/apk/* && \
    rm -rf /var/tmp/terraform*

	
################f5 terrafrom##############################	
ENV GOPATH=/home/snops/workspace
RUN mkdir -p /home/snops/workspace/src/github.com/f5devcentral && cd /home/snops/workspace && go get github.com/f5devcentral/terraform-provider-bigip
RUN cd /home/snops/workspace/src/github.com/f5devcentral/terraform-provider-bigip/ && go build
RUN mkdir -p /home/snops/.terraform.d/plugins/linux_amd64
RUN cp /home/snops/workspace/src/github.com/f5devcentral/terraform-provider-bigip/terraform-provider-bigip /home/snops/.terraform.d/plugins/linux_amd64/
RUN mkdir -p /root/.terraform.d/plugins/linux_amd64
RUN cp /home/snops/workspace/src/github.com/f5devcentral/terraform-provider-bigip/terraform-provider-bigip /root/.terraform.d/plugins/linux_amd64/
	
####################