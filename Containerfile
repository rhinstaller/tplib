FROM quay.io/centos/centos:stream8

RUN dnf install -y epel-release && \
    dnf install -y dnf-plugin-config-manager && \
    dnf config-manager --enable powertools

RUN dnf install -y git python3 make python3-jinja2 python3-pyyaml \
                   python3-pylint python3-sphinx diffutils python3-libxml2
