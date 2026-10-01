import time
import random

# ============================================================
# CONFIGURAÇÕES
# ============================================================

MAX = 100000

cadastros = {}
fila = []
atendidos = []
contador_eventos = 0


# ============================================================
# R1 - CADASTRAR
# ============================================================

def cadastrar(cpf, nome, nascimento):
    if cpf in cadastros:
        print("CPF já cadastrado!")
        return False

    cadastros[cpf] = {
        "cpf": cpf,
        "nome": nome,
        "nascimento": nascimento
    }

    print("Cadastro realizado com sucesso!")
    return True


# ============================================================
# R2 - BUSCAR CADASTRO
# Retorna o cadastro ou None se não existir
# Complexidade média: O(1)
# ============================================================

def buscar_cadastro(cpf):
    if cpf in cadastros:
        return cadastros[cpf]

    return None


# ============================================================
# R3 - DAR ENTRADA
# ============================================================

def dar_entrada(cpf, risco):
    global contador_eventos

    if cpf not in cadastros:
        print("CPF não possui cadastro.")
        return False

    # Verifica se já está na fila
    for paciente in fila:
        if paciente["cpf"] == cpf:
            print("Paciente já está na fila.")
            return False

    contador_eventos += 1

    paciente = {
        "cpf": cpf,
        "nome": cadastros[cpf]["nome"],
        "nascimento": cadastros[cpf]["nascimento"],
        "risco": risco,
        "entrada": contador_eventos
    }

    fila.append(paciente)

    print("Paciente entrou na fila.")
    return True


# ============================================================
# R4 - CHAMAR PRÓXIMO
#
# Regra:
# 1. Menor número de risco = maior prioridade
# 2. Em caso de empate, quem chegou primeiro é chamado
#
# Complexidade: O(n)
# ============================================================

def chamar_proximo():
    global contador_eventos

    # Tratamento da fila vazia
    if not fila:
        return None

    melhor = 0

    # Procura o paciente de maior prioridade
    for i in range(1, len(fila)):

        # Menor risco = maior prioridade
        if fila[i]["risco"] < fila[melhor]["risco"]:
            melhor = i

        # Mesmo risco: quem chegou primeiro
        elif fila[i]["risco"] == fila[melhor]["risco"]:

            if fila[i]["entrada"] < fila[melhor]["entrada"]:
                melhor = i

    # Remove o paciente correto da fila
    paciente = fila.pop(melhor)

    # Registra o evento da chamada
    contador_eventos += 1

    paciente["chamada"] = contador_eventos

    paciente["tempo_espera"] = (
        paciente["chamada"] - paciente["entrada"]
    )

    atendidos.append(paciente)

    # R4 precisa retornar o paciente
    return paciente


# ============================================================
# R5 - DESISTIR
# ============================================================

def desistir(cpf):

    for i in range(len(fila)):

        if fila[i]["cpf"] == cpf:

            fila.pop(i)

            print("Paciente removido da fila.")
            return True

    print("Paciente não está na fila.")
    return False


# ============================================================
# R6 - TAMANHO DA FILA
# ============================================================

def tamanho_fila():
    print(
        "Quantidade de pacientes aguardando:",
        len(fila)
    )


# ============================================================
# INSERTION SORT
#
# Ordenação decrescente pelo tempo de espera.
#
# Complexidade:
# Melhor caso: O(n)
# Pior caso: O(n²)
# ============================================================

def insertion_sort(lista):

    comparacoes = 0
    movimentos = 0

    for i in range(1, len(lista)):

        atual = lista[i]

        j = i - 1

        while j >= 0:

            comparacoes += 1

            # Maior tempo de espera primeiro
            if lista[j]["tempo_espera"] < atual["tempo_espera"]:

                lista[j + 1] = lista[j]

                movimentos += 1

                j -= 1

            else:
                break

        lista[j + 1] = atual

        movimentos += 1

    return lista, comparacoes, movimentos


# ============================================================
# MERGE SORT
#
# Complexidade: O(n log n)
# ============================================================

def merge_sort(lista):

    if len(lista) <= 1:
        return lista

    meio = len(lista) // 2

    esquerda = merge_sort(lista[:meio])

    direita = merge_sort(lista[meio:])

    return merge(esquerda, direita)


# ============================================================
# MERGE
# ============================================================

