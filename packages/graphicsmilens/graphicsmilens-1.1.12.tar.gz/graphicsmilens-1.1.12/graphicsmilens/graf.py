import matplotlib.pyplot as plt
import pandas as pd

class Graficos():
    """ Classe usada para criar graficos
    
    Classe que contém as função para criar graficos modelo pizza,barra,ponto e linha
    
    Attributes
    ----------
    arq : csv
        Variavel que armazenara um arquivo csv
        
    Methods
    -------
    lerArq()
        Funcao responsavel por ler um arquivo definido
    linha()
        Funcao que criara um grafico modelo linha
    barra()
        Funcao que criara um grafico modelo barra
    pizza()
        Funcao que criara um grafico modelo pizza
    ponto()
        Funcao que criara um grafico modelo ponto
        
    """
    def __init__(self,arq):
        """ 
        Parameters
        ----------
        
        arq : csv
            Variavel que armazenara um arquivo csv
        """
        self.arq = arq
        self.lerAqr()
        
    def lerAqr(self):
        """
        Funcao responsavel por ler um arquivo definido pelo usuario
        
        Essa funcao recebe o arquivo com os dados para criacao do grafico 
        """
        
        try:
            self.arqCont = pd.read_csv(self.arq)
        except Exception as e:   
            print(e)       

    def linha(self,x,y,legenda,tit,xlabel,ylabel):
        """
        Funcao responsavel por realizar a criacao do grafico modelo linha
        
        ...
        
        Parameters
        ----------
        
        x : int
            variavel que pegara a primeira coluna do arquivo
        y : int
            variavel que pegara a segunda coluna do arquivo
        legenda : string
            variavel responsavel por legendar o grafico
        tit : string
            variavel responsavel por colocar um titulo no grafico
        xlabel : string
            variavel que vai armazena um rotulo para o eixo x
        ylabel : string
            variavel que vai armazena um rotulo para o eixo y 
        """
        plt.plot(sorted(self.arqCont[x]),sorted(self.arqCont[y]))
        plt.title(tit)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(legenda)
        plt.show()

    def barra(self,x,y,legenda,tit,xlabel,ylabel):
        """
        Funcao responsavel por realizar a criacao do grafico modelo barra
        
        ...
        
        Parameters
        ----------
        
        x : int
            variavel que pegara a primeira coluna do arquivo
        y : int
            variavel que pegara a segunda coluna do arquivo
        legenda : string
            variavel responsavel por legendar o grafico
        tit : string
            variavel responsavel por colocar um titulo no grafico
        xlabel : string
            variavel que vai armazena um rotulo para o eixo x
        ylabel : string
            variavel que vai armazena um rotulo para o eixo y 
        """
        plt.bar(self.arqCont[x],self.arqCont[y],color = '#FF6B1A')
        for i,valor in enumerate((self.arqCont[y])):
            plt.text(i,valor+1,str(valor),ha='center')
        plt.title(tit)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(legenda)
        plt.show()

    def pizza(self,x,tit,labels,cores='-'):
        
        """
        Funcao responsavel por realizar a criacao do grafico modelo pizza
        
        ...
        
        Parameters
        ----------
        
        x : int
            variavel que pegara coluna do arquivo
        tit : string
            variavel responsavel por colocar um titulo no grafico
        labels : list
            variavel que vaia armazena uma lista com as etiquetas do grafico
        cores : list,opcional
            variavel que vai armazena a lista de cores definida  pelo usuario 
        """
        tam = len(self.arqCont[x])
        print(tam)
        if cores != '-':
            if tam != len(cores) or tam != len(labels):
                print('Valores incompatíveis!')
            else: 
                patches = plt.pie(self.arqCont[x],colors=cores,labels=labels,autopct='%1.1f%%' )
                """ plt.legend(patches, , loc="best"') """
                plt.title(tit)
                plt.show()
        elif cores == '-':
            patches = plt.pie(self.arqCont[x],labels=labels,autopct='%1.1f%%' )
            plt.title(tit)
            plt.show()
        
    def ponto(self,x,y,legenda,tit,xlabel,ylabel):
        """
        Funcao responsavel por realizar a criacao do grafico modelo ponto
        
        ...
        
        Parameters
        ----------
        
        x : int
            variavel que pegara a primeira coluna do arquivo
        y : int
            variavel que pegara a segunda coluna do arquivo
        legenda : string
            variavel responsavel por legendar o grafico
        tit : string
            variavel responsavel por colocar um titulo no grafico
        xlabel : string
            variavel que vai armazena um rotulo para o eixo x
        ylabel : string
            variavel que vai armazena um rotulo para o eixo y 
        """
        plt.scatter(sorted(self.arqCont[x]),sorted(self.arqCont[y]),marker = '*', color = 'blue')
        plt.title(tit)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(legenda)
        plt.show()




