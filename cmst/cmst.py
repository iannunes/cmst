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
        self.vertices = {}
        self.mstTotal = 2000000000
        self.randomOnlyFirst = False
        self.randomAll       = False
        self.randomAllFirst  = False
        self.LS              = False
        self.crossover       = False
        self.mutation        = False

def geraSolucaoViavel(instancia, restricao, randomOnlyFirst=True, randomAll=False, randomAllFirst=False):
    nClusters = 0
    clusters = {}
    vertices = {}
    retorno = clustersObject()

    for i in range(0,instancia.pesos.shape[0]):
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
        retorno.vertices[ultimoInserido]=nClusters
    else:
        ultimoInserido = noCentral
    first = False
    while nVerticesInseridos < instancia.tamanho:
        menorCustoEncontrado = minCusto
        noEscolhido = -1
        if randomAll:
            noEscolhido = getRandomNode(vertices)
            menorCustoEncontrado = instancia.custos[noEscolhido,ultimoInserido]
        elif randomAllFirst and first:
            noEscolhido = getRandomNode(vertices)
            #menorCustoEncontrado = instancia.custos[noEscolhido,ultimoInserido]
            first = False
        else:
            for i in range(linhas):
                if (vertices[i]==False) and (i != noCentral):
                    custoIparaUltimoInserido = instancia.custos[i,ultimoInserido]
                    if (menorCustoEncontrado > custoIparaUltimoInserido) and (custoIparaUltimoInserido >= 0):
                        noEscolhido = i
                        menorCustoEncontrado = custoIparaUltimoInserido
        if ((noEscolhido == None) or (noEscolhido < 0)):
            break

        pesoInstancia = instancia.pesos[noEscolhido]
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
            retorno.vertices[noEscolhido]=nClusters
        #if contaNosInseridos(clusters)!=nVerticesInseridos:
        #    stop=1

    #for i,c in clusters.items():
    #    for j in (c.nodes):
    #        retorno.vertices[j]=i

    retorno.lista=clusters
    retorno.mstTotal = calculaTotalMST(clusters,instancia)
    retorno.randomAll = randomAll
    retorno.randomAllFirst = randomAllFirst
    retorno.randomOnlyFirst = randomOnlyFirst

    if debug:
        print(str(linhas)+" - "+str(len(retorno.vertices)))

    return retorno

def contaNosInseridos(clusters):
    contador = 0
    for i,c in clusters.items():
        contador+= len(c.nodes)
    return contador

def geraSolucaoViavel2(instancia, restricao):
    # escolher o primeiro vertice aleatoriamente para cada cluster
    # para o proximo vertice, escolher o que minimiza a distancia entre o central e o primeiro
    # para os proximos escolher o vertice mais proximo do corte
    # ate a capacidade

    vertices = {}
    retorno = clustersObject()
    for i in range(0,instancia.pesos.shape[0]):
        vertices[i]=False

    minCusto = instancia.custoMaximo()+1
    noMaisProximo = -1

    noCentral = instancia.tamanho-1
    nClusters = 0
    nVerticesInseridos = 0

    while True:
        nClusters += 1
        retorno.lista[nClusters]=cluster()
        retorno.lista[nClusters].peso = 0
    
        primeiroInserido = getRandomNode(vertices)
        pesoVertice = instancia.pesos[primeiroInserido]
        vertices[primeiroInserido] = True
        retorno.lista[nClusters].nodes.append(primeiroInserido)
        retorno.lista[nClusters].peso += pesoVertice 
        retorno.vertices[primeiroInserido]=nClusters
        nVerticesInseridos += 1

        if (nVerticesInseridos>=noCentral):
            break

        menorDistancia = 2000000000
        proximoVertice = -1
        for i in range(0,noCentral):
            if vertices[i]==False:
                distancia = instancia.custos[i,noCentral]+instancia.custos[i,primeiroInserido]
                if ((distancia<menorDistancia) and ((retorno.lista[nClusters].peso+instancia.pesos[i])<=restricao)):
                    proximoVertice = i
                    menorDistancia = distancia

        pesoVertice = instancia.pesos[proximoVertice]
        vertices[proximoVertice] = True
        retorno.lista[nClusters].nodes.append(proximoVertice)
        retorno.lista[nClusters].peso += pesoVertice 
        retorno.vertices[proximoVertice]=nClusters
        nVerticesInseridos += 1

        if (nVerticesInseridos>=noCentral):
            break

        while True:
            menorDistancia = 2000000000
            proximoVertice = -1
            for i in range(0,noCentral):
                if vertices[i]==False:
                    distancia = 0 
                    for j in retorno.lista[nClusters].nodes:
                       distancia += instancia.custos[i,j]
                    if ((distancia<menorDistancia) and ((retorno.lista[nClusters].peso+instancia.pesos[i])<=restricao)):
                        proximoVertice = i
                        menorDistancia = distancia
            if proximoVertice<0:
                break
            pesoVertice = instancia.pesos[proximoVertice]
            vertices[proximoVertice] = True
            retorno.lista[nClusters].nodes.append(proximoVertice)
            retorno.lista[nClusters].peso += pesoVertice 
            retorno.vertices[proximoVertice]=nClusters
            nVerticesInseridos += 1

        if (nVerticesInseridos>=noCentral):
            break
    #
    retorno.mstTotal = calculaTotalMST(retorno.lista,instancia)
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

