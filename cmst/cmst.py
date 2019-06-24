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
    
    for i,c in clusters.items():
        for j in (c.nodes):
            retorno.vertices[j]=i

    retorno.lista=clusters
    retorno.mstTotal = calculaTotalMST(clusters,instancia)
    retorno.randomAll = randomAll
    retorno.randomAllFirst = randomAllFirst
    retorno.randomOnlyFirst = randomOnlyFirst
    
    if debug:
        print(str(linhas)+" - "+str(len(retorno.vertices)))

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

def geraPopulacaoInicial(instancia, Q, quantidade):
    solucoes = []
    s = geraSolucaoViavel(instancia, Q, False, False)
    solucoes.append(s)
    quantidade -= 1 
    for i in range(0,int(quantidade/2)):
        s = geraSolucaoViavel(instancia, Q, False, False, True)
        if (len(s.vertices)<instancia.tamanho-1):
            print("ERRO")
        else:
            solucoes.append(s)
        #s = geraSolucaoViavel(instancia, Q, False, True, False)
        #solucoes.append(s)
        s = geraSolucaoViavel(instancia, Q, True, False, False)
        if (len(s.vertices)<instancia.tamanho-1):
            print("ERRO")
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

def crossover(solucao1, solucao2, instancia):
    i=0
    ## gerar 2 solucoes filhas a partir das duas originais
    ## pegar metade dos clusters de cada e juntar
    ## havendo sobreposicao, eliminar os clusters e rodar o algoritmo de geracao de solucao inicial para clusterizar os nos livres
    ## recalcular o mstTotal e retornar as 2 solucoes novas

def mutation(solucao, instancia):
    i=0

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
        return solucao
    if debug:
        print ("solucao original msttotal:" + str(solucao.mstTotal) + " - nova: " + str(melhorMST))
    return retorno

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

            #mst = calculaTotalMST(clusters.lista,instancia)
            clusters.mstTotal = solucao.mstTotal + clusters.lista[clusterJ].mstCusto + clusters.lista[clusterI].mstCusto - solucao.lista[clusterJ].mstCusto - solucao.lista[clusterI].mstCusto

            if clusters.mstTotal<melhorMST:
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
        return melhorClusters
    else:
        return solucao
            
def executa(quantidadeSolucoesIniciais, quantidadeGeracoes):
    Q=[200,400,800]

    instancias = l.load("data\\capmst2.txt").instances

    s = geraSolucaoViavel(instancias["50_1"], Q[0], False, False, False)

    for instancia in instancias:
        for q in range(2,len(Q)):
            print ("tamanho instancia: "+str(instancias[instancia].tamanho)+" - id "+str(instancias[instancia].id)+" - "+str(Q[q]))
            tempo = datetime.datetime.now()
            solucoes = geraPopulacaoInicial(instancias[instancia], Q[q], quantidadeSolucoesIniciais)
            print(str(datetime.datetime.now()-tempo))
            print (len(solucoes))
            print("executando a LS")
            solucoesLS = []
            for s in solucoes:
                #inicio = datetime.datetime.now()
                #solucoesLS.append(LS(s, instancias[instancia], Q[q]))
                #print(datetime.datetime.now() - inicio)
                inicio = datetime.datetime.now()
                solucoesLS.append(LS2(s, instancias[instancia], Q[q]))
                print(datetime.datetime.now() - inicio)
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
    print ("SOLUCOES LS - menor valor mstTotal="+str(minValue) + " randomAll:" + str(minI.randomAll)+ " randomOnlyFirst:" + str(minI.randomOnlyFirst)+ " randomAllFirst:" + str(minI.randomAllFirst)+" LS:"+ str(minI.LS))
    minValue = 1000000000
    minI = -1
    maxValue = -1
    maxI = -1
    for s in solucoes:
        if s.mstTotal<minValue:
            minValue=s.mstTotal
            minI = s
    print ("SOLUCOES ORIGINAIS - menor valor mstTotal="+str(minValue) + " randomAll:" + str(minI.randomAll)+ " randomOnlyFirst:" + str(minI.randomOnlyFirst)+ " randomAllFirst:" + str(minI.randomAllFirst)+" LS:"+ str(minI.LS))
     
inicio = datetime.datetime.now()
executa(1000,1000)
print(datetime.datetime.now() - inicio)




