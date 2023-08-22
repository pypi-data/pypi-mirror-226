import matplotlib.pyplot as plt
import pandas as pd

class Graficos():
    def __init__(self,arq):
        self.arq = arq
        self.lerAqr()
        
    def lerAqr(self):
        try:
            self.arqCont = pd.read_csv(self.arq)
        except Exception as e:   
            print(e)       #se der erro, ele para

    def linha(self,x,y,legenda,tit,xlabel,ylabel):
        plt.plot(sorted(self.arqCont[x]),sorted(self.arqCont[y]))
        plt.title(tit)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(legenda)
        plt.show()

    def barra(self,x,y,legenda,tit,xlabel,ylabel):
        plt.bar(self.arqCont[x],self.arqCont[y],color = '#FF6B1A')
        for i,valor in enumerate((self.arqCont[y])):
            plt.text(i,valor+1,str(valor),ha='center')
        plt.title(tit)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(legenda)
        plt.show()

    def pizza(self,x,tit,labels,cores='-'):
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
        plt.scatter(sorted(self.arqCont[x]),sorted(self.arqCont[y]),marker = '*', color = 'blue',label='Star')
        plt.title(tit)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(legenda)
        plt.show()