def calculaTotalMST(clusters, instancia):
    mstTotal=0
    for i,c in clusters.items():
        if c.mstCusto<=0:
            c.mstCusto = prim(c.nodes,instancia)
        mstTotal+=c.mstCusto
    return mstTotal

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
    return -1

def geraPopulacaoInicial(instancia, Q, quantidade):
    solucoes = []
    s = geraSolucaoViavel(instancia, Q, False, False)
    solucoes.append(s)
    quantidade -= 1 
    contador=0
    for i in range(0,int(quantidade*0.4)):
        contador+=1
        if (contador==106):
            stop=1
        s = geraSolucaoViavel(instancia, Q, False, False, True)
        if (len(s.vertices)<instancia.tamanho-1):
            print("ERRO 2 - "+str(contador))
        else:
            solucoes.append(s)
    for i in range(0,int(quantidade*0.1)):
        s = geraSolucaoViavel(instancia, Q, False, True, False)
        if (len(s.vertices)<instancia.tamanho-1):
            print("ERRO 3")
        else:
            solucoes.append(s)
    for i in range(0,int(quantidade*0.2)):
        s = geraSolucaoViavel(instancia, Q, True, False, False)
        if (len(s.vertices)<instancia.tamanho-1):
            print("ERRO 4")
        else:
            solucoes.append(s)
    for i in range(0,int(quantidade*0.3)):
        s = geraSolucaoViavel2(instancia, Q)
        if (len(s.vertices)<instancia.tamanho-1):
            print("ERRO 1")
        else:
            solucoes.append(s)
    minValue = 1000000000
    minI = -1
    maxValue = -1
    maxI = -1
    for s in solucoes:
        if s.mstTotal<minValue:
            minValue=s.mstTotal
            minI = s
    solucoesFinal = []
    for s in solucoes:
        if (s.mstTotal<1.2*minValue):
            solucoesFinal.append(s)
    if debug:
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
    return solucoesFinal

def geraFilhos(solucao1,solucao2,instancia, restricao):
    nova1 = clustersObject()
    nova2 = clustersObject()
    nClustersNova1 = 0
    nClustersNova2 = 0
    for i,c in solucao1.lista.items():
        if (i%2==0):
            nClustersNova2+=1
            nova2.lista[nClustersNova2] = cluster()
            nova2.lista[nClustersNova2].nodes = c.nodes.copy()
            nova2.lista[nClustersNova2].mstCusto = c.mstCusto
            nova2.lista[nClustersNova2].peso = c.peso
        else:
            nClustersNova1+=1
            nova1.lista[nClustersNova1] = cluster()
            nova1.lista[nClustersNova1].nodes = c.nodes.copy()
            nova1.lista[nClustersNova1].mstCusto = c.mstCusto
            nova1.lista[nClustersNova1].peso = c.peso
    
    nClustersNova1Metade = nClustersNova1
    nClustersNova2Metade = nClustersNova2
    nClustersNova1 = 0
    nClustersNova2 = 0
    for i,c in solucao2.lista.items():
        #if (nClustersNova2>int(len(solucao2.lista)/2)):
        if (i%2==0):
            nClustersNova1+=1
            nova1.lista[nClustersNova1+nClustersNova1Metade] = cluster()
            nova1.lista[nClustersNova1+nClustersNova1Metade].nodes = c.nodes.copy()
            nova1.lista[nClustersNova1+nClustersNova1Metade].mstCusto = c.mstCusto
            nova1.lista[nClustersNova1+nClustersNova1Metade].peso = c.peso
        else:
            nClustersNova2+=1
            nova2.lista[nClustersNova2+nClustersNova2Metade] = cluster()
            nova2.lista[nClustersNova2+nClustersNova2Metade].nodes = c.nodes.copy()
            nova2.lista[nClustersNova2+nClustersNova2Metade].mstCusto = c.mstCusto
            nova2.lista[nClustersNova2+nClustersNova2Metade].peso = c.peso
    nova1 = removeInconsistencias(nova1, instancia, restricao)
    nova2 = removeInconsistencias(nova2, instancia, restricao)
    return nova1, nova2

