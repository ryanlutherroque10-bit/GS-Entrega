# Documentação técnica

## Modelo dos dados

`Servico` é uma dataclass com ID inteiro único, categoria, título, descrição, requisitos e local/canal. Cada campo textual é obrigatório. O CSV utiliza cabeçalho e `;` como delimitador, com suporte a acentos por UTF-8.

## Lista encadeada

A classe `No` armazena um `Servico` e uma referência `proximo`. `ListaServicos.inicio` aponta para o primeiro nó. Inserção percorre até o fim. A busca por ID percorre os nós sequencialmente. Remoção religa o nó anterior ao seguinte; quando remove o primeiro elemento, atualiza `inicio`. Python gerencia a liberação da memória quando nós deixam de ser referenciados.

## Algoritmos

`buscar_id` faz busca linear. `pesquisar` procura uma substring no título ou categoria, sem diferenciar maiúsculas/minúsculas nem acentos ("saude" encontra "Saúde"). As duas operações comparam textos pela função `normalizar`, que remove os acentos (decomposição Unicode NFD) e aplica `casefold`. `ordenar_por_titulo` implementa Insertion Sort na lista: retira cada nó e o insere na posição correta da lista já ordenada, comparando os títulos normalizados: "Água" fica entre "abacate" e "banco", e não depois de "zebra". A ordenação é estável (títulos iguais mantêm a ordem de entrada). Não usa `sort`, `sorted` ou outro algoritmo pronto para ordenar registros.

## Menu e persistência

O menu fornece cadastro, consulta por ID, pesquisa por atributo, atualização, exclusão, listagem, ordenação, análise e encerramento. Erros de formato, campos vazios, ID duplicado, consultas sem resultado e lista vazia são tratados com mensagens. O CSV é salvo após alterações e ao encerrar. Caminho usado: `dados/servicos.csv` dentro da pasta do projeto.

Na carga, cada linha do CSV é validada antes de virar um registro: quantidade de colunas, campos ausentes ou vazios, ID inteiro positivo e ID não repetido. Um problema gera erro com o número da linha e o motivo. Se a carga inicial falhar, o programa informa o erro e encerra antes do menu, sem gravar nada: o arquivo com defeito fica preservado para ser corrigido ou substituído por uma cópia íntegra. Se o arquivo não existir ou estiver vazio, o programa começa com a lista vazia. IDs têm até 9 dígitos; valores maiores são recusados com a mesma mensagem de ID inválido. Se a entrada terminar de repente (Ctrl+C, Ctrl+Z ou fim da entrada), o programa salva a lista e encerra sem mostrar erro técnico.

## Escopo e cuidados

Os registros fornecidos são exemplos fictícios e não devem ser interpretados como orientação oficial. Antes de apresentar conteúdo ao público, confirmar fatos e documentos em fontes oficiais e registrar os links e as datas de consulta. O protótipo não coleta dados pessoais.
