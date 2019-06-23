import load as l
import random as rd
import datetime

debug=False

rd.seed(1)

Q=[200,400,800]

instancias = l.load("data\\capmst2.txt").instances
class cluster:
    def __init__(self):
        self.nodes = []
        self.peso = 0

def geraSolucaoViavel(instancia, restricao, randomFirst=True, randomAll=False):
    nClusters = 0
    clusters = {}
    vertices = {}
    nVerticesInseridos = 0
    for i in range(0,instancia.pesos.shape[0]+1):
        vertices[i]=False

    linhas = instancia.pesos.shape[0]

    restricaoRestante = restricao
    minCusto = instancia.custoMaximo()+1
    noCentral = instancia.custos.shape[1]-1
    noMaisProximo = -1

    clusters[1]=cluster()
    clusters[1].peso = 0
    nClusters = 1
    nVerticesInseridos = 0

    if randomFirst or randomAll:
        ultimoInserido = getRandomNode(vertices)
        nVerticesInseridos += 1
        pesoInstancia = instancia.pesos[ultimoInserido]
        restricaoRestante -= pesoInstancia 
        vertices[ultimoInserido]=True
        clusters[nClusters].nodes.append(ultimoInserido)
        clusters[nClusters].peso += pesoInstancia 
    else:
        ultimoInserido = noCentral
    while nVerticesInseridos < instancia.tamanho-1:
        menorCustoEncontrado = minCusto
        noEscolhido = -1
        if randomAll:
            noEscolhido = getRandomNode(vertices)
            menorCustoEncontrado = instancia.custos[noEscolhido,ultimoInserido]
        else:
            for i in range(linhas):
                if (vertices[i]==False) and (i != noCentral):
                    custoIparaUltimoInserido = instancia.custos[i,ultimoInserido]
                    if (menorCustoEncontrado > custoIparaUltimoInserido) and (custoIparaUltimoInserido > 0):
                        noEscolhido = i
                        menorCustoEncontrado = custoIparaUltimoInserido
        pesoInstancia = instancia.pesos[noEscolhido]
        if (noEscolhido < 0):
            break
        if (pesoInstancia > restricaoRestante):
            restricaoRestante = restricao
            nClusters+=1
            ultimoInserido = noCentral
            clusters[nClusters]=cluster()
            clusters[nClusters].peso = 0
        else:
            nVerticesInseridos += 1
            restricaoRestante -= pesoInstancia 
            vertices[noEscolhido]=True
            clusters[nClusters].nodes.append(noEscolhido)
            clusters[nClusters].peso += pesoInstancia 
            ultimoInserido = noEscolhido

    return clusters

def prim(g,instancia):
    g = g.copy()
    selecionados = []
    custoMST = 0
    
    minCusto = instancia.custoMaximo()+1
    selecionados.append(g[0])
    g.pop(0)
    
    for i in range(0, len(g)):
        maisProximo = -1
        menorCusto = minCusto
        arestaAdicionada = ""
        for j in range(0, len(selecionados)):
            for k in range(0,len(g)):
                custoJK = instancia.custos[selecionados[j],g[k]]
                if debug:
                    print("custo - "+str(selecionados[j])+" para "+str(g[k])+ " = "+str(custoJK))
                if (custoJK < menorCusto):
                    menorCusto = custoJK
                    maisProximo = g[k]
                    maisProximoIndice = k
                    arestaAdicionada = str(selecionados[j])+"---"+str(g[k])
        selecionados.append(maisProximo)
        custoMST += menorCusto
        g.pop(maisProximoIndice )
        if debug:
            print("_______________"+arestaAdicionada)

    return custoMST

def getRandomNode(vertices):
    nVertices = len(vertices)
    contador = 0
    for i,v in vertices.items():
        if v==False:
            contador+=1
    randvalue=-1
    if (contador>1):
        contador = rd.randint(1,contador-1)
        randvalue = contador
    else:
        contador = 1

    for i,v in vertices.items():
        if v==True:
            continue
        contador-=1
        if (contador==0):
            return i
    
    for i,v in vertices.items():
        if v==False:
            return i
solucoes = []
c = geraSolucaoViavel(instancias["50_1"], Q[0], False, False)
solucoes.append(c)

tempo = datetime.datetime.now()
for i in range(0,10000):
    solucoes.append(geraSolucaoViavel(instancias["50_1"], Q[0], False, True))
print(str(datetime.datetime.now()-tempo))
print(prim(c[1].nodes,instancias["50_1"]))



i=0




