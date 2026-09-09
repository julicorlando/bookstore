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

A imagem é publicada automaticamente pelo GitHub Actions para:

```text
julicorlando/ebac-docker-hello-world:1.0
julicorlando/ebac-docker-hello-world:latest
```

O workflow utiliza o secret `DOCKERHUB_TOKEN` cadastrado em Repository secrets no GitHub. O usuário do Docker Hub está definido como `julicorlando` no próprio workflow.

## Link para entrega na EBAC

```text
https://hub.docker.com/r/julicorlando/ebac-docker-hello-world
```
