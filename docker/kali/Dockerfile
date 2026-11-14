FROM kalilinux/kali-rolling:latest

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates curl iproute2 medusa python3 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 1000 lab

USER lab
WORKDIR /home/lab
CMD ["sleep", "infinity"]
