import time
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import threading
import multiprocessing
from math import sqrt

def num_pft(start, end, listnum):
    for i in range(start, end):
        sum = 1
        for j in range(2, int(sqrt(i)+1)):
            if i % j == 0:
                sum += j
                if j!= i//j:
                    sum+=i//j
        if sum == i:
            listnum.append(i)

st.title("Trabalho de Arquitetura de Computadores II")
st.write("Encontrar numeros perfeitos")
num1 = st.number_input("Digite o início do intervalo:", min_value=1, format="%d")
num2 = st.number_input("Digite o fim do intervalo:", min_value=1, format="%d")
opcao = st.selectbox("Escolha uma opção:", ["Sequencial", "Threading", "Multiprocessing", "Comparar os 3"])
if st.button("Enviar"):
    with st.spinner("Calculando..."):
        if opcao == "Sequencial":
            num_perfect=[]
            tempo_inicial=time.time()
            num_pft(num1,num2,num_perfect)
            tempo_final=time.time()
            for i in num_perfect:
                st.write(i)
            st.write("Tempo de execução: {:.2f} segundos".format(tempo_final - tempo_inicial))
        elif opcao == "Threading":
            threads = []
            resultados = []
            parte = (num2 - num1) // 4
            tempo_inicial = time.time()
            for i in range(4):
                ini = num1 + i * parte
                if i < 3:
                    fim = num1 + (i + 1) * parte
                else:
                    fim = num2
                t = threading.Thread(target=num_pft, args=(ini, fim, resultados))
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
            tempo_final=time.time()
            for i in resultados:
                st.write(i)
            st.write("Tempo de execucao: {:.2f} segundos" .format(tempo_final-tempo_inicial))

        elif opcao== "Multiprocessing":      
            start_time = time.time()
            process = []
            with multiprocessing.Manager() as manager:
                num_perfect = manager.list()
                parte = (num2 - num1) // 4
                for i in range(4):
                    ini = num1 + i * parte
                    fim = num1 + (i + 1) * parte if i < 3 else num2
                    p = multiprocessing.Process(target=num_pft, args=(ini, fim, num_perfect))
                    process.append(p)
                    p.start()
                
                for p in process:
                    p.join()
                
                results = list(num_perfect)
            
                end_time = time.time()
                for i in results:
                    st.write(i)
                st.write(f"Tempo de execução: {end_time - start_time:.2f} segundos")
        elif opcao == "Comparar os 3":
                tempos = {
                    "Método": [],
                    "Tempo (s)": []
                }
                
                grafico_placeholder = st.empty()

                # SEQUENCIAL
                tempo_inicial = time.time()
                num_pft(num1, num2, [])
                tempo_final = time.time()
                tempos["Método"].append("Sequencial")
                tempos["Tempo (s)"].append(tempo_final - tempo_inicial)
                df = pd.DataFrame(tempos)
                grafico_placeholder.line_chart(df.set_index("Método"))

                # THREADING
                parte = (num2 - num1) // 4
                threads = []
                resultados = []
                tempo_inicial = time.time()
                for i in range(4):
                    ini = num1 + i * parte
                    fim = num1 + (i + 1) * parte if i < 3 else num2
                    t = threading.Thread(target=num_pft, args=(ini, fim, resultados))
                    threads.append(t)
                    t.start()
                for t in threads:
                    t.join()
                tempo_final = time.time()
                tempos["Método"].append("Threading")
                tempos["Tempo (s)"].append(tempo_final - tempo_inicial)
                df = pd.DataFrame(tempos)
                grafico_placeholder.line_chart(df.set_index("Método"))

                # MULTIPROCESSING
                tempo_inicial = time.time()
                with multiprocessing.Manager() as manager:
                    num_perfect = manager.list()
                    processes = []
                    for i in range(4):
                        ini = num1 + i * parte
                        fim = num1 + (i + 1) * parte if i < 3 else num2
                        p = multiprocessing.Process(target=num_pft, args=(ini, fim, num_perfect))
                        processes.append(p)
                        p.start()
                    for p in processes:
                        p.join()
                    results = list(num_perfect)
                tempo_final = time.time()
                tempos["Método"].append("Multiprocessing")
                tempos["Tempo (s)"].append(tempo_final - tempo_inicial)
                df = pd.DataFrame(tempos)
                grafico_placeholder.line_chart(df.set_index("Método"))
                st.subheader("Tabela de Tempos de Execução")
                st.table(df)
    st.success("Cálculo concluído!")