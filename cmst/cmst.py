import load as l
import random as rd
import datetime

debug=False
rd.seed(1)

class cluster:
    def __init__(self):
        self.nodes = []
        self.peso = 0
        self.mstCusto = 0
class clustersObject:
    def __init__(self):
        self.lista    = {}
        self.mstTotal = 0
        self.randomOnlyFirst = False
        self.randomAll       = False
        self.randomAllFirst  = False

def geraSolucaoViavel(instancia, restricao, randomOnlyFirst=True, randomAll=False, randomAllFirst=False):
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

    if randomOnlyFirst or randomAll or randomAllFirst:
        ultimoInserido = getRandomNode(vertices)
        nVerticesInseridos += 1
        pesoInstancia = instancia.pesos[ultimoInserido]
        restricaoRestante -= pesoInstancia 
        vertices[ultimoInserido]=True
        clusters[nClusters].nodes.append(ultimoInserido)
        clusters[nClusters].peso += pesoInstancia 
    else:
        ultimoInserido = noCentral
    first = False
    while nVerticesInseridos < instancia.tamanho-1:
        menorCustoEncontrado = minCusto
        noEscolhido = -1
        if randomAll:
            noEscolhido = getRandomNode(vertices)
            menorCustoEncontrado = instancia.custos[noEscolhido,ultimoInserido]
        elif randomAllFirst and first:
            noEscolhido = getRandomNode(vertices)
            menorCustoEncontrado = instancia.custos[noEscolhido,ultimoInserido]
            first = False
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
            first = True
        else:
            nVerticesInseridos += 1
            restricaoRestante -= pesoInstancia 
            vertices[noEscolhido]=True
            clusters[nClusters].nodes.append(noEscolhido)
            clusters[nClusters].peso += pesoInstancia 
            ultimoInserido = noEscolhido
    mstTotal = 0
    for i,c in clusters.items():
        c.mstCusto = prim(c.nodes,instancia)
        mstTotal+=c.mstCusto
    retorno = clustersObject()
    retorno.lista=clusters
    retorno.mstTotal = mstTotal
    retorno.randomAll = randomAll
    retorno.randomAllFirst = randomAllFirst
    retorno.randomOnlyFirst = randomOnlyFirst

    return retorno

def prim(g,instancia):
    g = g.copy()
    noCentral = instancia.tamanho-1
    selecionados = []
    custoMST = 0
    minCusto = instancia.custoMaximo()+1
    menorCustoNoCentral=minCusto 
    #adiciona o menor caminho ao no central no calculo do custo do cluster
    for i in range(0, len(g)):
        custoNoCentralI = instancia.custos[noCentral,g[i]]
        if custoNoCentralI < menorCustoNoCentral:
            menorCustoNoCentral = custoNoCentralI

    custoMST = menorCustoNoCentral 
    
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

def geraPopulacaoInicial(instancia, Q, quantidade):
    solucoes = []
    s = geraSolucaoViavel(instancia, Q, False, False)
    solucoes.append(s)
    quantidade -= 1 
    for i in range(0,int(quantidade/2)):
        s = geraSolucaoViavel(instancia, Q, False, False, True)
        solucoes.append(s)
        #s = geraSolucaoViavel(instancia, Q, False, True, False)
        #solucoes.append(s)
        s = geraSolucaoViavel(instancia, Q, True, False, False)
        solucoes.append(s)
    minValue = 1000000000
    minI = -1
    maxValue = -1
    maxI = -1
    for s in solucoes:
        if s.mstTotal<minValue:
            minValue=s.mstTotal
            minI = s
            #print ("menor valor mstTotal="+str(minValue) + " randomAll:" + str(minI.randomAll)+ " randomOnlyFirst:" + str(minI.randomOnlyFirst)+ " randomAllFirst:" + str(minI.randomAllFirst))
        #if s.mstTotal>maxValue:
        #    maxValue=s.mstTotal
        #    maxI = s
            #print ("MAIOR valor mstTotal="+str(maxValue) + " randomAll:" + str(maxI.randomAll)+ " randomOnlyFirst:" + str(maxI.randomOnlyFirst)+ " randomAllFirst:" + str(maxI.randomAllFirst))
    solucoesFinal = []
    for s in solucoes:
        if (s.mstTotal<2*minValue):
            solucoesFinal.append(s)

    minValue = 1000000000
    minI = -1
    maxValue = -1
    maxI = -1
    for s in solucoesFinal:
        if s.mstTotal<minValue:
            minValue=s.mstTotal
            minI = s
            if debug:
                print ("menor valor mstTotal="+str(minValue) + " randomAll:" + str(minI.randomAll)+ " randomOnlyFirst:" + str(minI.randomOnlyFirst)+ " randomAllFirst:" + str(minI.randomAllFirst))
        #if s.mstTotal>maxValue:
        #    maxValue=s.mstTotal
        #    maxI = s
            #print ("MAIOR valor mstTotal="+str(maxValue) + " randomAll:" + str(maxI.randomAll)+ " randomOnlyFirst:" + str(maxI.randomOnlyFirst)+ " randomAllFirst:" + str(maxI.randomAllFirst))

    return solucoesFinal

def crossover():
    i=0
def mutation():
    i=0
def LS():
    i=0

def executa(quantidadeSolucoesIniciais, quantidadeGeracoes):
    Q=[200,400,800]

    instancias = l.load("data\\capmst2.txt").instances

    for instancia in instancias:
        for q in range(0,len(Q)):
            print ("tamanho instancia: "+str(instancias[instancia].tamanho)+" - id "+str(instancias[instancia].id)+" - "+str(Q[q]))
            tempo = datetime.datetime.now()
            solucoes = geraPopulacaoInicial(instancias[instancia], Q[q], quantidadeSolucoesIniciais)
            print(str(datetime.datetime.now()-tempo))
            print (len(solucoes))

executa(1000,1000)