def completaSolucao(instancia, restricao, solucao, vertices, randomOnlyFirst=True, randomAll=False, randomAllFirst=False):
    nClusters = len(solucao.lista)
    retorno = solucao
    nVerticesInseridos = len(solucao.vertices)

    linhas = instancia.pesos.shape[0]

    restricaoRestante = restricao
    minCusto = instancia.custoMaximo()+1
    noCentral = instancia.custos.shape[1]-1
    noMaisProximo = -1

    nClusters+=1
    clusters={}
    clusters[nClusters]=cluster()
    clusters[nClusters].peso = 0

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
                    if (menorCustoEncontrado > custoIparaUltimoInserido) and (custoIparaUltimoInserido >= 0):
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
    
    for i,c in clusters.items():
        for j in (c.nodes):
            retorno.vertices[j]=i

    for i,c in clusters.items():
        retorno.lista[i]=c
    retorno.mstTotal = calculaTotalMST(retorno.lista, instancia)
    retorno.randomAll = randomAll
    retorno.randomAllFirst = randomAllFirst
    retorno.randomOnlyFirst = randomOnlyFirst
    
    if debug:
        print(str(linhas)+" - "+str(len(retorno.vertices)))

    return retorno

def removeInconsistencias(s,instancia, restricao):
    s.vertices={}
    vertices={}
    for i in range(0,instancia.tamanho-1):
        vertices[i] = False
    removerClusters = []
    for i,c in s.lista.items():
        for v in c.nodes:
            if (i in s.vertices):
                removerClusters.append(i)
                break
            s.vertices[v]=i
    # caso haja repeticao de algum elemento em mais de um cluster, um deles é removido
    for remover in removerClusters:
        s.lista.pop(remover)
   
    sNova = clustersObject()
    nclusters = 0

    for i,c in s.lista.items():
        nclusters+=1
        sNova.lista[nclusters]=cluster()
        sNova.lista[nclusters].peso = c.peso
        sNova.lista[nclusters].mstCusto = c.mstCusto

        for v in c.nodes:
            sNova.lista[nclusters].nodes.append(v)
            sNova.vertices[v]=nclusters
            vertices[v]=True

    for i in range(0,instancia.tamanho-1):
        if (vertices[i]==False):
            pesoVertice = instancia.pesos[i]
            clusterMaisProximo = -1
            clusterMaisProximoDistancia=2000000000
            for j,c in sNova.lista.items():
                if c.peso+pesoVertice>restricao:
                    continue
                for k in c.nodes:
                    custoIK = instancia.custos[i,k]
                    if custoIK<clusterMaisProximoDistancia:
                        clusterMaisProximo=j
                        clusterMaisProximoDistancia=custoIK
            if (clusterMaisProximo>0):
                sNova.lista[clusterMaisProximo].nodes.append(i)
                sNova.lista[clusterMaisProximo].peso += pesoVertice
                sNova.lista[clusterMaisProximo].mstCusto = prim(sNova.lista[clusterMaisProximo].nodes,instancia)
                sNova.vertices[i]=clusterMaisProximo
                vertices[i]=True

    sNova = completaSolucao(instancia, restricao, sNova, vertices, False, False, False)
    return sNova

def crossover(solucao1, solucao2, instancia, restricao):
    i=0
    nova1,nova2 = geraFilhos(solucao1,solucao2,instancia, restricao)
    nova1,i,j=LS(nova1,instancia,restricao)
    nova2,i,j=LS(nova2,instancia,restricao)
    retorno={}
    retorno[nova1.mstTotal]=nova1
    retorno[nova2.mstTotal]=nova2
    retorno[solucao1.mstTotal]=solucao1
    retorno[solucao2.mstTotal]=solucao2

    retornoOrderedKeys = sorted(retorno)
    return retorno[retornoOrderedKeys[0]], retorno[retornoOrderedKeys[1]]


    ## gerar 2 solucoes filhas a partir das duas originais
    ## pegar metade dos clusters de cada e juntar
    ## havendo sobreposicao, eliminar os clusters e rodar o algoritmo de geracao de solucao inicial para clusterizar os nos livres
    ## recalcular o mstTotal e retornar as 2 solucoes novas


