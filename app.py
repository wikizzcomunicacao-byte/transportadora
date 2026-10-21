import os
import pandas as pd
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Gestão de Transportadora", page_icon="🚚", layout="wide"
)

# Arquivo CSV para persistência simples dos dados
ARQUIVO_DADOS = "dados_transportadora.csv"


def carregar_dados():
  if os.path.exists(ARQUIVO_DADOS):
    return pd.read_csv(ARQUIVO_DADOS)
  else:
    # Cria um DataFrame vazio com a estrutura necessária
    return pd.DataFrame(columns=[
        "ID",
        "Data",
        "Tipo",
        "Motorista",
        "Plataforma",
        "Pacotes",
        "KM",
        "Valor_Abastecimento",
        "Litros",
    ])


def salvar_dados(df):
  df.to_csv(ARQUIVO_DADOS, index=False)


df_global = carregar_dados()

# --- MENU LATERAL: ESCOLHA DE PERFIL ---
st.sidebar.title("🚚 Painel Transportadora")
perfil = st.sidebar.radio(
    "Selecione o seu perfil:", ["Funcionário (Motorista)", "Gestor (Dashboard)"]
)

# Lista dos 4 motoristas
MOTORISTAS = ["João Silva", "Carlos Souza", "Marcos Lima", "Pedro Santos"]

# ==========================================
# 1. PAINEL DO FUNCIONÁRIO (MOTORISTA)
# ==========================================
if perfil == "Funcionário (Motorista)":
  st.header("📱 Registro Diário do Motorista")
  st.write(
    "Insira os dados da sua rota ou abastecimento de forma rápida pelo"
    " celular."
  )

  motorista_selecionado = st.selectbox(
      "Selecione seu Nome:", MOTORISTAS, key="motorista_func"
  )

  aba = st.radio(
      "O que você deseja registrar?",
      ["📦 Coleta de Pacotes", "⛽ Abastecimento e KM"],
      horizontal=True,
  )

  st.markdown("---")

  if aba == "📦 Coleta de Pacotes":
    st.subheader("Registro de Coleta")
    with st.form("form_coleta", clear_on_submit=True):
      plataforma = st.selectbox(
          "Plataforma:", ["Shopee", "Mercado Livre", "Outra"]
      )
      quantidade = st.number_input(
          "Quantidade de Pacotes:", min_value=1, step=1, value=10
      )
      data_registro = st.date_input("Data da Coleta")

      enviar = st.form_submit_button("Registrar Coleta ✅")

      if enviar:
        novo_id = len(df_global) + 1
        novo_registro = {
            "ID": novo_id,
            "Data": str(data_registro),
            "Tipo": "Coleta",
            "Motorista": motorista_selecionado,
            "Plataforma": plataforma,
            "Pacotes": quantidade,
            "KM": 0.0,
            "Valor_Abastecimento": 0.0,
            "Litros": 0.0,
        }
        df_global = pd.concat(
            [df_global, pd.DataFrame([novo_registro])], ignore_index=True
        )
        salvar_dados(df_global)
        st.success(
            f"✅ Coleta de {quantidade} pacotes ({plataforma}) registrada com"
            " sucesso!"
        )

  elif aba == "⛽ Abastecimento e KM":
    st.subheader("Registro de Abastecimento & Quilometragem")
    with st.form("form_abastecimento", clear_on_submit=True):
      km_atual = st.number_input(
          "Quilometragem Atual (KM):", min_value=0.0, step=1.0
      )
      valor_total = st.number_input(
          "Valor Total Pago (R$):", min_value=0.0, step=0.01
      )
      litros = st.number_input(
          "Litros Abastecidos (Opcional):", min_value=0.0, step=0.1
      )
      data_registro = st.date_input("Data do Abastecimento")

      enviar = st.form_submit_button("Registrar Abastecimento ⛽")

      if enviar:
        novo_id = len(df_global) + 1
        novo_registro = {
            "ID": novo_id,
            "Data": str(data_registro),
            "Tipo": "Abastecimento",
            "Motorista": motorista_selecionado,
            "Plataforma": "",
            "Pacotes": 0,
            "KM": km_atual,
            "Valor_Abastecimento": valor_total,
            "Litros": litros,
        }
        df_global = pd.concat(
            [df_global, pd.DataFrame([novo_registro])], ignore_index=True
        )
        salvar_dados(df_global)
        st.success(
            f"✅ Abastecimento de R$ {valor_total:.2f} no KM {km_atual}"
            " registrado com sucesso!"
        )

# ==========================================
# 2. PAINEL DO GESTOR (DASHBOARD)
# ==========================================
elif perfil == "Gestor (Dashboard)":
  st.header("📊 Painel de Controle do Gestor")
  st.write("Acompanhe o desempenho da frota, coletas e custos em tempo real.")

  if df_global.empty:
    st.info("Nenhum dado registrado até o momento.")
  else:
    # Métricas Principais
    df_coletas = df_global[df_global["Tipo"] == "Coleta"]
    df_abast = df_global[df_global["Tipo"] == "Abastecimento"]

    total_pacotes = (
        int(df_coletas["Pacotes"].sum()) if not df_coletas.empty else 0
    )
    total_gasto = (
        float(df_abast["Valor_Abastecimento"].sum())
        if not df_abast.empty
        else 0.0
    )
    total_abastecimentos = len(df_abast)

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total de Pacotes Coletados", total_pacotes)
    col2.metric("⛽ Gasto Total com Combustível", f"R$ {total_gasto:.2f}")
    col3.metric("📝 Registros de Abastecimento", total_abastecimentos)

    st.markdown("---")

    # Filtros e Detalhes
    st.subheader("📈 Desempenho por Plataforma")
    if not df_coletas.empty:
      resumo_plat = df_coletas.groupby("Plataforma")["Pacotes"].sum()
      st.bar_chart(resumo_plat)

    st.subheader("👥 Produtividade por Motorista (Pacotes)")
    if not df_coletas.empty:
      resumo_mot = df_coletas.groupby("Motorista")["Pacotes"].sum()
      st.bar_chart(resumo_mot)

    st.markdown("---")
    st.subheader("📋 Histórico Completo de Lançamentos")

    # Opção para excluir registros errados se necessário
    if st.checkbox("Exibir opção de gerenciar/excluir registros"):
      id_para_excluir = st.selectbox(
          "Selecione o ID do registro para excluir:",
          options=df_global["ID"].tolist(),
      )
      if st.button("Excluir Registro Selecionado 🗑️"):
        df_global = df_global[df_global["ID"] != id_para_excluir]
        salvar_dados(df_global)
        st.success(f"Registro ID {id_para_excluir} excluído com sucesso!")
        st.rerun()

    st.dataframe(df_global, use_container_width=True)

    # Botão para baixar CSV
    st.download_button(
        label="📥 Baixar Relatório em CSV",
        data=df_global.to_csv(index=False).encode("utf-8"),
        file_name="relatorio_transportadora.csv",
        mime="text/csv",
    )
