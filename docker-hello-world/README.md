# Exercício EBAC — Primeira imagem no Docker Hub

Esta pasta contém uma imagem Docker simples baseada em BusyBox para o exercício de publicação no Docker Hub.

## Build local

```bash
cd docker-hello-world
docker build -t ebac-docker-hello-world:1.0 .
```

## Teste local

```bash
docker run --rm ebac-docker-hello-world:1.0
```

Saída esperada:

```text
Hello World - Julio Orlando
```

## Publicação no Docker Hub

Substitua `SEU_USUARIO_DOCKERHUB` pelo seu usuário real:

```bash
docker login
docker tag ebac-docker-hello-world:1.0 SEU_USUARIO_DOCKERHUB/ebac-docker-hello-world:1.0
docker tag ebac-docker-hello-world:1.0 SEU_USUARIO_DOCKERHUB/ebac-docker-hello-world:latest
docker push SEU_USUARIO_DOCKERHUB/ebac-docker-hello-world:1.0
docker push SEU_USUARIO_DOCKERHUB/ebac-docker-hello-world:latest
```

Após o push, entregue na EBAC o link do repositório da imagem no Docker Hub.