def merge(esquerda, direita):

    resultado = []

    i = 0
    j = 0

    while i < len(esquerda) and j < len(direita):

        # Maior tempo de espera primeiro
        if esquerda[i]["tempo_espera"] >= direita[j]["tempo_espera"]:

            resultado.append(esquerda[i])

            i += 1

        else:

            resultado.append(direita[j])

            j += 1

    while i < len(esquerda):

        resultado.append(esquerda[i])

        i += 1

    while j < len(direita):

        resultado.append(direita[j])

        j += 1

    return resultado


# ============================================================
# GERA CPF ALEATÓRIO
# ============================================================

def gerar_cpf():

    return ''.join(
        str(random.randint(0, 9))
        for _ in range(11)
    )


# ============================================================
# GERA N CPFs ÚNICOS
# ============================================================

def gerar_cpfs_unicos(n):

    cpfs = set()

    while len(cpfs) < n:

        cpfs.add(gerar_cpf())

    return list(cpfs)


# ============================================================
# CRIAR CADASTROS PARA O BENCHMARK
# ============================================================

def criar_cadastros_benchmark(n):

    cadastros.clear()

    cpfs = gerar_cpfs_unicos(n)

    for i, cpf in enumerate(cpfs):

        cadastros[cpf] = {
            "cpf": cpf,
            "nome": f"Paciente {i}",
            "nascimento": "01/01/2000"
        }

    return cpfs


# ============================================================
# PREPARAR FILA PARA BENCHMARK
# ============================================================

def preparar_fila_benchmark(cpfs):

    global contador_eventos

    fila.clear()

    atendidos.clear()

    contador_eventos = 0

    for cpf in cpfs:

        contador_eventos += 1

        fila.append({
            "cpf": cpf,
            "nome": cadastros[cpf]["nome"],
            "nascimento": cadastros[cpf]["nascimento"],

            # Riscos aleatórios
            "risco": random.randint(1, 5),

            "entrada": contador_eventos
        })


# ============================================================
# BENCHMARK R2
#
# Executa várias buscas para obter uma medição mais estável.
# ============================================================

def benchmark_r2(n):

    cpfs = criar_cadastros_benchmark(n)

    cpf_teste = cpfs[-1]

    repeticoes = 10000

    inicio = time.perf_counter()

    for _ in range(repeticoes):

        resultado = buscar_cadastro(cpf_teste)

    fim = time.perf_counter()

    tempo_total = fim - inicio

    tempo_medio = tempo_total / repeticoes

    return tempo_total, tempo_medio, resultado


# ============================================================
# BENCHMARK R4
#
# Mede a operação completa:
# procura o paciente + remove da fila.
# ============================================================

def benchmark_r4(n):

    cpfs = criar_cadastros_benchmark(n)

    preparar_fila_benchmark(cpfs)

    # Faz uma cópia para não destruir a fila original
    fila_teste = fila.copy()

    inicio = time.perf_counter()

    melhor = 0

    for i in range(1, len(fila_teste)):

        if fila_teste[i]["risco"] < fila_teste[melhor]["risco"]:

            melhor = i

        elif fila_teste[i]["risco"] == fila_teste[melhor]["risco"]:

            if fila_teste[i]["entrada"] < fila_teste[melhor]["entrada"]:

                melhor = i

    paciente = fila_teste.pop(melhor)

    fim = time.perf_counter()

    tempo = fim - inicio

    return tempo, paciente


# ============================================================
# GERAR REGISTROS DE ATENDIMENTO PARA R7
# ============================================================

def gerar_atendimentos(m):

    registros = []

    for i in range(m):

        registros.append({

            "cpf": f"{i:011d}",

            "nome": f"Paciente {i}",

            "risco": random.randint(1, 5),

            # Valores aleatórios para produzir uma entrada
            # suficientemente desordenada
            "entrada": i,

            "chamada": i + random.randint(1, 1000),

            "tempo_espera": random.randint(1, 1000000)
        })

    return registros


# ============================================================
# BENCHMARK INSERTION SORT
# ============================================================

def benchmark_insertion(m):

    dados = gerar_atendimentos(m)

    inicio = time.perf_counter()

    lista_ordenada, comparacoes, movimentos = insertion_sort(
        dados
    )

    fim = time.perf_counter()

    tempo = fim - inicio

    return tempo, comparacoes, movimentos


