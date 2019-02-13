FROM alpine:3.8

RUN apk --no-cache add ca-certificates && update-ca-certificates

EXPOSE 8080

COPY backend /
ENTRYPOINT ["/backend"]