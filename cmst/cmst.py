import load as l
import random as rd
import datetime
from pathlib import Path
import sys

debug=False


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
    for i in range(0,instancia.tamanho):
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
    if len(g)==0:
        return 2000000000
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
    if quantidade==1:
        return [geraSolucaoViavel(instancia, Q, False, False, True)]
    q=quantidade*3
    solucoes = {}
    s = geraSolucaoViavel(instancia, Q, False, False)
    #solucoes.append(s)
    solucoes[s.mstTotal]=s
    q -= 1 
    for i in range(0,int(q*0.4)):
        s = geraSolucaoViavel(instancia, Q, False, False, True)
        if (len(s.vertices)<instancia.tamanho-1):
            print("ERRO 2 - "+str(contador))
        else:
            #solucoes.append(s)
            solucoes[s.mstTotal]=s
    for i in range(0,int(q*0.1)):
        s = geraSolucaoViavel(instancia, Q, False, True, False)
        if (len(s.vertices)<instancia.tamanho-1):
            print("ERRO 3")
        else:
            #solucoes.append(s)
            solucoes[s.mstTotal]=s

    for i in range(0,int(q*0.2)):
        s = geraSolucaoViavel(instancia, Q, True, False, False)
        if (len(s.vertices)<instancia.tamanho-1):
            print("ERRO 4")
        else:
            #solucoes.append(s)
            solucoes[s.mstTotal]=s

    for i in range(0,int(q*0.3)):
        s = geraSolucaoViavel2(instancia, Q)
        if (len(s.vertices)<instancia.tamanho-1):
            print("ERRO 1")
        else:
            solucoes[s.mstTotal]=s
            #solucoes.append(s)
    minValue = 1000000000
    minI = -1
    maxValue = -1
    maxI = -1
    for i,s in solucoes.items():
        if s.mstTotal<minValue:
            minValue=s.mstTotal
            minI = s
    solucoesFinal = []
    for i,s in solucoes.items():
        if (s.mstTotal<2*minValue):
            solucoesFinal.append(s)
            if len(solucoesFinal)>=quantidade:
                return solucoesFinal
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