# ============================================================
# BENCHMARK MERGE SORT
# ============================================================

def benchmark_merge(m):

    dados = gerar_atendimentos(m)

    inicio = time.perf_counter()

    lista_ordenada = merge_sort(dados)

    fim = time.perf_counter()

    tempo = fim - inicio

    return tempo


# ============================================================
# BENCHMARK R7
#
# Os dois algoritmos recebem conjuntos equivalentes.
# ============================================================

def benchmark_r7(m):

    dados = gerar_atendimentos(m)

    dados_insertion = dados.copy()

    dados_merge = dados.copy()

    # -----------------------------
    # INSERTION SORT
    # -----------------------------

    inicio = time.perf_counter()

    lista_insertion, comparacoes, movimentos = insertion_sort(
        dados_insertion
    )

    fim = time.perf_counter()

    tempo_insertion = fim - inicio

    # -----------------------------
    # MERGE SORT
    # -----------------------------

    inicio = time.perf_counter()

    lista_merge = merge_sort(dados_merge)

    fim = time.perf_counter()

    tempo_merge = fim - inicio

    return (
        tempo_insertion,
        comparacoes,
        movimentos,
        tempo_merge
    )


# ============================================================
# EXECUTAR EXPERIMENTO 2.1
#
# R2 e R4:
# N = 10.000
# N = 100.000
# ============================================================

def executar_experimento_21():

    print("\n")
    print("=" * 70)
    print("EXPERIMENTO 2.1 - R2 E R4")
    print("=" * 70)

    resultados = []

    for n in [10000, 100000]:

        print("\nExecutando N =", n)

        # -----------------------------
        # R2
        # -----------------------------

        tempo_r2_total, tempo_r2_medio, resultado = benchmark_r2(n)

        print("\nR2 - Buscar cadastro")

        print("N:", n)

        print(
            "Tempo total:",
            f"{tempo_r2_total:.10f}",
            "segundos"
        )

        print(
            "Tempo médio:",
            f"{tempo_r2_medio:.12f}",
            "segundos"
        )

        # -----------------------------
        # R4
        # -----------------------------

        tempo_r4, paciente = benchmark_r4(n)

        print("\nR4 - Chamar próximo")

        print("N:", n)

        print(
            "Tempo:",
            f"{tempo_r4:.10f}",
            "segundos"
        )

        resultados.append({
            "n": n,
            "r2": tempo_r2_total,
            "r2_medio": tempo_r2_medio,
            "r4": tempo_r4
        })

    # -----------------------------
    # TABELA
    # -----------------------------

    print("\n")
    print("=" * 70)
    print("TABELA - EXPERIMENTO 2.1")
    print("=" * 70)

    print(
        f"{'Operação':<15}"
        f"{'N':<15}"
        f"{'Tempo (s)':<20}"
    )

    print("-" * 50)

    for resultado in resultados:

        print(
            f"{'R2':<15}"
            f"{resultado['n']:<15}"
            f"{resultado['r2']:<20.10f}"
        )

        print(
            f"{'R4':<15}"
            f"{resultado['n']:<15}"
            f"{resultado['r4']:<20.10f}"
        )

    return resultados


# ============================================================
# EXECUTAR EXPERIMENTO 2.2
#
# M = 10.000
# M = 100.000
# ============================================================

