FROM postgres:14-alpine
RUN apk update && apk add
RUN mkdir -p /docker-entrypoint-initdb.d
# Copy in the load-extensions script
COPY load-extensions.sh /docker-entrypoint-initdb.d/