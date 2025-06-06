from datetime import datetime, date
import mysql.connector

print("=" * 70)
print("Sistema de Monitoramento de Sustentabilidade Pessoal".center(70))
print("=" * 70)

def conectar_banco():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Mb570619@@@",
        database="sustentabilidade2"
    )

def validar_data():
    while True:
        data = input("Qual é a data? (DD-MM-AAAA) ")
        try:
            data_convertida = datetime.strptime(data, "%d-%m-%Y")
            if data_convertida.date() > date.today():
                print("Data futura não permitida.")
                continue
            return data_convertida
        except ValueError:
            print("Data inválida! Formato correto: DD-MM-AAAA.")

def obter_numero(mensagem):
    while True:
        entrada = input(mensagem).replace(",", ".")
        try:
            valor = float(entrada)
            if valor < 0:
                print("Valor não pode ser negativo.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida! Digite um número válido.")

def obter_transporte():
    transportes = []
    while True:
        try:
            opcao = int(input(
                "Qual o meio de transporte você usou hoje?\n"
                "1. Transporte público (ônibus, metrô, trem)\n"
                "2. Bicicleta\n"
                "3. Caminhada\n"
                "4. Carro (combustível fóssil)\n"
                "5. Carro elétrico\n"
                "6. Carona compartilhada\n"
                "Escolha uma das opções acima: "))
            if 1 <= opcao <= 6:
                transportes.append(opcao)
            else:
                print("Opção inválida.")
        except ValueError:
            print("Entrada inválida. Digite um número de 1 a 6.")
            continue

        outro = input("Você utilizou outro meio de transporte hoje? (sim/não): ").strip().lower()
        if outro != "sim":
            break

    return transportes

def classificar_transporte(transportes):
    alta = {1, 2, 3, 5}
    moderada = {6}
    if all(t in alta for t in transportes):
        return "Alta Sustentabilidade"
    elif any(t in moderada for t in transportes):
        return "Moderada Sustentabilidade"
    else:
        return "Baixa Sustentabilidade"