def geraFilhos(solucao1,solucao2,instancia, restricao, estrategia=1):
    nova1 = clustersObject()
    nova2 = clustersObject()
    if estrategia==1:
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
    elif estrategia==2:
        corte1 = rd.randint(0,len(solucao1.lista))
        corte2 = rd.randint(0,len(solucao1.lista))
        if corte1>corte2:
            temp=corte2
            corte2=corte1
            corte1=temp
        nClustersNova1 = 0
        nClustersNova2 = 0
        for i,c in solucao1.lista.items():    
            if i>=corte1 and i<corte2:
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
        corte1 = rd.randint(0,len(solucao1.lista))
        corte2 = rd.randint(0,len(solucao1.lista))
        if corte1>corte2:
            temp=corte2
            corte2=corte1
            corte1=temp
        nClustersNova1Metade = nClustersNova1
        nClustersNova2Metade = nClustersNova2
        nClustersNova1 = 0
        nClustersNova2 = 0
        for i,c in solucao2.lista.items():    
            if i>corte1 and i<=corte2:
                nClustersNova1+=1
                nova1.lista[nClustersNova2] = cluster()
                nova1.lista[nClustersNova2].nodes = c.nodes.copy()
                nova1.lista[nClustersNova2].mstCusto = c.mstCusto
                nova1.lista[nClustersNova2].peso = c.peso

            else:
                nClustersNova2+=1
                nova2.lista[nClustersNova1] = cluster()
                nova2.lista[nClustersNova1].nodes = c.nodes.copy()
                nova2.lista[nClustersNova1].mstCusto = c.mstCusto
                nova2.lista[nClustersNova1].peso = c.peso
        for i,c in nova1.lista.items():
            if ((c.peso>0) and (rd.randint(0,5)==19)):
                    c.nodes.pop(rd.randint(0,len(c.nodes)-1))
                    c.peso = 0

        for i,c in nova2.lista.items():
            if ((c.peso>0) and (rd.randint(0,5)==19)):
                    c.nodes.pop(rd.randint(0,len(c.nodes)-1))
                    c.peso = 0
    elif estrategia==3:
        clusterSolucao1 = rd.randint(1,len(solucao1.lista))
        clusterSolucao2 = rd.randint(1,len(solucao2.lista))
        novoCluster1 = cluster()
        novoCluster2 = cluster()
        for k in range(0, len(solucao1.lista[clusterSolucao1].nodes)):
            if (rd.choice([0,1])==0):
                if (solucao1.lista[clusterSolucao1].nodes[k] not in novoCluster1.nodes):
                    novoCluster1.nodes.append(solucao1.lista[clusterSolucao1].nodes[k])
            if (rd.choice([0,1])==0):
                if (solucao1.lista[clusterSolucao1].nodes[k] not in novoCluster2.nodes):
                    novoCluster2.nodes.append(solucao1.lista[clusterSolucao1].nodes[k])
        for k in range(0, len(solucao2.lista[clusterSolucao2].nodes)):
            if (rd.choice([0,1])==0):
                if (solucao2.lista[clusterSolucao2].nodes[k] not in novoCluster2.nodes):
                    novoCluster2.nodes.append(solucao2.lista[clusterSolucao2].nodes[k])
            if (rd.choice([0,1])==0):
                if (solucao2.lista[clusterSolucao2].nodes[k] not in novoCluster1.nodes):
                    novoCluster1.nodes.append(solucao2.lista[clusterSolucao2].nodes[k])

        for i,c in solucao1.lista.items():    
            if i!=clusterSolucao1:
                nova1.lista[i] = cluster()
                nova1.lista[i].nodes = c.nodes.copy()
                nova1.lista[i].mstCusto = c.mstCusto
                nova1.lista[i].peso = c.peso
                for k in range(0,len(novoCluster1.nodes)):
                    if (novoCluster1.nodes[k] in nova1.lista[i].nodes):
                        nova1.lista[i].peso = 0
                        nova1.lista[i].nodes.remove(novoCluster1.nodes[k])
                if ((nova1.lista[i].peso>0) and (rd.randint(0,9)==5)):
                    nova1.lista[i].nodes.pop(rd.randint(0,len(nova1.lista[i].nodes)-1))
                    nova1.lista[i].peso = 0
            else:
                nova1.lista[i] = novoCluster1
                nova1.lista[i].peso=0
                nova1.lista[i].mstCusto=0
        for i,c in solucao2.lista.items():    
            if i!=clusterSolucao2:
                nova2.lista[i] = cluster()
                nova2.lista[i].nodes = c.nodes.copy()
                nova2.lista[i].mstCusto = c.mstCusto
                nova2.lista[i].peso = c.peso
                for k in range(0,len(novoCluster2.nodes)):
                    if (novoCluster2.nodes[k] in nova2.lista[i].nodes):
                        nova2.lista[i].peso = 0
                        nova2.lista[i].nodes.remove(novoCluster2.nodes[k])
                if ((nova2.lista[i].peso>0) and (rd.randint(0,9)==5)):
                    nova2.lista[i].nodes.pop(rd.randint(0,len(nova2.lista[i].nodes)-1))
                    nova2.lista[i].peso = 0

            else:
                nova2.lista[i] = novoCluster2
                nova2.lista[i].peso=0
                nova2.lista[i].mstCusto=0

    nova1 = removeInconsistencias(nova1, instancia, restricao)
    nova2 = removeInconsistencias(nova2, instancia, restricao)
    return nova1, nova2

def completaSolucao(instancia, restricao, solucao, vertices, randomOnlyFirst=True, randomAll=False, randomAllFirst=False):
    nClusters = len(solucao.lista)
    retorno = solucao
    nVerticesInseridos = len(solucao.vertices)
    #print(str(nVerticesInseridos)+" - ")

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

    clustersRecalcular = []
    # retiro itens do cluster caso a restricão nao tenha sido respeitada
    # precisa recalcular a mst ao final
    for i,c in s.lista.items():
        if c.peso==0:
            peso = sys.maxsize
            c.mstCusto=0
            clustersRecalcular.append(i)
            while peso>restricao:
                peso = 0
                quantidadeVertices = len(c.nodes)
                for j in range(0,quantidadeVertices):
                    peso += instancia.pesos[c.nodes[j]]
                if peso>restricao:
                    if quantidadeVertices>1:
                        c.nodes.pop(rd.randint(0,quantidadeVertices-1))
                    else:
                        c.nodes.pop(0)
            c.peso = peso
    #print("recalcular: "+str(clustersRecalcular))
    removerClusters = []
    for i,c in s.lista.items():
        for v in c.nodes:
            if (v in s.vertices):
                if (i not in removerClusters) and (s.vertices[v] not in removerClusters) and (i!=s.vertices[v]):
                    removerClusters.append(i)
                    #print("remover: "+str(i))
                    break
            s.vertices[v]=i
    #print ("remover: "+str(removerClusters))
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

    for j,c in sNova.lista.items():
        if c.peso>=restricao:
            continue

        for i in range(0,instancia.tamanho-1):
            if (vertices[i]==False):
                pesoVertice = instancia.pesos[i]
                clusterMaisProximo = -1
                clusterMaisProximoDistancia = sys.maxsize
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