def executar_experimento_22():

    print("\n")
    print("=" * 70)
    print("EXPERIMENTO 2.2 - ORDENAÇÃO DO R7")
    print("=" * 70)

    resultados = []

    for m in [10000, 100000]:

        print("\nExecutando M =", m)

        (
            tempo_insertion,
            comparacoes,
            movimentos,
            tempo_merge
        ) = benchmark_r7(m)

        print("\nInsertion Sort")

        print(
            "Tempo:",
            f"{tempo_insertion:.10f}",
            "segundos"
        )

        print(
            "Comparações:",
            comparacoes
        )

        print(
            "Movimentos:",
            movimentos
        )

        print("\nMerge Sort")

        print(
            "Tempo:",
            f"{tempo_merge:.10f}",
            "segundos"
        )

        resultados.append({
            "m": m,
            "insertion": tempo_insertion,
            "merge": tempo_merge
        })

    # -----------------------------
    # TABELA
    # -----------------------------

    print("\n")
    print("=" * 70)
    print("TABELA - EXPERIMENTO 2.2")
    print("=" * 70)

    print(
        f"{'Algoritmo':<20}"
        f"{'M':<15}"
        f"{'Tempo (s)':<20}"
    )

    print("-" * 55)

    for resultado in resultados:

        print(
            f"{'Insertion Sort':<20}"
            f"{resultado['m']:<15}"
            f"{resultado['insertion']:<20.10f}"
        )

        print(
            f"{'Merge Sort':<20}"
            f"{resultado['m']:<15}"
            f"{resultado['merge']:<20.10f}"
        )

    # -----------------------------
    # RAZÕES
    # -----------------------------

    if len(resultados) == 2:

        insertion_razao = (
            resultados[1]["insertion"] /
            resultados[0]["insertion"]
        )

        merge_razao = (
            resultados[1]["merge"] /
            resultados[0]["merge"]
        )

        print("\n")
        print("=" * 70)
        print("COMPARAÇÃO M = 10.000 -> M = 100.000")
        print("=" * 70)

        print(
            "Insertion Sort:",
            f"{insertion_razao:.2f} vezes mais lento"
        )

        print(
            "Merge Sort:",
            f"{merge_razao:.2f} vezes mais lento"
        )

    return resultados


# ============================================================
# R7 - RELATÓRIO
#
# Executa os dois algoritmos.
# ============================================================

def relatorio():

    if len(atendidos) == 0:

        print("Nenhum paciente foi atendido.")

        return

    print("\n")
    print("=" * 50)
    print("RELATÓRIO R7")
    print("=" * 50)

    # --------------------------------
    # INVERSION SORT
    # --------------------------------

    lista_insertion = atendidos.copy()

    inicio = time.perf_counter()

    lista_insertion, comparacoes, movimentos = insertion_sort(
        lista_insertion
    )

    fim = time.perf_counter()

    tempo_insertion = fim - inicio

    # --------------------------------
    # MERGE SORT
    # --------------------------------

    lista_merge = atendidos.copy()

    inicio = time.perf_counter()

    lista_merge = merge_sort(lista_merge)

    fim = time.perf_counter()

    tempo_merge = fim - inicio

    # --------------------------------
    # RESULTADOS
    # --------------------------------

    print("\nInsertion Sort")

    print(
        "Tempo:",
        f"{tempo_insertion:.10f}",
        "segundos"
    )

    print(
        "Comparações:",
        comparacoes
    )

    print(
        "Movimentos:",
        movimentos
    )

    print("\nMerge Sort")

    print(
        "Tempo:",
        f"{tempo_merge:.10f}",
        "segundos"
    )

    # Mostra apenas os 10 primeiros
    # para não destruir a medição com milhares
    # de prints.

    print("\nPrimeiros 10 registros ordenados:")

    for paciente in lista_merge[:10]:

        print(
            paciente["nome"],
            "- Espera:",
            paciente["tempo_espera"]
        )


# ============================================================
# GERADOR DE CARGA
#
# Cria N cadastros e executa uma sequência de:
# entradas, buscas, chamadas e desistências.
# ============================================================