def inserir_registro():
    data = validar_data()
    litros_agua = obter_numero("Quantos litros de água você consumiu hoje? ")
    energia = obter_numero("Quantos kWh de energia elétrica você consumiu hoje? ")
    residuos_nao = obter_numero("Quantos kg de resíduos não recicláveis você gerou hoje? ")
    reciclados = obter_numero("Qual a porcentagem de resíduos reciclados (em %)? ")
    transportes = obter_transporte()

    print("=" * 70)
    print(f"Consumo de água: {'Alta Sustentabilidade' if litros_agua < 150 else 'Moderada Sustentabilidade' if litros_agua <= 200 else 'Baixa Sustentabilidade'}")
    print(f"Consumo de energia: {'Alta Sustentabilidade' if energia < 5 else 'Moderada Sustentabilidade' if energia <= 10 else 'Baixa Sustentabilidade'}")
    print(f"Resíduos reciclados: {'Alta Sustentabilidade' if reciclados > 50 else 'Moderada Sustentabilidade' if reciclados >= 20 else 'Baixa Sustentabilidade'}")
    print(f"Transporte: {classificar_transporte(transportes)}")

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        comando = """
            INSERT INTO registros 
            (data_registro, litros_agua, energia_kwh, residuos_nao_reciclaveis, percentual_reciclado, meio_transporte)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (
            data.date(), litros_agua, energia,
            residuos_nao, reciclados, min(transportes)
        )
        cursor.execute(comando, valores)
        conexao.commit()
        print("Dados inseridos com sucesso.")

    except mysql.connector.Error as erro:
        print(f"Erro ao inserir no banco: {erro}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()

def listar_registros():
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("SELECT id, data_registro FROM registros ORDER BY data_registro DESC")
        resultados = cursor.fetchall()
        print("\nRegistros disponíveis:")
        for row in resultados:
            print(f"ID: {row[0]} | Data: {row[1].strftime('%d-%m-%Y')}")
        return resultados

    except mysql.connector.Error as erro:
        print(f"Erro: {erro}")
        return []

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()

def atualizar_registro():
    registros = listar_registros()
    if not registros:
        print("Nenhum registro disponível.")
        return

    try:
        id_reg = int(input("Digite o ID do registro para atualizar: "))
    except ValueError:
        print("ID inválido.")
        return

    nova_data = validar_data()
    nova_agua = obter_numero("Novo consumo de água (litros): ")
    nova_energia = obter_numero("Novo consumo de energia (kWh): ")
    novos_residuos = obter_numero("Nova quantidade de resíduos não recicláveis (kg): ")
    novo_percentual = obter_numero("Nova porcentagem de resíduos reciclados (%): ")
    novo_transporte = obter_transporte()

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        comando = """
            UPDATE registros
            SET data_registro=%s, litros_agua=%s, energia_kwh=%s, 
                residuos_nao_reciclaveis=%s, percentual_reciclado=%s, meio_transporte=%s
            WHERE id=%s
        """
        valores = (
            nova_data.date(), nova_agua, nova_energia,
            novos_residuos, novo_percentual, min(novo_transporte), id_reg
        )
        cursor.execute(comando, valores)
        conexao.commit()
        print("Registro atualizado com sucesso." if cursor.rowcount else "Registro não encontrado.")

    except mysql.connector.Error as erro:
        print(f"Erro ao atualizar: {erro}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()

def excluir_registro():
    registros = listar_registros()
    if not registros:
        return

    try:
        id_reg = int(input("ID do registro a excluir: "))
    except ValueError:
        print("ID inválido.")
        return

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM registros WHERE id = %s", (id_reg,))
        conexao.commit()
        print("Registro excluído." if cursor.rowcount else "ID não encontrado.")
    except mysql.connector.Error as erro:
        print(f"Erro ao excluir: {erro}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()

def calcular_medias_e_classificar():
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM registros")
        registros = cursor.fetchall()

        if not registros:
            print("Nenhum registro.")
            return

        total = len(registros)
        media_agua = sum(r['litros_agua'] for r in registros) / total
        media_energia = sum(r['energia_kwh'] for r in registros) / total
        media_reciclado = sum(r['percentual_reciclado'] for r in registros) / total
        media_transportes = sum(r['meio_transporte'] for r in registros) / total

        if round(media_transportes) in [1, 2, 3, 5]:
            classificacao_transporte = "Alta Sustentabilidade"
        elif round(media_transportes) == 6:
            classificacao_transporte = "Moderada Sustentabilidade"
        else:
            classificacao_transporte = "Baixa Sustentabilidade"

        print("\nMÉDIAS:")
        print(f"Água: {media_agua:.2f}L - {'Alta' if media_agua < 150 else 'Moderada' if media_agua <= 200 else 'Baixa'} Sustentabilidade")
        print(f"Eletricidade: {media_energia:.2f}kWh - {'Alta' if media_energia < 5 else 'Moderada' if media_energia <= 10 else 'Baixa'} Sustentabilidade")
        print(f"Reciclagem: {media_reciclado:.2f}% - {'Alta' if media_reciclado > 50 else 'Moderada' if media_reciclado >= 20 else 'Baixa'} Sustentabilidade")
        print(f"Transporte: {media_transportes:.2f} - {classificacao_transporte}")

    except mysql.connector.Error as erro:
        print(f"Erro: {erro}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()

def menu():
    while True:
        print("\nMENU")
        print("1. Inserir novo registro")
        print("2. Atualizar um registro")
        print("3. Listar registros")
        print("4. Ver médias e classificação")
        print("5. Excluir registro")
        print("6. Sair")

        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            inserir_registro()
        elif opcao == '2':
            atualizar_registro()
        elif opcao == '3':
            listar_registros()
        elif opcao == '4':
            calcular_medias_e_classificar()
        elif opcao == '5':
            excluir_registro()
        elif opcao == '6':
            print("Encerrando.")
            break
        else:
            print("Opção inválida.")

menu()