def crossover(solucao1, solucao2, instancia, restricao, estrategia, tipoLS):
    i=0
    nova1,nova2 = geraFilhos(solucao1,solucao2,instancia, restricao, estrategia)
    if tipoLS==1:
        nova1,i,j=LS(nova1,instancia,restricao)
        nova2,i,j=LS(nova2,instancia,restricao)
    else:
        nova1,i,j=LS2(nova1,instancia,restricao)
        nova2,i,j=LS2(nova2,instancia,restricao)
    retorno={}
    retorno[nova1.mstTotal]=nova1
    retorno[nova2.mstTotal]=nova2
    retorno[solucao1.mstTotal]=solucao1
    retorno[solucao2.mstTotal]=solucao2

    retornoOrderedKeys = sorted(retorno)
    if len(retornoOrderedKeys)<2:
        return retorno[retornoOrderedKeys[0]],None, 1
    return retorno[retornoOrderedKeys[0]], retorno[retornoOrderedKeys[1]], 2


    ## gerar 2 solucoes filhas a partir das duas originais
    ## pegar metade dos clusters de cada e juntar
    ## havendo sobreposicao, eliminar os clusters e rodar o algoritmo de geracao de solucao inicial para clusterizar os nos livres
    ## recalcular o mstTotal e retornar as 2 solucoes novas


def LS(solucao, instancia, Q):
    iEscolhido = -1
    jEscolhido = -1
    novoClusterJ = -1
    novoClusterI = -1
    linhas = instancia.pesos.shape[0]
    melhorClusters = solucao
    swapsTestados = {}

    custosOrdenados = instancia.getCustosOrdenados()
    quantidadeItens = int(instancia.tamanho*0.3)

    for i in range(0,linhas-1):
        clusterI = solucao.vertices[i]
        contador=0
        if i not in swapsTestados:
            swapsTestados[i] = []
            maisProximo = -1
            for k in range(0,len(custosOrdenados[i])-1):
                if (clusterI == solucao.vertices[k]):
                    maisProximo = k
        for kv in custosOrdenados[maisProximo]:
            j = kv.key
            if (contador >= quantidadeItens):
                break
            #o proprio ou no central
            if (i==j) or (j==instancia.tamanho-1):
                continue
            clusterJ = solucao.vertices[j]
            if (clusterJ == clusterI):
                continue
            # nao troco se a restricao de peso por cluster nao for respeitada
            if ((solucao.lista[clusterI].peso-instancia.pesos[i]+instancia.pesos[j])>Q) or ((solucao.lista[clusterJ].peso-instancia.pesos[j]+instancia.pesos[i])>Q):
                continue
            if j not in swapsTestados:
                swapsTestados[j] = []
            elif j in swapsTestados[i]:
                continue
            swapsTestados[i].append(j)
            swapsTestados[j].append(i)

            clusters = clustersObject()
            for c,v in solucao.lista.items():
                clusters.lista[c]=cluster() 
                clusters.lista[c].mstCusto = solucao.lista[c].mstCusto
                clusters.lista[c].peso = v.peso
                clusters.lista[c].nodes = v.nodes.copy()

            clusters.lista[clusterJ].nodes.remove(j)
            clusters.lista[clusterI].nodes.remove(i)

            clusters.lista[clusterJ].nodes.append(i)
            clusters.lista[clusterI].nodes.append(j)  
            
            clusters.lista[clusterJ].peso = (solucao.lista[clusterJ].peso-instancia.pesos[j]+instancia.pesos[i])
            clusters.lista[clusterI].peso = (solucao.lista[clusterI].peso-instancia.pesos[i]+instancia.pesos[j])

            clusters.lista[clusterJ].mstCusto = prim(clusters.lista[clusterJ].nodes, instancia)
            clusters.lista[clusterI].mstCusto = prim(clusters.lista[clusterI].nodes, instancia)

            #clusters.mstTotal = solucao.mstTotal + clusters.lista[clusterJ].mstCusto + clusters.lista[clusterI].mstCusto - solucao.lista[clusterJ].mstCusto - solucao.lista[clusterI].mstCusto
            clusters.mstTotal = 0
            for k,c in clusters.lista.items():
                clusters.mstTotal += c.mstCusto

            contador+=1
            if clusters.mstTotal < melhorClusters.mstTotal:
                iEscolhido = i
                jEscolhido = j
                novoClusterJ = clusterI
                novoClusterI = clusterJ
                melhorClusters = clusters
    
    if melhorClusters.mstTotal <= solucao.mstTotal:
        melhorClusters.vertices = solucao.vertices.copy()
        melhorClusters.vertices[iEscolhido] = novoClusterI
        melhorClusters.vertices[jEscolhido] = novoClusterJ
        melhorClusters.LS=True
        if debug:
            print ("solucao original msttotal:" + str(solucao.mstTotal) + " - nova: " + str( melhorClusters.mstTotal ))
        return melhorClusters, iEscolhido, jEscolhido
    else:
        return solucao, iEscolhido, jEscolhido

