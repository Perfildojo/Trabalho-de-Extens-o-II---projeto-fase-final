
---

### 2. `docs/API_REFERENCE.md`

Este arquivo fornece uma referência técnica para integração com o sistema, descrevendo endpoints, formatos de dados e exemplos de uso.

#### Exemplo de Conteúdo:

```markdown
# Referência da API

Esta documentação descreve os endpoints disponíveis para integração com o sistema **Mapa do Medo**.

## Endpoints

### 1. Listar Ocorrências

**Descrição**: Retorna uma lista de todas as ocorrências registradas.

**Endpoint**: `GET /api/ocorrencias`

**Exemplo de Requisição**:
```bash
curl -X GET http://localhost:5000/api/ocorrencias

Resposta:

[
    {
        "id": 1,
        "bairro": "Vergel do Lago",
        "ocorrencia": "Tiroteio",
        "rua": "Rua das Flores",
        "imagem": "imagens/AgADBAxU5QABe0-1.jpg"
    },
    {
        "id": 2,
        "bairro": "Benedito Bentes",
        "ocorrencia": "Roubo",
        "rua": "Avenida Principal",
        "imagem": "Sem imagem"
    }
]

2. Adicionar Ocorrência

Descrição: Registra uma nova ocorrência.

Endpoint: POST /api/ocorrencias

Exemplo de Requisição:

curl -X POST http://localhost:5000/api/ocorrencias \
-H "Content-Type: application/json" \
-d '{
    "bairro": "Vergel do Lago",
    "ocorrencia": "Tiroteio",
    "rua": "Rua das Flores",
    "imagem": "imagens/AgADBAxU5QABe0-1.jpg"
}'

Resposta:

{
    "id": 3,
    "mensagem": "Ocorrência registrada com sucesso!"
}

3. Previsão de Ocorrências
Descrição: Retorna uma previsão de ocorrências com base em dados históricos.

Endpoint: POST /api/previsao

Exemplo de Requisição:

curl -X POST http://localhost:5000/api/previsao \
-H "Content-Type: application/json" \
-d '{
    "bairro": "Vergel do Lago",
    "mes": 10,
    "ano": 2023
}'

Resposta:

{
    "bairro": "Vergel do Lago",
    "previsao": "Alto risco de roubos"
}

