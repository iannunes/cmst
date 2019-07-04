import numpy as np
from enum import Enum
import collections
import sys

class fase(Enum):
    begining=1
    pesos=2
    custos=3
    lerTamanho=4

class instance:
    def __init__(self, id, t, p, tipo):
        self.id = id
        self.tamanho = t
        self.pesos = p
        self.custos = np.zeros([t,t],dtype=int)
        self.tipo = tipo
        self.custosOrdenados = {}

    def pesoMaximo(self):
        return max(self.pesos)

    def custoMaximo(self):
        return np.amax(self.custos)

    def getCustosOrdenados(self):
        if len(self.custosOrdenados)==0:
            for i in range(0, self.tamanho):
                self.custosOrdenados[i] = []
                for j in range(0, self.tamanho):
                    if i==j:
                        self.custosOrdenados[i].append(keyValue(j,sys.maxsize))
                    else:
                        self.custosOrdenados[i].append(keyValue(j,self.custos[i,j]))
            for i in range(0, self.tamanho):
                self.custosOrdenados[i].sort(key=lambda x: x.value, reverse=False)

        return self.custosOrdenados
class keyValue:
    def __init__(self, key, value):
        self.key = key
        self.value = value 
class load:
    def __init__(self, type, path):
        if type=="cm":
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
                            self.instances[str(faseTamanho)+"_1"]=instance(1,faseTamanho,pesos[faseTamanho],"cm")
                            self.instances[str(faseTamanho)+"_2"]=instance(2,faseTamanho,pesos[faseTamanho],"cm")
                            self.instances[str(faseTamanho)+"_3"]=instance(3,faseTamanho,pesos[faseTamanho],"cm")
                            self.instances[str(faseTamanho)+"_4"]=instance(4,faseTamanho,pesos[faseTamanho],"cm")
                            self.instances[str(faseTamanho)+"_5"]=instance(5,faseTamanho,pesos[faseTamanho],"cm")
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
        elif type=="tcte":
            self.instances = {}
            pesos={}
            faseCarga = fase.begining
            faseTamanho = None
            faseId = None
            tipo = ""
            with open(path) as f: 
                for line in f: 
                    if (line.find("--")>=0):
                        continue

                    l = line.replace("\n","").replace(".txt","").replace(".dat","").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").rstrip(' ').lstrip(' ')
                    if ((l.find("te")>=0) or (l.find("tc")>=0)):
                        faseCarga = fase.lerTamanho
                        contador=0
                        tipo = "tc"
                        if l.find("te")>=0:
                            tipo="te"
                        faseTamanho = int(l.replace('te','').replace('tc','').replace('-',' ').split(" ")[0])
                        faseId = int(l.replace('te','').replace('tc','').replace('-',' ').split(" ")[1])
                        contadorI=0
                        contadorJ=0
                        if (faseTamanho not in pesos):
                            pesos[faseTamanho]=np.zeros([faseTamanho],dtype=int)
                            for i in range(0,faseTamanho):
                                pesos[faseTamanho][i]=1

                            self.instances["tc"+str(faseTamanho)+"_1"]=instance(1,faseTamanho+1,pesos[faseTamanho],tipo)
                            self.instances["tc"+str(faseTamanho)+"_2"]=instance(2,faseTamanho+1,pesos[faseTamanho],tipo)
                            self.instances["tc"+str(faseTamanho)+"_3"]=instance(3,faseTamanho+1,pesos[faseTamanho],tipo)
                            self.instances["tc"+str(faseTamanho)+"_4"]=instance(4,faseTamanho+1,pesos[faseTamanho],tipo)
                            self.instances["tc"+str(faseTamanho)+"_5"]=instance(5,faseTamanho+1,pesos[faseTamanho],tipo)
                            self.instances["te"+str(faseTamanho)+"_1"]=instance(1,faseTamanho+1,pesos[faseTamanho],tipo)
                            self.instances["te"+str(faseTamanho)+"_2"]=instance(2,faseTamanho+1,pesos[faseTamanho],tipo)
                            self.instances["te"+str(faseTamanho)+"_3"]=instance(3,faseTamanho+1,pesos[faseTamanho],tipo)
                            self.instances["te"+str(faseTamanho)+"_4"]=instance(4,faseTamanho+1,pesos[faseTamanho],tipo)
                            self.instances["te"+str(faseTamanho)+"_5"]=instance(5,faseTamanho+1,pesos[faseTamanho],tipo)
                        continue
                
                    elif(faseCarga == fase.lerTamanho):
                        faseCarga = fase.custos
                        continue

                    else:
                        temp = l.split(" ")
                        for i in range(0,len(temp)):
                            if (contadorI==faseTamanho+1):
                                contadorI=0
                                contadorJ+=1
                            
                            self.instances[tipo+str(faseTamanho)+"_"+str(faseId)].custos[contadorJ,contadorI]=temp[i]
                            contadorI+=1
