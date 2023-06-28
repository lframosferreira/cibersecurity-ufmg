# Projeto de programação 2

## Cibersegurança - 2023/1 - Prof. Michele Nogueira

## Universidade Federal de Minas Ferais

### Luís Felipe Ramos Ferreira - 2019022553

#### [Repositório](https://github.com/lframosferreira/cibersecurity-ufmg/tree/main/project_2/)

- Parte 1 - _Exploits_ dos alvos 1 e 2

  A parte 1 do projeto de programação 2 consistiu em escrever _exploits_ que tirassem proveito das vulnerabilidades presentes nos alvos 1 e 2. Em particular, os alvos em questão
  são códigos escritos em C que contêm vulnerabilidades devido à possibilidade
  de causar um _buffer overflow_.

  No alvo 1, a função _strcpy_ é utilizada para armazenar o conteúdo da variável _arg_ em _out_. Como _strcpy_ não faz nenhuma checagem de limite de tamanho de _string_ de cópia, o que permite um _overflow_ no momento
  da cópia. Essa vulnerabilidade permite que um _shellcode_ seja introduzido como entrada para o _script_ e, assim, seja possível ter acesso à um _shell root_.

  No alvo 2, o problema está na implementação da função auxiliar _nmemcpy_. Mais especificamente, na função que exerce a cópia do conteúdo de uma _string_ em outra, apesar de existir uma checagem de tamanho das _strings_ de cópia, o laço _for_ possui um _typo_. A condição de limite imposta no laço é **i <= len** e não **i < len**. Desse modo, um _byte_ a mais é sempre lido na cópia da de uma _string_ em outra, o que, mais uma vez, permite que o _buffer overflow_ seja explorado e um _shellcode_ que concede acessos privilegiados a um _shell root_ seja possível.

- Parte 2 - Alvos 3, 4, e 5

  O alvo 3 parece conter mais um caso de vulnerabilidade devido a _overflow_, mas dessa vez relacionado a números
  inteiros, que pode ser exlorado na função _foo_. Em particular, na função, há uma checagem, antes da cópia, se a variável _count_ é menor do que a constante definida _MAX_WIDGETS_. No entanto, o valor de _count_ pode ser manipulado para que essa condição seja aceita mesmo quando não deveria. Uma estratégia seria utilizar dos conceitos de tipos de inteiros com e sem sinais em C para alterar o tamanho do _buffer_ e assim inserir o _shellcode_ no programa.
  
  O alvo 4 sofre da mesma vulnerabilidade do alvo 2. O _typo_ presente no laço _for_ feito na função auxiliar de cópia de _strings_ permite que um _byte_ extra seja adicionado na cópia. Ademais, a manipulação dos ponteiros da função _foo_, após o _buffer overflow_, pode permitir que o ponteiro de execução seja direcionado para o _shellcode_ já citado.

  O alvo 5 também sofre de uma vulnerabilidade de _stack overflow_ 

- Parte 3 - Vulnerabilidades em um programa do mundo real (bdstar)

  O _backtrace_ e os comentários estão presentes no _README_ do diretório _fuzz_, como solicitado. O _link_ com redirecionamento para o repositório público no _GitHub_ está disposto nos _headers_ deste arquivo.
