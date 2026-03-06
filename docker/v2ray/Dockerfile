FROM alpine:latest AS builder

ARG TARGETARCH

# CentOS 7 已停止维护(2024-06 EOL)，直接在 Alpine 中下载 v2ray 二进制文件
RUN apk add --no-cache curl unzip \
    && case "${TARGETARCH}" in \
        amd64) ARCH="64" ;; \
        arm64) ARCH="arm64-v8a" ;; \
        386)   ARCH="32" ;; \
        *)     echo "Unsupported arch: ${TARGETARCH}" && exit 1 ;; \
       esac \
    && LATEST=$(curl -sL "https://api.github.com/repos/v2fly/v2ray-core/releases/latest" \
         -H "Accept: application/json" -H "User-Agent: Mozilla/5.0" \
         | grep '"tag_name"' | cut -d'"' -f4) \
    && [ -n "${LATEST}" ] || { echo "Failed to fetch latest v2ray version"; exit 1; } \
    && echo "Downloading v2ray ${LATEST} for linux-${ARCH}" \
    && curl -L -o /tmp/v2ray.zip \
         "https://github.com/v2fly/v2ray-core/releases/download/${LATEST}/v2ray-linux-${ARCH}.zip" \
    && mkdir -p /usr/bin/v2ray \
    && unzip -oj /tmp/v2ray.zip -d /usr/bin/v2ray \
    && chmod +x /usr/bin/v2ray/v2ray

FROM alpine:latest

LABEL maintainer="Jrohy <euvkzx@Jrohy.com>"

ENV COMPLETION_FILE="/usr/share/bash-completion/completions/v2ray"
ENV SOURCE_COMPLETION_FILE="https://multi.netlify.app/v2ray"
ENV VERSION_LIST="https://api.github.com/repos/Jrohy/multi-v2ray/tags"

COPY --from=builder /usr/bin/v2ray/v2ray /usr/bin/v2ray/
COPY --from=builder /usr/bin/v2ray/geoip.dat /usr/bin/v2ray/
COPY --from=builder /usr/bin/v2ray/geosite.dat /usr/bin/v2ray/
COPY run.sh /root

WORKDIR /root

RUN apk --no-cache add python3 py3-pip bash bash-completion ca-certificates curl socat openssl iptables ip6tables && \
    rm -f /usr/lib/python*/EXTERNALLY-MANAGED && \
    ln -sf $(which pip3) /usr/local/bin/pip && \
    LATEST_VERSION=`curl -s $VERSION_LIST|grep name|grep -o "[0-9].*[0-9]"|head -n 1` && \
    pip install v2ray-util==$LATEST_VERSION && \
    curl $SOURCE_COMPLETION_FILE > $COMPLETION_FILE && \
    mkdir /var/log/v2ray/ && \
    chmod +x /usr/bin/v2ray/v2ray && \
    chmod +x /root/run.sh && \
    chmod +x $COMPLETION_FILE && \
    echo "source $COMPLETION_FILE" > /root/.bashrc && \
    ln -s $(which v2ray-util) /usr/local/bin/v2ray && \
    rm -r /root/.cache

ENTRYPOINT ["./run.sh"]
