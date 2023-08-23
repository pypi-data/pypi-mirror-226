def imc(peso, altura):
    return peso/(altura * altura)


def litrosAgua(peso):
    return peso * 35


def qtdCalorias(peso, altura, idade, sexo):

    if sexo == 'm':
        return (66 + (6.2 * peso) + (12.7 * altura)) - (6.76 * idade)

    if sexo == 'f':
        return (655.1 + (4.35 * peso) + (4.7* altura)) - (4.7 * idade)


def qtdProteina(qtdCalorias):
    return (qtdCalorias * 0.4)/4


def qtdCarboidratos(qtdCalorias):
    return (qtdCalorias * 0.4)/4


def qtdGorduras(qtdCalorias):
    return (qtdCalorias * 0.2)/9


def imm(peso, altura, massa_muscular):
    return massa_muscular / (altura ** 2)


def percentualGordura(imc, idade, sexo):
    if sexo == 'm':
        return 1.20 * imc + 0.23 * idade - 10.8 - 5.4
    else:
        return 1.20 * imc + 0.23 * idade - 5.4


def gastoEnergeticoBasal(peso, altura, idade, sexo):
    if sexo == 'm':
        return 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * idade)
    else:
        return 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * idade)


def gastoEnergeticoTotal(geb, nivel_atividade):
    return geb * nivel_atividade


def taxaMetabólicaBasal(peso, altura, idade, sexo):
    if sexo == 'm':
        return 10 * peso + 6.25 * altura - 5 * idade + 5
    else:
        return 10 * peso + 6.25 * altura - 5 * idade - 161


def frequenciaCardiacaMaxima(idade, sexo):
    if sexo == 'm':
        return 220 - idade
    else:
        return 226 - idade


def taxaPerdaPeso(calorias_consumidas, calorias_gastas):
    return (calorias_consumidas - calorias_gastas) / 7700  
   