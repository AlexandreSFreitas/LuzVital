# LuzVital API — imagem para o deploy no render.com
# Estágio 1: compila com o Maven Wrapper do projeto (JDK 21)
FROM eclipse-temurin:21-jdk AS build
WORKDIR /app
COPY .mvn .mvn
COPY mvnw pom.xml ./
RUN sh mvnw -B -q dependency:go-offline
COPY src src
RUN sh mvnw -B -q package -DskipTests

# Estágio 2: só o JRE 21 e o .jar (imagem menor)
FROM eclipse-temurin:21-jre
WORKDIR /app
RUN useradd --system --uid 10001 luzvital
COPY --from=build /app/target/*.jar app.jar
USER luzvital
ENV SPRING_PROFILES_ACTIVE=prod
# O Render informa a porta pela variável PORT (application.properties usa ${PORT:8080})
EXPOSE 8080
# Limita a memória ao plano gratuito (512 MB)
ENTRYPOINT ["java", "-XX:MaxRAMPercentage=75", "-XX:+UseSerialGC", "-Xss512k", "-jar", "/app/app.jar"]
