FROM alpine:latest AS builder

ARG TARGETARCH

# CentOS 7 已停止维护(2024-06 EOL)，直接在 Alpine 中下载 v2ray 二进制文件
# 使用 releases/latest/download 直链，无需查询 GitHub API，避免 CI 中被限流
RUN set -ex \
    && apk add --no-cache curl unzip \
    && case "${TARGETARCH}" in \
        amd64) ARCH="64" ;; \
        arm64) ARCH="arm64-v8a" ;; \
        386)   ARCH="32" ;; \
        *)     echo "Unsupported arch: ${TARGETARCH}"; exit 1 ;; \
       esac \
    && curl -fL --retry 3 --retry-delay 5 -o /tmp/v2ray.zip \
         "https://github.com/v2fly/v2ray-core/releases/latest/download/v2ray-linux-${ARCH}.zip" \
    && mkdir -p /usr/bin/v2ray \
    && unzip -oj /tmp/v2ray.zip -d /usr/bin/v2ray \
    && chmod +x /usr/bin/v2ray/v2ray \
    && rm -f /tmp/v2ray.zip

FROM alpine:latest

LABEL maintainer="Jrohy <euvkzx@Jrohy.com>"

ENV COMPLETION_FILE="/usr/share/bash-completion/completions/v2ray"
ENV SOURCE_COMPLETION_FILE="https://multi.netlify.app/v2ray"

COPY --from=builder /usr/bin/v2ray/v2ray /usr/bin/v2ray/
COPY --from=builder /usr/bin/v2ray/geoip.dat /usr/bin/v2ray/
COPY --from=builder /usr/bin/v2ray/geosite.dat /usr/bin/v2ray/
COPY docker/v2ray/run.sh /root
# 复制源码用于本地安装 v2ray-util，不依赖 PyPI
COPY setup.py README.md README_EN.md /tmp/v2ray-util/
COPY v2ray_util/ /tmp/v2ray-util/v2ray_util/

WORKDIR /root

RUN set -ex \
    && apk --no-cache add python3 py3-pip bash bash-completion ca-certificates curl socat openssl iptables ip6tables \
    && rm -f /usr/lib/python*/EXTERNALLY-MANAGED \
    && ln -sf $(which pip3) /usr/local/bin/pip \
    && pip install --only-binary=:all: cryptography 2>/dev/null || true \
    && pip install --no-build-isolation /tmp/v2ray-util/ \
    && rm -rf /tmp/v2ray-util \
    && curl $SOURCE_COMPLETION_FILE > $COMPLETION_FILE \
    && mkdir -p /var/log/v2ray/ \
    && chmod +x /usr/bin/v2ray/v2ray \
    && chmod +x /root/run.sh \
    && chmod +x $COMPLETION_FILE \
    && echo "source $COMPLETION_FILE" > /root/.bashrc \
    && ln -s $(which v2ray-util) /usr/local/bin/v2ray \
    && rm -rf /root/.cache

ENTRYPOINT ["./run.sh"]
