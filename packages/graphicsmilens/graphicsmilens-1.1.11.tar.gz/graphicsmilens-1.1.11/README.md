# graphicsmilens

Pacote feito para criar gráficos (linha, ponto, barra e pizza) com diversos tipos de dados.

Bibliotecas que são utilizadas e já são instaladas ao baixar o pacote:
- pandas 
- matplotlib

## Instalação:

    pip install graphicsmilens

## Uso:

Inicialmente você realiza a importação do pacote e depois cria uma instância da classe criada passando como parâmetro o arquivo csv, em seguida, faz a chamada da função. Assim seu gráfico estará pronto.

### Barra

```
from graphicsmilens import Graficos
variavel = Graficos('nome_arquivo.csv')
variavel.barra('coluna1','coluna2',legenda = 'legenda', tit = 'Grafico de barra' , xlabel = 'x', ylabel = 'y')
```
### Linha

```
from graphicsmilens import Graficos
variavel = Graficos('nome_arquivo.csv')
variavel.linha('coluna1','coluna2',legenda='legenda do grafico',tit='titulo do grafico',xlabel='x',ylabel='y')
```

### Ponto

```
from graphicsmilens import Graficos
variavel = Graficos('nome_arquivo.csv')
variavel.ponto('coluna1','coluna2',legenda='legenda do grafico',tit='titulo do grafico',xlabel='x',ylabel='y')
```

### Pizza

```
from graphicsmilens import Graficos
variavel = Graficos('nome_arquivo.csv')
cores = ['red','green','black','pink','blue'] 
labels = [r'vendas', r'gastos',r'despesas', r'imoveis',r'aluguel']
variavel.pizza('coluna1','Gráfico de Vendas Lanchonete',labels,cores)
```

## Licença

O graphicsmilens é distribuído sob a [Licença MIT](https://choosealicense.com/licenses/mit/).Você é livre para usar, modificar e distribuir este pacote de acordo com os termos da licença.