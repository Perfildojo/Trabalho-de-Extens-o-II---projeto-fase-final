### Este projeto está licenciado sob a MIT License.


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