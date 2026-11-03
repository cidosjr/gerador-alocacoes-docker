# Gerador de códigos de alocação

Aplicação web em Python + Flask, executada com Docker Compose.

## Requisitos
- Docker
- Docker Compose (plugin `docker compose`)

## Executar
No terminal, dentro da pasta do projeto:

```bash
docker compose up -d --build
```

Acesse no navegador:

http://localhost:5000

Para parar:

```bash
docker compose down
```

## Regras atuais
- Dias: 23, 24 e 25
- Locais: 03 e 04
- Salas: números de até três dígitos, completados com zero à esquerda
- Horários: 08, 10, 13, 16 e 19
- Sessões: A, B, C, D e E

São gerados 75 códigos por sala (3 dias × 1 local escolhido × 5 horários × 5 sessões).
Formato: `23, 03, 315, 16B`

A interface permite copiar os códigos e baixar um CSV.