def LS(solucao, instancia, Q):
    iEscolhido = -1
    jEscolhido = -1
    novoClusterJ = -1
    novoClusterI = -1
    melhorMST = solucao.mstTotal
    linhas = instancia.pesos.shape[0]
    melhorClusters = {}

    for i in range(0,linhas-1):
        clusterI = solucao.vertices[i]
        for j in range(i+1,linhas):
            if (i==j):
                continue
            clusterJ = solucao.vertices[j]
            # nao troco se a restricao de peso por cluster nao for respeitada
            if ((solucao.lista[clusterI].peso-instancia.pesos[i]+instancia.pesos[j])>Q):
                continue
            if ((solucao.lista[clusterJ].peso-instancia.pesos[j]+instancia.pesos[i])>Q):
                continue

            clusters = {}
            for c,v in solucao.lista.items():
                clusters[c]=cluster() 
                clusters[c].mstCusto = 0
                clusters[c].peso = v.peso
                clusters[c].nodes = v.nodes.copy()

            clusters[clusterJ].nodes.remove(j)
            clusters[clusterI].nodes.remove(i)
            clusters[clusterJ].nodes.append(i)
            clusters[clusterI].nodes.append(j)  
            
            clusters[clusterJ].peso = (solucao.lista[clusterJ].peso-instancia.pesos[j]+instancia.pesos[i])
            clusters[clusterI].peso = (solucao.lista[clusterI].peso-instancia.pesos[i]+instancia.pesos[j])

            mst = calculaTotalMST(clusters,instancia)

            if mst<melhorMST:
                iEscolhido = i
                jEscolhido = j
                novoClusterJ = clusterI
                novoClusterI = clusterJ
                melhorClusters = clusters
                melhorMST = mst
    
    retorno = clustersObject()

    if melhorMST <= solucao.mstTotal:
        retorno.lista = melhorClusters
        retorno.mstTotal = melhorMST
        retorno.vertices = solucao.vertices.copy()
        retorno.vertices[iEscolhido] = novoClusterI
        retorno.vertices[jEscolhido] = novoClusterJ
        retorno.LS=True
    else:
        retorno = solucao, iEscolhido, jEscolhido
    if debug:
        print ("solucao original msttotal:" + str(solucao.mstTotal) + " - nova: " + str(melhorMST))
    return retorno, iEscolhido, jEscolhido

def LS2(solucao, instancia, Q):
    iEscolhido = -1
    jEscolhido = -1
    novoClusterJ = -1
    novoClusterI = -1
    melhorMST = solucao.mstTotal+1
    linhas = instancia.pesos.shape[0]
    melhorClusters = {}

    for i in range(0,linhas-1):
        clusterI = solucao.vertices[i]
        for j in range(i+1,linhas):
            if (i==j):
                continue
            clusterJ = solucao.vertices[j]
            # nao troco se a restricao de peso por cluster nao for respeitada
            if ((solucao.lista[clusterI].peso-instancia.pesos[i]+instancia.pesos[j])>Q):
                continue
            if ((solucao.lista[clusterJ].peso-instancia.pesos[j]+instancia.pesos[i])>Q):
                continue

            clusters = clustersObject()
            for c,v in solucao.lista.items():
                clusters.lista[c]=cluster() 
                clusters.lista[c].peso = v.peso
                clusters.lista[c].nodes = v.nodes.copy()
                clusters.lista[c].mstCusto = v.mstCusto

            clusters.lista[clusterJ].nodes.remove(j)
            clusters.lista[clusterI].nodes.remove(i)
            clusters.lista[clusterJ].nodes.append(i)
            clusters.lista[clusterI].nodes.append(j)  
            
            clusters.lista[clusterJ].mstCusto = prim(clusters.lista[clusterJ].nodes,instancia)
            clusters.lista[clusterI].mstCusto = prim(clusters.lista[clusterI].nodes,instancia)
            clusters.lista[clusterJ].peso = (solucao.lista[clusterJ].peso-instancia.pesos[j]+instancia.pesos[i])
            clusters.lista[clusterI].peso = (solucao.lista[clusterI].peso-instancia.pesos[i]+instancia.pesos[j])

            mst = calculaTotalMST(clusters.lista,instancia)
            clusters.mstTotal = solucao.mstTotal + clusters.lista[clusterJ].mstCusto + clusters.lista[clusterI].mstCusto - solucao.lista[clusterJ].mstCusto - solucao.lista[clusterI].mstCusto

            if (mst!= clusters.mstTotal):
                alerta=1

            if clusters.mstTotal<melhorMST:
                iEscolhido = i
                jEscolhido = j
                novoClusterJ = clusterI
                novoClusterI = clusterJ
                melhorClusters = clusters
    
    if melhorClusters.mstTotal < solucao.mstTotal:
        melhorClusters.vertices = solucao.vertices.copy()
        melhorClusters.vertices[iEscolhido] = novoClusterI
        melhorClusters.vertices[jEscolhido] = novoClusterJ
        melhorClusters.LS=True
        if debug:
            print ("solucao original msttotal:" + str(solucao.mstTotal) + " - nova: " + str( melhorClusters.mstTotal ))
        return melhorClusters, iEscolhido, jEscolhido
    else:
        return solucao, iEscolhido, jEscolhido
            
