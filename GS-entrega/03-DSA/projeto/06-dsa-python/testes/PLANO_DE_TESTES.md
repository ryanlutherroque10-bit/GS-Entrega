# Plano de testes, evidências e demonstração

Execução registrada em 16/11/2026, Windows 11, Python 3.14. Reproduza com:

```sh
python -m unittest discover -s testes -v
```

Resultado observado: **20 testes executados, 20 aprovados** (registro completo em `saida_testes.txt`).

- `test_main.py` — 9 testes da lista encadeada (inserção, busca, remoção, ordenação, pesquisa e ordenação sem diferenciar acentos, CSV, lista vazia).
- `test_csv_menu.py` — 6 testes de CSV defeituoso ou vazio e 5 testes que executam o menu real com entradas simuladas sobre um arquivo temporário.

## Evidências: entrada, resultado esperado e observado

| # | Situação | Entrada | Resultado esperado | Resultado observado | Evidência |
|---|---|---|---|---|---|
| 1 | Carga inicial | `dados/servicos.csv` com 5 registros | Informa 5 serviços carregados | "5 serviço(s) carregado(s)" | `saida_demonstracao.txt`, demo 1 |
| 2 | Consulta por ID existente | opção 2, ID `1` | Exibe o registro 1 | Exibiu "Tarifa Social de Energia" | demo 1 |
| 3 | Consulta por ID inexistente | ID `99` | Avisa que não encontrou | `buscar_id(99)` devolve `None`; o menu informa a ausência | `test_insercao_e_busca_por_id`, `saida_menu.txt` |
| 4 | Pesquisa por título/categoria | opção 3, `energia` | Lista registros com o termo, sem diferenciar maiúsculas | Exibiu os registros de energia | demo 1, `test_pesquisa_por_titulo_ou_categoria_sem_case` |
| 5 | Pesquisa sem resultado | opção 3, `xyz` | "Nenhum resultado para essa busca." | Igual ao esperado | demo 1 |
| 6 | Cadastro | opção 1, ID `6` e cinco campos | "Serviço cadastrado." e gravação no CSV | Igual ao esperado | demo 1, `test_crud_completo_pelo_menu` |
| 7 | ID duplicado | opção 1, ID `6` de novo | Recusa e mantém a lista | "Esse ID já está cadastrado." | demo 1, `test_rejeita_id_duplicado_e_nao_positivo` |
| 8 | Atualização | opção 4, ID `6`, novos campos | "Serviço atualizado." | Igual ao esperado | demo 1 |
| 9 | Ordenação (Insertion Sort) | opção 7 | Títulos em ordem alfabética | Ordem alfabética exibida | demo 1, `test_insertion_sort_por_titulo` |
| 10 | Indicador por categoria | opção 8 | Total e quantidade por categoria | Total e categorias exibidos | demo 1 |
| 11 | Exclusão | opção 5, ID `6` | "Serviço excluído." | Igual ao esperado | demo 1, `test_remocao_inicio_meio_fim_e_nao_encontrado` |
| 12 | Exclusão de ID inexistente | opção 5, ID `99` | Nada é excluído | "ID inexistente; nada foi excluído." | demo 1 |
| 13 | Entrada inválida para ID | opção 2, `abc` | Mensagem de erro e retorno ao menu | "Digite um inteiro positivo válido." | demo 1 |
| 14 | Opção inválida | `9` | "Opção inválida." | Igual ao esperado | demo 1 |
| 15 | Persistência | encerrar e reabrir | Dados permanecem | 5 registros recarregados | demo 2, `test_csv_persistencia` |
| 16 | CSV com linha incompleta | linha `9;Categoria` no arquivo | Erro com o número da linha; arquivo intacto; programa encerra | "Registro inválido na linha 7: faltam os campos…"; hash SHA-1 do arquivo igual antes e depois | demo 3, `test_csv_danificado_nao_e_sobrescrito` |
| 17 | CSV com coluna a mais, campo vazio, ID não numérico, ID repetido, cabeçalho errado | arquivos temporários | `ValueError` com a linha e o motivo | Igual ao esperado | `TestCargaCsvInvalido` |
| 18 | Lista vazia | opções 2 a 8 sem registros | "Lista vazia." em cada operação e aviso na análise | 6 avisos de lista vazia e "Não há categorias para resumir." | demo 4, `test_menu_com_lista_vazia` |
| 19 | Pesquisa sem acento | `saude`, `ENERGÍA` | Encontra "Saúde" e "Energia" | Igual ao esperado | `test_pesquisa_ignora_acentos` |
| 20 | Ordenação com acento e maiúsculas | zebra, Água, banco, Banco, abacate | abacate, Água, banco, Banco, zebra (estável) | Igual ao esperado | `test_insertion_sort_ignora_acentos_e_maiusculas` |
| 21 | CSV vazio | arquivo com 0 bytes ou só espaços | Começa com a lista vazia | 0 registros carregados | `test_arquivo_vazio_resulta_em_lista_vazia` |
| 22 | ID com dígitos demais | ID com 5000 dígitos e com 10 dígitos | "Digite um inteiro positivo válido." e CSV intacto | Igual ao esperado | `test_id_com_digitos_demais_e_recusado_com_mensagem_clara` |
| 23 | Entrada interrompida | Ctrl+C ou fim da entrada no menu | Salva e encerra sem erro técnico | "Entrada encerrada. Dados salvos." | `test_fim_da_entrada_ou_ctrl_c_salva_e_sai_sem_erro` |

`saida_demonstracao.txt` é a saída real do programa executado em uma cópia temporária dos dados, com as entradas enviadas pela entrada padrão (por isso as respostas digitadas não aparecem ao lado das perguntas). O CSV do repositório não foi alterado pelas demonstrações.

### Correção registrada em 16/11/2026

Antes da correção, um CSV com cabeçalho correto e uma linha incompleta (`1;Categoria`) causava `AttributeError` na carga, porque o código chamava `.strip()` em um campo ausente. A falha foi reproduzida em arquivo temporário com o código anterior. Agora cada linha é validada antes do uso, o erro informa a linha e o motivo, e, se a carga falhar, o programa encerra antes do menu sem gravar nada, preservando o arquivo para correção manual.

## Roteiro da demonstração

A demonstração prática é feita pela equipe, ao vivo ou gravada, conforme a orientação do professor (o enunciado não exige vídeo).

1. Mostrar o modelo `Servico`, a classe `No` e a lista `ListaServicos` no código.
2. Executar `python main.py` e apontar os itens carregados do CSV.
3. Consultar por ID (existente e inexistente), pesquisar por título/categoria e mostrar uma pesquisa sem resultado.
4. Cadastrar um item e tentar repetir o ID para demonstrar a validação.
5. Atualizar o registro, ordenar por título (explicando o Insertion Sort nos nós) e exibir a análise por categoria.
6. Excluir o registro; tentar excluir um ID inexistente; digitar uma opção e um ID inválidos.
7. Encerrar, reabrir e confirmar que as alterações permaneceram no CSV.
8. Explicar a busca linear, o Insertion Sort e a tabela Big-O de `docs/ANALISE_COMPLEXIDADE.md`.

Não incluir dados pessoais reais; os registros de exemplo são fictícios.