def LS2(solucao, instancia, Q):
    iEscolhido = -1
    jEscolhido = -1
    novoClusterJ = -1
    novoClusterI = -1
    linhas = instancia.tamanho-1
    melhorClusters = solucao

    for i in range(0,linhas-1):
        clusterI = solucao.vertices[i]
        for j in range(i+1,linhas):
            if (i==j):
                continue
            clusterJ = solucao.vertices[j]
            if (clusterJ==clusterI):
                continue
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

            #mst = calculaTotalMST(clusters.lista,instancia)
            clusters.mstTotal = 0
            for k,c in clusters.lista.items():
                clusters.mstTotal += c.mstCusto
            #clusters.mstTotal = solucao.mstTotal + clusters.lista[clusterJ].mstCusto + clusters.lista[clusterI].mstCusto - solucao.lista[clusterJ].mstCusto - solucao.lista[clusterI].mstCusto

            #if (mst!= clusters.mstTotal):
                #alerta=1

            if clusters.mstTotal<melhorClusters.mstTotal:
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

def executa(quantidadeSolucoesIniciais, quantidadeGeracoes, LStype=2, estrategia_crossover=2, seeds=[1,2,3,4,5], tempolimite = 1200, quantidadeRenovacao=2):
    Q=[200,400,800]
    Q=[5,10,20]

    instancias = l.load("tcte","data\\capmst1.txt").instances
    datahora_arquivos = datetime.datetime.now()
    datahora_arquivos = str(datahora_arquivos.year)+str(datahora_arquivos.month)+str(datahora_arquivos.day)+str(datahora_arquivos.hour)+str(datahora_arquivos.minute)+str(datahora_arquivos.second)

    results_path = "results\\"+str(datahora_arquivos)+".csv"
    path_instance = Path(results_path)
    if path_instance.is_file()==False:
        with open(results_path, "a") as results_file:
            results_write=["instancia;tamanho;id;restricao;melhor incial;melhor GA;seed;crossover;LS;tempo;renovacao;populacao\n"]
            results_file.writelines(results_write)
    
    for seed in seeds:
        rd.seed(seed)
        for instancia in instancias:
            #if instancia != "tc80_2":
            #    continue
            if instancia.find("80")<0:
                continue
            inst = instancias[instancia]
            for q in range(0,len(Q)):      
                print (instancia+" tamanho instancia: "+str(inst.tamanho)+" - id "+str(instancias[instancia].id)+" - restricao "+str(Q[q])+" - tempo "+str(tempolimite)+" - LS "+str(LStype)+" - crossover "+str(estrategia_crossover))

                inicio = datetime.datetime.now()
                solucoes = geraPopulacaoInicial(inst, Q[q], quantidadeSolucoesIniciais)
                melhorSolucao = solucoes[0]
                for s in solucoes:
                    if s.mstTotal<melhorSolucao.mstTotal:
                        melhorSolucao.mstTotal = s.mstTotal
                
                melhorInicial = str(melhorSolucao.mstTotal)
                print("Melhor inicial: "+ str(melhorInicial))
                solucoesLS = []
                inicio=datetime.datetime.now()
                for s in solucoes:
                    if LStype==2:
                        ns,i,j = LS2(s,inst,Q[q])
                    else:
                        ns,i,j = LS(s,inst,Q[q])
                    solucoesLS.append(ns)
                print("LS inicial: "+str(datetime.datetime.now()-inicio))

                solucoes = solucoesLS

                for s in solucoes:
                    if s.mstTotal<melhorSolucao.mstTotal:
                        melhorSolucao.mstTotal = s.mstTotal
                print("Melhor apos LS inicial: "+ str(melhorSolucao.mstTotal))
                
                for i in range(0,quantidadeGeracoes):
                    novaGeracao=[]
                    for j in range(0,len(solucoes)-1,2):
                        s1 = solucoes[j]
                        s2 = solucoes[j+1]
                        n1,n2, qtd = crossover(s1,s2,inst, Q[q], estrategia_crossover, LStype)
                        if qtd==1:
                            n2 = geraPopulacaoInicial(inst, Q[q], 1)[0]
                        novaGeracao.append(n1)
                        novaGeracao.append(n2)

                        if melhorSolucao.mstTotal>n1.mstTotal:
                            melhorSolucao=n1
                            print("Geração "+str(i)+" melhor até geracao: "+ str(melhorSolucao.mstTotal) +" - "+str(datetime.datetime.now()-inicio)+" em "+str(len(solucoes))+" solucoes")
                        if melhorSolucao.mstTotal>n2.mstTotal:
                            melhorSolucao=n2
                            print("Geração "+str(i)+" melhor até geracao: "+ str(melhorSolucao.mstTotal) +" - "+str(datetime.datetime.now()-inicio)+" em "+str(len(solucoes))+" solucoes")
                        if (datetime.datetime.now()-inicio).seconds>tempolimite:
                            break
                    
                    if (datetime.datetime.now()-inicio).seconds>tempolimite:
                        break
                    novaGeracao.sort(key=lambda x: x.mstTotal, reverse=True)

                    for k in range(0,quantidadeRenovacao):
                        #novaGeracao.pop(int((k*quantidadeSolucoesIniciais-1)/quantidadeRenovacao))
                        novaGeracao.pop(0)
                    
                    
                    solucoes = []
                    if (quantidadeRenovacao>0):
                        solucoes.append(geraPopulacaoInicial(inst, Q[q], 1)[0])
                                            
                    lenNovaGeracao=len(novaGeracao)
                    while (lenNovaGeracao>0):
                        if lenNovaGeracao>0:
                            solucoes.append(novaGeracao.pop(rd.randint(0,len(novaGeracao)-1)))
                        else:
                            solucoes.append(novaGeracao.pop(0))
                        if (lenNovaGeracao%(quantidadeSolucoesIniciais)/quantidadeRenovacao)==0:
                            solucoes.append(geraPopulacaoInicial(inst, Q[q], 1)[0])
                        lenNovaGeracao-=1

                    while(len(solucoes)<quantidadeSolucoesIniciais):
                        solucoes.append(geraPopulacaoInicial(inst, Q[q], 1)[0])

                    #if i%5 == 0:
                    #    print("Geração "+str(i)+" melhor até geracao: "+ str(melhorSolucao.mstTotal) +" - "+str(datetime.datetime.now()-inicio))
                print("Geração "+str(i)+" melhor até geracao: "+ str(melhorSolucao.mstTotal) +" - "+str(datetime.datetime.now()-inicio)+" em "+str(len(solucoes))+" solucoes")
                #print(str(melhorSolucao.vertices))
                if LStype==2:
                    melhorSolucao,i,j = LS2(melhorSolucao,inst,Q[q])
                else:
                    melhorSolucao,i,j = LS(melhorSolucao,inst,Q[q])

                solucoes.append(melhorSolucao)
                print("FIM - "+str(datetime.datetime.now()-inicio))
                #print(str(melhorSolucao.vertices))
                with open(results_path, "a") as results_file:
                    results_write=[instancia+";"+str(inst.tamanho)+";"+str(instancias[instancia].id)+";"+str(Q[q])+";"+melhorInicial+";"+str(melhorSolucao.mstTotal)+";"+str(seed)+";"+str(estrategia_crossover)+";"+str(LStype)+";"+str((datetime.datetime.now()-inicio).seconds)+";"+str(quantidadeRenovacao)+";"+str(quantidadeSolucoesIniciais)+"\n"]
                    results_file.writelines(results_write)

inicio = datetime.datetime.now()
population = 40
generations = 400
LStype = 1
estrategiacrossover = 3
quantidadeRenovacao = int(population*0.1)
tempolimite = 1200
executa(population,generations,LStype,estrategiacrossover,[1,2,3,4,5],tempolimite,quantidadeRenovacao)
print(datetime.datetime.now() - inicio)