def executa(quantidadeSolucoesIniciais, quantidadeGeracoes, LStype=2):
    Q=[200,400,800]

    instancias = l.load("data\\capmst2.txt").instances
    s = geraSolucaoViavel2(instancias["50_1"], Q[0])

    s = geraSolucaoViavel(instancias["50_1"], Q[0], False, False, False)

    for instancia in instancias:
        for q in range(0,len(Q)):
            print ("tamanho instancia: "+str(instancias[instancia].tamanho)+" - id "+str(instancias[instancia].id)+" - "+str(Q[q]))
            #tempo = datetime.datetime.now()
            solucoes = geraPopulacaoInicial(instancias[instancia], Q[q], quantidadeSolucoesIniciais)
            #print(str(datetime.datetime.now()-tempo))
            print (len(solucoes))
            print("executando a LS tipo " + str(LStype))
            solucoesLS = []
            inicio = datetime.datetime.now()
            for i in range(0,quantidadeGeracoes):
                s1 = solucoes.pop(rd.randint(0,len(solucoes)-1))
                s2 = solucoes.pop(rd.randint(0,len(solucoes)-1))

                n1,n2 = crossover(s1,s2,instancias[instancia], Q[q])
                solucoes.append(n1)
                solucoes.append(n2)

                if i%20 == 0:
                    print("Geração "+str(i)+" - "+str(datetime.datetime.now()-inicio))
            print("FIM - "+str(datetime.datetime.now()-inicio))

            for s in solucoes:
                if LStype==1:
                    #inicio = datetime.datetime.now()
                    sLS,LSi,LSj = LS(s, instancias[instancia], Q[q])
                    solucoesLS.append(sLS)
                    #print(datetime.datetime.now() - inicio)
                else:
                    #inicio = datetime.datetime.now()
                    sLS2,LS2i,LS2j = LS2(s, instancias[instancia], Q[q])
                    solucoesLS.append(sLS)
                    #print(datetime.datetime.now() - inicio)
                #if (sLS2.mstTotal!=sLS.mstTotal):
                #    sLS2 = LS2(s, instancias[instancia], Q[q])
                    #print(datetime.datetime.now() - inicio)
            break
        break
    minValue = 1000000000
    minI = -1
    maxValue = -1
    maxI = -1
    for s in solucoesLS:
        if s.mstTotal<minValue:
            minValue=s.mstTotal
            minI = s
    print ("SOLUCOES LS tipo "+str(LStype)+" - menor valor mstTotal="+str(minValue) + " randomAll:" + str(minI.randomAll)+ " randomOnlyFirst:" + str(minI.randomOnlyFirst)+ " randomAllFirst:" + str(minI.randomAllFirst)+" LS:"+ str(minI.LS))
    minValue = 1000000000
    minI = -1
    maxValue = -1
    maxI = -1
    for s in solucoes:
        if s.mstTotal<minValue:
            minValue=s.mstTotal
            minI = s
    print ("SOLUCOES ORIGINAIS - menor valor mstTotal="+str(minValue) + " randomAll:" + str(minI.randomAll)+ " randomOnlyFirst:" + str(minI.randomOnlyFirst)+ " randomAllFirst:" + str(minI.randomAllFirst)+" LS:"+ str(minI.LS))


#inicio = datetime.datetime.now()
#executa(100,1000,2)
#print(datetime.datetime.now() - inicio)
     
#inicio = datetime.datetime.now()
#executa(100,1000,1)
#print(datetime.datetime.now() - inicio)
#inicio = datetime.datetime.now()
#executa(200,1000,1)
#print(datetime.datetime.now() - inicio)
#inicio = datetime.datetime.now()
#executa(300,1000,1)
#print(datetime.datetime.now() - inicio)
#inicio = datetime.datetime.now()
#executa(500,1000,1)
#print(datetime.datetime.now() - inicio)
inicio = datetime.datetime.now()
executa(1000,40,1)
print(datetime.datetime.now() - inicio)




