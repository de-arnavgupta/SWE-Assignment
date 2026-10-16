# Stage 1: Build Java bytecode
FROM eclipse-temurin:17-jdk-alpine AS builder
WORKDIR /app
COPY SimpleHttpServer.java .
RUN javac SimpleHttpServer.java

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=builder /app/SimpleHttpServer*.class ./
RUN chown -R appuser:appgroup /app

USER appuser
EXPOSE 8080

CMD ["java", "SimpleHttpServer"]