def gerar_carga():

    global contador_eventos

    quantidade = int(
        input("Quantidade de cadastros: ")
    )

    if quantidade > MAX:

        quantidade = MAX

    # Limpa estruturas
    cadastros.clear()
    fila.clear()
    atendidos.clear()

    contador_eventos = 0

    print("\nCriando cadastros...")

    # -----------------------------
    # CPFs aleatórios
    # -----------------------------

    cpfs = gerar_cpfs_unicos(quantidade)

    inicio = time.perf_counter()

    for i, cpf in enumerate(cpfs):

        cadastros[cpf] = {

            "cpf": cpf,

            "nome": f"Paciente {i}",

            "nascimento": "01/01/2000"
        }

    fim = time.perf_counter()

    print(
        "Cadastros criados:",
        quantidade
    )

    print(
        "Tempo de criação:",
        f"{fim - inicio:.6f}",
        "segundos"
    )

    # ========================================================
    # ENTRADAS
    # ========================================================

    print("\nExecutando entradas...")

    for cpf in cpfs:

        risco = random.randint(1, 5)

        # Entrada direta para não gerar prints
        contador_eventos += 1

        fila.append({

            "cpf": cpf,

            "nome": cadastros[cpf]["nome"],

            "nascimento": cadastros[cpf]["nascimento"],

            "risco": risco,

            "entrada": contador_eventos
        })

    print(
        "Pacientes na fila:",
        len(fila)
    )

    # ========================================================
    # BUSCAS
    # ========================================================

    print("\nExecutando buscas...")

    quantidade_buscas = min(
        quantidade,
        10000
    )

    inicio = time.perf_counter()

    for _ in range(quantidade_buscas):

        cpf = random.choice(cpfs)

        buscar_cadastro(cpf)

    fim = time.perf_counter()

    print(
        "Buscas realizadas:",
        quantidade_buscas
    )

    print(
        "Tempo das buscas:",
        f"{fim - inicio:.6f}",
        "segundos"
    )

    # ========================================================
    # DESISTÊNCIAS
    # ========================================================

    print("\nExecutando desistências...")

    quantidade_desistencias = quantidade // 10

    cpfs_desistencia = random.sample(
        cpfs,
        quantidade_desistencias
    )

    inicio = time.perf_counter()

    for cpf in cpfs_desistencia:

        desistir_silencioso(cpf)

    fim = time.perf_counter()

    print(
        "Desistências realizadas:",
        quantidade_desistencias
    )

    print(
        "Tempo das desistências:",
        f"{fim - inicio:.6f}",
        "segundos"
    )

    # ========================================================
    # CHAMADAS
    # ========================================================

    print("\nExecutando chamadas...")

    quantidade_chamadas = min(
        len(fila),
        quantidade // 10
    )

    inicio = time.perf_counter()

    for _ in range(quantidade_chamadas):

        chamar_proximo()

    fim = time.perf_counter()

    print(
        "Chamadas realizadas:",
        quantidade_chamadas
    )

    print(
        "Tempo das chamadas:",
        f"{fim - inicio:.6f}",
        "segundos"
    )

    print("\nCarga finalizada.")

    print(
        "Cadastros:",
        len(cadastros)
    )

    print(
        "Na fila:",
        len(fila)
    )

    print(
        "Atendidos:",
        len(atendidos)
    )


# ============================================================
# DESISTÊNCIA SEM PRINT
#
# Usada pelo gerador de carga para não poluir a medição.
# ============================================================

def desistir_silencioso(cpf):

    for i in range(len(fila)):

        if fila[i]["cpf"] == cpf:

            fila.pop(i)

            return True

    return False


# ============================================================
# TESTE DA FILA VAZIA - R4
# ============================================================

def testar_r4_fila_vazia():

    fila.clear()

    resultado = chamar_proximo()

    if resultado is None:

        print(
            "R4: fila vazia tratada corretamente."
        )

    else:

        print(
            "Erro: R4 deveria retornar None."
        )


# ============================================================
# TESTE FUNCIONAL R2
# ============================================================

def testar_r2():

    cadastros.clear()

    cadastros["12345678901"] = {

        "cpf": "12345678901",

        "nome": "Paciente Teste",

        "nascimento": "01/01/2000"
    }

    resultado = buscar_cadastro(
        "12345678901"
    )

    print("\nTeste R2:")

    if resultado is not None:

        print(
            "Cadastro encontrado:",
            resultado
        )

    else:

        print(
            "Erro no R2."
        )

    resultado_inexistente = buscar_cadastro(
        "99999999999"
    )

    if resultado_inexistente is None:

        print(
            "CPF inexistente tratado corretamente."
        )


# ============================================================
# TESTE FUNCIONAL R4
# ============================================================

def testar_r4():

    global contador_eventos

    fila.clear()

    atendidos.clear()

    contador_eventos = 0

    # Paciente 1
    contador_eventos += 1

    fila.append({

        "cpf": "11111111111",

        "nome": "Paciente 1",

        "risco": 3,

        "entrada": contador_eventos
    })

    # Paciente 2 - maior prioridade
    contador_eventos += 1

    fila.append({

        "cpf": "22222222222",

        "nome": "Paciente 2",

        "risco": 1,

        "entrada": contador_eventos
    })

    # Paciente 3
    contador_eventos += 1

    fila.append({

        "cpf": "33333333333",

        "nome": "Paciente 3",

        "risco": 3,

        "entrada": contador_eventos
    })

    paciente = chamar_proximo()

    print("\nTeste R4:")

    if paciente is not None:

        print(
            "Paciente chamado:",
            paciente["nome"]
        )

        print(
            "Risco:",
            paciente["risco"]
        )

        # Deve ser Paciente 2
        if paciente["cpf"] == "22222222222":

            print(
                "Prioridade correta."
            )

        else:

            print(
                "Erro na regra de prioridade."
            )

    else:

        print(
            "Erro: nenhum paciente foi chamado."
        )

    testar_r4_fila_vazia()


