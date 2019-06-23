import numpy as np
from enum import Enum

class fase(Enum):
    begining=1
    pesos=2
    custos=3
    lerTamanho=4

class instance:
    def __init__(self, id, t, p):
        self.id = id
        self.tamanho = t
        self.pesos = p
        self.custos = np.zeros([t,t],dtype=int)

    def pesoMaximo(self):
        return max(self.pesos)

    def custoMaximo(self):
        return np.amax(self.custos)

class load:
    def __init__(self, path):
        self.instances = {}
        pesos={}
        faseCarga = fase.begining
        faseTamanho = None
        faseId = None
        with open(path) as f: 
            for line in f: 
                if (line.find("--")>=0):
                    continue

                l = line.replace("\n","").replace(".dat","").rstrip(' ').lstrip(' ')
                if (line.find("priz")>=0):
                    faseCarga = fase.pesos
                    contador=0
                    faseTamanho = int(l.replace('priz','').replace('r',''))
                    if (faseTamanho not in pesos):
                        pesos[faseTamanho]=np.zeros([faseTamanho-1],dtype=int)
                        self.instances[str(faseTamanho)+"_1"]=instance(1,faseTamanho,pesos[faseTamanho])
                        self.instances[str(faseTamanho)+"_2"]=instance(2,faseTamanho,pesos[faseTamanho])
                        self.instances[str(faseTamanho)+"_3"]=instance(3,faseTamanho,pesos[faseTamanho])
                        self.instances[str(faseTamanho)+"_4"]=instance(4,faseTamanho,pesos[faseTamanho])
                        self.instances[str(faseTamanho)+"_5"]=instance(5,faseTamanho,pesos[faseTamanho])
                    continue
                
                elif (line.find("cm")>=0):
                    faseCarga = fase.lerTamanho
                    temp = l.replace("cm","").replace("r"," ").split(" ")
                    faseTamanho = int(temp[0])
                    faseId = int(temp[1])
                    contadorI=0
                    contadorJ=0
                    continue
                elif(faseCarga == fase.lerTamanho):
                    faseCarga = fase.custos
                    continue

                if (faseCarga == fase.pesos):
                    temp = l.split(" ")
                    for i in range(0,len(temp)):
                        pesos[faseTamanho][contador]=temp[i]
                        contador+=1
                else:
                    temp = l.split(" ")
                    for i in range(0,len(temp)):
                        if (contadorI==faseTamanho):
                            contadorI=0
                            contadorJ+=1
                            
                        self.instances[str(faseTamanho)+"_"+str(faseId)].custos[contadorJ,contadorI]=temp[i]
                        contadorI+=1
