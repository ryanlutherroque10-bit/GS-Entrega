# Análise de complexidade

Considere `n` como o número de registros; `m` como o tamanho do texto comparado.

| Operação | Implementação | Tempo | Espaço auxiliar |
|---|---|---:|---:|
| Inserir no fim | Busca linear do ID para recusar duplicados e, depois, percurso até o último nó (duas passagens) | O(n) | O(1), além do novo nó |
| Consultar por ID | Busca linear | O(n) | O(1) |
| Pesquisar título/categoria | Verifica cada registro, normaliza os textos (sem acentos) e compara substrings | O(n × m) | O(k) para lista de resultados, sendo `k` o número encontrado |
| Atualizar | Busca linear e substituição dos campos do nó | O(n) | O(1) |
| Remover por ID | Busca linear e religação de referências | O(n) | O(1) |
| Percorrer/listar/contar | Visita cada nó | O(n) | O(1) para a iteração |
| Insertion Sort por título | Insere nós na lista já ordenada, comparando títulos normalizados | O(n² × m) pior caso; O(n × m) melhor caso | O(m) por comparação |
| Resumo por categoria | Uma passagem com dicionário de contagem | O(n) médio | O(c), para `c` categorias |

A remoção é O(1) depois de localizar o nó, mas a operação completa inclui uma busca O(n). O Insertion Sort preserva os nós e não cria vetor auxiliar; sua complexidade quadrática é adequada ao catálogo pequeno do protótipo. Busca binária não foi usada, pois lista encadeada não oferece acesso aleatório eficiente.

A inserção faz duas passagens pela lista (verificação de ID duplicado e localização do último nó); 2n passos continuam sendo O(n). Carregar o CSV insere um registro por vez, com essa verificação em cada um, portanto a carga de `n` linhas custa O(n²); salvar percorre a lista uma vez, O(n). `len(lista)` também percorre os nós, O(n), pois a lista não guarda um contador.

Cada comparação de texto normaliza os títulos (remove acentos e aplica `casefold`), o que custa O(m) para títulos de tamanho `m`. Como os títulos são curtos, `m` é pequeno e o comportamento continua dominado por n² no Insertion Sort e por n na pesquisa; o espaço extra é só a cópia temporária do texto normalizado, sem vetor auxiliar de registros.
