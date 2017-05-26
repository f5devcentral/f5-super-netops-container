###############################################################
# Dockerfile to build f5-super-netops-container Jenkins variant
###############################################################

# Derived from https://github.com/jenkinsci/docker

# Start with an awesome, tiny Linux distro.
FROM f5devcentral/f5-super-netops-container:base

LABEL maintainer "h.patel@f5.com, n.pearce@f5.com"

# Set the SNOPS image name
ENV SNOPS_IMAGE jenkins

RUN apk add --no-cache openjdk8 git openssh-client curl unzip bash ttf-dejavu coreutils

ENV PATH ${PATH}:/usr/lib/jvm/java-1.8-openjdk/bin/

# Copy in base FS from repo
COPY fs /

ENV JENKINS_HOME /var/jenkins_home
ENV JENKINS_SLAVE_AGENT_PORT 50000

ARG user=jenkins
ARG group=jenkins
ARG uid=1001
ARG gid=1001

# Jenkins is run with user `jenkins`, uid = 1001
# If you bind mount a volume from the host or a data container,
# ensure you use the same uid
RUN addgroup -g ${gid} ${group} \
    && adduser -h "$JENKINS_HOME" -u ${uid} -G ${group} -s /bin/bash -D ${user}

# Jenkins home directory is a volume, so configuration and build history
# can be persisted and survive image upgrades
VOLUME /var/jenkins_home

# `/usr/share/jenkins/ref/` contains all reference configuration we want
# to set on a fresh new installation. Use it to bundle additional plugins
# or config file with your custom jenkins Docker image.
RUN mkdir -p /usr/share/jenkins/ref/init.groovy.d

# jenkins version being bundled in this docker image
ARG JENKINS_VERSION
#ENV JENKINS_VERSION ${JENKINS_VERSION:-2.46.2}
ENV JENKINS_VERSION ${JENKINS_VERSION:-2.62}
ENV COPY_REFERENCE_FILE_LOG $JENKINS_HOME/copy_reference_file.log

# jenkins.war checksum, download will be validated using it
#ARG JENKINS_SHA=aa7f243a4c84d3d6cfb99a218950b8f7b926af7aa2570b0e1707279d464472c7
ARG JENKINS_SHA=b0778a1763e582ecbbece698e9ef78b45579ef8945db0198fe02295de8da15b7

# Can be used to customize where jenkins.war get downloaded from
ARG JENKINS_URL=https://repo.jenkins-ci.org/public/org/jenkins-ci/main/jenkins-war/${JENKINS_VERSION}/jenkins-war-${JENKINS_VERSION}.war

# could use ADD but this one does not check Last-Modified header neither does it allow to control checksum
# see https://github.com/docker/docker/issues/8331
RUN curl -fsSL ${JENKINS_URL} -o /usr/share/jenkins/jenkins.war \
  && echo "${JENKINS_SHA}  /usr/share/jenkins/jenkins.war" | sha256sum -c -

ARG JENKINS_CI_URL=https://raw.githubusercontent.com/jenkinsci/docker/master
ADD ${JENKINS_CI_URL}/init.groovy /usr/share/jenkins/ref/init.groovy.d/tcp-slave-agent-port.groovy
ADD ${JENKINS_CI_URL}/jenkins-support /usr/local/bin/jenkins-support
ADD ${JENKINS_CI_URL}/jenkins.sh /usr/local/bin/jenkins.sh
ADD ${JENKINS_CI_URL}/plugins.sh /usr/local/bin/plugins.sh
ADD ${JENKINS_CI_URL}/install-plugins.sh /usr/local/bin/install-plugins.sh
RUN chmod 755 /usr/local/bin/jenkins* /usr/local/bin/*plugins*

ENV JENKINS_UC https://updates.jenkins.io

RUN /usr/local/bin/install-plugins.sh bouncycastle-api cloudbees-folder structs junit antisamy-markup-formatter pam-auth windows-slaves display-url-api mailer ldap token-macro external-monitor-job icon-shim matrix-auth script-security matrix-project build-timeout credentials workflow-step-api plain-credentials credentials-binding timestamper scm-api workflow-api workflow-support durable-task workflow-durable-task-step resource-disposer ws-cleanup ant gradle pipeline-milestone-step jquery-detached pipeline-input-step ace-editor workflow-scm-step workflow-cps pipeline-stage-step workflow-job pipeline-graph-analysis pipeline-rest-api handlebars momentjs pipeline-stage-view pipeline-build-step pipeline-model-api pipeline-model-extensions ssh-credentials git-client git-server workflow-cps-global-lib branch-api workflow-multibranch authentication-tokens docker-commons docker-workflow pipeline-stage-tags-metadata pipeline-model-declarative-agent workflow-basic-steps pipeline-model-definition workflow-aggregator github-api git github github-branch-source pipeline-github-lib github-organization-folder mapdb-api subversion ssh-slaves email-ext

RUN chown -R ${user}:${group} "$JENKINS_HOME" /usr/share/jenkins/ref /usr/local/bin/jenkins* /usr/local/bin/*plugins*

# for main web interface:
EXPOSE 8080

# will be used by attached slave agents:
EXPOSE 50000
