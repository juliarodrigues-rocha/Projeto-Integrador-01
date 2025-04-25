from datetime import datetime  # Importa a biblioteca datetime para manipulação de datas

# Estilizando 
print("=" * 70)
print("Sistema de Monitoramento de Sustentabilidade Pessoal".center(70))  # Centraliza o título
print("=" * 70)


# Função para validar e formatar a data de entrada
def validar_data():
    while True:
        data = input("Qual é a data? (DD/MM/AAAA) ")  # Pede a data no formato correto
        try:
            # Tenta converter a string para um objeto de data
            data_formatada = datetime.strptime(data, "%d/%m/%Y")
            return data_formatada.strftime("%d/%m/%Y")  # Retorna a data formatada corretamente
        except ValueError:
            print("Data inválida! Certifique-se de digitar um dia, mês e ano corretos.")  # Exibe erro caso a data digitada seja inválida



# Função para validar entradas numéricas, aceitando vírgula e ponto final como separador decimal (6,5 ou 6.5 são aceitos como resposta)
def obter_numero(mensagem):
    while True:
        entrada = input(mensagem).replace(",", ".")  # Substitui ',' por '.' para evitar erro de conversão
        try:
            valor = float(entrada)  # Converte a entrada digitada para float
            if valor < 0:
                print("O valor não pode ser negativo. Tente novamente.")  # Impede valores negativos
                continue
            return valor  # Retorna o número corretamente convertido
        except ValueError:
            print("Entrada inválida! Digite um número válido.")  # Mensagem de erro para entrada inválida

            

# Função para validar a escolha do meio de transporte
def obter_transporte():
    while True:
        try:
            opcao = int(input("Qual o meio de transporte você usou hoje?\n"
                              "1. Transporte público (ônibus, metrô, trem)\n"
                              "2. Bicicleta\n"
                              "3. Caminhada\n"
                              "4. Carro (combustível fóssil)\n"
                              "5. Carro elétrico\n"
                              "6. Carona compartilhada\n"
                              "Escolha uma das opções acima: "))
            if 1 <= opcao <= 6:  # Verifica se a opção está entre 1 e 6
                return opcao
            else:
                print("Opção inválida! Escolha um número entre 1 e 6.")  # Caso o usuário digite um número inválido
        except ValueError:
            print("Entrada inválida! Digite um número inteiro.")  # Mensagem de erro para entradas não numéricas

            


data = validar_data()

# Entradas / todas passam pela função `obter_numero()` que já faz as validações 
litros_agua = obter_numero("Quantos litros de água você consumiu hoje? (Aprox. em litros): ")  
energia_eletrica = obter_numero("Quantos kWh de energia elétrica você consumiu hoje? ")  
r_nao_reciclaveis = obter_numero("Quantos kg de resíduos não recicláveis você gerou hoje? ")  
residuos_reciclados = obter_numero("Qual a porcentagem de resíduos reciclados no total (em %)? ")  
meio_transporte = obter_transporte()  # Chama a função que valida o meio de transporte


print("=" * 70)

# Classificação do consumo de água
if litros_agua < 150:
    print("Consumo de água: Alta Sustentabilidade ")
elif 150 <= litros_agua <= 200:
    print("Consumo de água: Moderada Sustentabilidade ")
else:
    print("Consumo de água: Baixa Sustentabilidade ")

#  Classificação do consumo de energia elétrica
if energia_eletrica < 5:
    print("Consumo de energia: Alta Sustentabilidade ")
elif 5 <= energia_eletrica <= 10:
     print("Consumo de energia: Moderada Sustentabilidade ")
else:
     print("Consumo de energia: Baixa Sustentabilidade ")

#  Classificação da geração de resíduos recicláveis
if residuos_reciclados > 50:
    print("Geração de Resíduos Não Recicláveis: Alta Sustentabilidade")
elif 20 <= residuos_reciclados <= 50:
    print("Geração de Resíduos Não Recicláveis: Moderada Sustentabilidade")
else:
    print("Geração de Resíduos Não Recicláveis: Baixa Sustentabilidade")

#  Classificação do uso do transporte
if meio_transporte in [1, 2, 3, 5]:  # Transporte público, bicicleta, caminhada, carro elétrico
    print ("Uso de Transporte: Alta Sustentabilidade ")
elif meio_transporte == 6:  # Carona Compartilhada
    print ("Uso de Transporte: Moderada Sustentabilidade")
else:  # Carros movidos a combustíveis fósseis
    print("Uso de Transporte: Baixa Sustentabilidade")


print("Programa teste 01 encerrado")




