# ============================================================
# MENU PRINCIPAL
# ============================================================

def menu():

    while True:

        print("\n")
        print("=" * 40)
        print("PRONTO ATENDIMENTO")
        print("=" * 40)

        print("1 - Cadastrar paciente")
        print("2 - Buscar cadastro")
        print("3 - Dar entrada")
        print("4 - Chamar próximo")
        print("5 - Desistir")
        print("6 - Tamanho da fila")
        print("7 - Relatório")
        print("8 - Gerar carga")
        print("9 - Experimento 2.1 - R2/R4")
        print("10 - Experimento 2.2 - Ordenação")
        print("11 - Testar R2")
        print("12 - Testar R4")
        print("0 - Sair")

        print("=" * 40)

        opcao = input("Escolha: ")

        # --------------------------------
        # R1
        # --------------------------------

        if opcao == "1":

            cpf = input("CPF: ")

            nome = input("Nome: ")

            nascimento = input(
                "Data de nascimento: "
            )

            cadastrar(
                cpf,
                nome,
                nascimento
            )

        # --------------------------------
        # R2
        # --------------------------------

        elif opcao == "2":

            cpf = input("CPF: ")

            resultado = buscar_cadastro(cpf)

            if resultado is not None:

                print("\nCadastro encontrado:")

                print(
                    "CPF:",
                    resultado["cpf"]
                )

                print(
                    "Nome:",
                    resultado["nome"]
                )

                print(
                    "Nascimento:",
                    resultado["nascimento"]
                )

            else:

                print(
                    "Cadastro inexistente."
                )

        # --------------------------------
        # R3
        # --------------------------------

        elif opcao == "3":

            cpf = input("CPF: ")

            print("\n1 - Emergência")
            print("2 - Muito urgente")
            print("3 - Urgente")
            print("4 - Pouco urgente")
            print("5 - Não urgente")

            risco = int(
                input("Risco: ")
            )

            dar_entrada(
                cpf,
                risco
            )

        # --------------------------------
        # R4
        # --------------------------------

        elif opcao == "4":

            paciente = chamar_proximo()

            if paciente is None:

                print(
                    "Não existem pacientes na fila."
                )

            else:

                print(
                    "\n===== PACIENTE CHAMADO ====="
                )

                print(
                    "Nome:",
                    paciente["nome"]
                )

                print(
                    "CPF:",
                    paciente["cpf"]
                )

                print(
                    "Risco:",
                    paciente["risco"]
                )

                print(
                    "Tempo de espera:",
                    paciente["tempo_espera"]
                )

        # --------------------------------
        # R5
        # --------------------------------

        elif opcao == "5":

            cpf = input("CPF: ")

            desistir(cpf)

        # --------------------------------
        # R6
        # --------------------------------

        elif opcao == "6":

            tamanho_fila()

        # --------------------------------
        # R7
        # --------------------------------

        elif opcao == "7":

            relatorio()

        # --------------------------------
        # GERADOR DE CARGA
        # --------------------------------

        elif opcao == "8":

            gerar_carga()

        # --------------------------------
        # EXPERIMENTO 2.1
        # --------------------------------

        elif opcao == "9":

            executar_experimento_21()

        # --------------------------------
        # EXPERIMENTO 2.2
        # --------------------------------

        elif opcao == "10":

            executar_experimento_22()

        # --------------------------------
        # TESTE R2
        # --------------------------------

        elif opcao == "11":

            testar_r2()

        # --------------------------------
        # TESTE R4
        # --------------------------------

        elif opcao == "12":

            testar_r4()

        # --------------------------------
        # SAIR
        # --------------------------------

        elif opcao == "0":

            print(
                "Programa encerrado."
            )

            break

        else:

            print(
                "Opção inválida."
            )


# ============================================================
# INÍCIO DO PROGRAMA
# ============================================================

if __name__ == "__main__":

    menu()
