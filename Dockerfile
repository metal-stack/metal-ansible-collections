FROM ghcr.io/metal-stack/metal-deployment-base:latest
COPY Makefile /
RUN make install && rm /Makefile
