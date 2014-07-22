import subprocess
import csv
import json

def create_csv(file_input, data_csv):
    output = open(data_csv, "w")
    output.write("VM,Cores,CPU_UTIL\n")
    for instance in file_input:
        output.write(instance["VM"] + "," + str(instance["Cores"]) + "," + str(instance["CPU_UTIL"])+"\n")
    output.close()

def comunica_com_r(scriptR, dado):
    processo = subprocess.Popen(scriptR+" "+dado, shell=True, stdout=subprocess.PIPE)
    while True:
        if (processo.poll() == 0):
            break
        elif (processo.poll() == 1):
            print "Requisicao nao concluida"
            break

    
def gera_retorno(dado):
    dic = {}
    input = open(dado)
    input.readline()
    for linha in input.readlines():
        termos = linha.split(",")
        dic[termos[0][6:-1]] = [termos[1], termos[2][:-1]]
    input.close()
    return dic


def data_to_dic(dadoJson, dadoCSV, scriptR, flavors):
    create_csv(dadoJson, dadoCSV)
    comunica_com_r(scriptR, dadoCSV)
    return gera_retorno(flavors)


def recomenda_flavor(dado):
    
    script="Rscript analytics/generate_recommendation.R"
    data_csv = "dados.csv"
    data_json = dado
    flavors = "flavors.csv"
    if(len(dado)>0):
        return data_to_dic(data_json, data_csv, script, flavors)
    else:
        return {}   




    

