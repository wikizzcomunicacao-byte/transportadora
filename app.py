import os
import pandas as pd
import streamlit as st

# Configuração da página para ocupar a largura total
st.set_page_config(
    page_title="Gestão de Transportadora", page_icon="🚚", layout="wide"
)

# Arquivo CSV para salvar os dados localmente
ARQUIVO_DADOS = "dados_transportadora.csv"


def carregar_dados():
  if os.path.exists(ARQUIVO_DADOS):
    return pd.read_csv(ARQUIVO_DADOS)
  else:
    return pd.DataFrame(columns=[
        "ID",
        "DataHora",
        "Tipo",
        "Motorista",
        "Plataforma",
        "Pacotes",
        "KM",
        "Rota",
        "Valor_Abastecimento",
        "Litros",
    ])


def salvar_dados(df):
  df.to_csv(ARQUIVO_DADOS, index=False)


df_global = carregar_dados()

# --- MENU LATERAL (SELEÇÃO DE PERFIL) ---
st.sidebar.title("🚚 Sistema Transportadora")
perfil = st.sidebar.radio(
    "Selecione o seu perfil:", ["Funcionário (Motorista)", "Gestor (Dashboard)"]
)

# Lista dos 4 funcionários/motoristas
MOTORISTAS = ["Motorista 01", "Motorista 02", "Motorista 03", "Motorista 04"]

# ==========================================
# 1. PAINEL DO FUNCIONÁRIO (COM O NOVO LAYOUT)
# ==========================================
if perfil == "Funcionário (Motorista)":
  st.subheader("Painel de Lançamento Diário")
  motorista_selecionado = st.selectbox(
      "Identificação do Motorista:", MOTORISTAS
  )

  st.markdown("---")

  # Abas principais baseadas no modelo solicitado
  aba_coleta, aba_km, aba_abast = st.tabs(
      [
          "📦 1. Registrar Coleta",
          "⏱️ 2. Registrar KM / Viagem",
          "⛽ 3. Abastecimento",
      ]
  )

  # --- ABA 1: REGISTRAR COLETA ---
  with aba_coleta:
    with st.form("form_coleta_visual", clear_on_submit=True):
      st.markdown("### Selecione a Plataforma")

      # Simulando os botões de seleção de plataforma
      plataforma = st.radio(
          "PLATAFORMA *", ["Shopee", "Mercado Livre"], horizontal=True
      )

      col_a, col_b = st.columns(2)
      with col_a:
        qtd_pacotes = st.number_input(
            "QTD. DE PACOTES *", min_value=1, step=1, value=10
        )
      with col_b:
        rota_obs = st.text_input(
            "ROTA / GALPÃO / OBS.", placeholder="Ex: Rota SP-04 / Galpão Jagua"
        )

      data_hora = st.text_input(
          "DATA E HORA *",
          value=pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
      )

      enviar_coleta = st.form_submit_button(
          "💾 Salvar Registro de Coleta", use_container_width=True
      )

      if enviar_coleta:
        novo_id = len(df_global) + 1
        novo_registro = {
            "ID": novo_id,
            "DataHora": data_hora,
            "Tipo": "Coleta",
            "Motorista": motorista_selecionado,
            "Plataforma": plataforma,
            "Pacotes": qtd_pacotes,
            "KM": 0.0,
            "Rota": rota_obs,
            "Valor_Abastecimento": 0.0,
            "Litros": 0.0,
        }
        df_global = pd.concat(
            [df_global, pd.DataFrame([novo_registro])], ignore_index=True
        )
        salvar_dados(df_global)
        st.success(
            f"✅ Coleta de {qtd_pacotes} pacotes ({plataforma}) salva com"
            " sucesso!"
        )

  # --- ABA 2: REGISTRAR KM / VIAGEM ---
  with aba_km:
    with st.form("form_km", clear_on_submit=True):
      st.markdown("### Controle de Quilometragem")

      col1, col2 = st.columns(2)
      with col1:
        km_rodado = st.number_input(
            "KM RODADO / ATUAL *", min_value=0.0, step=1.0
        )
      with col2:
        detalhe_viagem = st.text_input(
            "DESTINO / ROTA", placeholder="Ex: Viagem Entrega Regional"
        )

      data_hora_km = st.text_input(
          "DATA E HORA *",
          value=pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
          key="dh_km",
      )

      enviar_km = st.form_submit_button(
          "💾 Salvar Quilometragem", use_container_width=True
      )

      if enviar_km:
        novo_id = len(df_global) + 1
        novo_registro = {
            "ID": novo_id,
            "DataHora": data_hora_km,
            "Tipo": "KM",
            "Motorista": motorista_selecionado,
            "Plataforma": "",
            "Pacotes": 0,
            "KM": km_rodado,
            "Rota": detalhe_viagem,
            "Valor_Abastecimento": 0.0,
            "Litros": 0.0,
        }
        df_global = pd.concat(
            [df_global, pd.DataFrame([novo_registro])], ignore_index=True
        )
        salvar_dados(df_global)
        st.success(f"✅ Quilometragem de {km_rodado} KM salva com sucesso!")

  # --- ABA 3: ABASTECIMENTO ---
  with aba_abast:
    with st.form("form_abastecimento", clear_on_submit=True):
      st.markdown("### Registro de Combustível")

      col1, col2 = st.columns(2)
      with col1:
        valor_abast = st.number_input(
            "VALOR TOTAL (R$) *", min_value=0.0, step=0.01
        )
      with col2:
        litros_abast = st.number_input(
            "LITROS (Opcional)", min_value=0.0, step=0.1
        )

      data_hora_abast = st.text_input(
          "DATA E HORA *",
          value=pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
          key="dh_abast",
      )

      enviar_abast = st.form_submit_button(
          "💾 Salvar Abastecimento", use_container_width=True
      )

      if enviar_abast:
        novo_id = len(df_global) + 1
        novo_registro = {
            "ID": novo_id,
            "DataHora": data_hora_abast,
            "Tipo": "Abastecimento",
            "Motorista": motorista_selecionado,
            "Plataforma": "",
            "Pacotes": 0,
            "KM": 0.0,
            "Rota": "Abastecimento",
            "Valor_Abastecimento": valor_abast,
            "Litros": litros_abast,
        }
        df_global = pd.concat(
            [df_global, pd.DataFrame([novo_registro])], ignore_index=True
        )
        salvar_dados(df_global)
        st.success(f"✅ Abastecimento de R$ {valor_abast:.2f} salvo com sucesso!")

# ==========================================
# 2. PAINEL DO GESTOR (DASHBOARD)
# ==========================================
elif perfil == "Gestor (Dashboard)":
  st.header("📊 Painel de Controle do Gestor")

  if df_global.empty:
    st.info("Nenhum lançamento registrado no sistema ainda.")
  else:
    df_coletas = df_global[df_global["Tipo"] == "Coleta"]
    df_abast = df_global[df_global["Tipo"] == "Abastecimento"]
    df_km = df_global[df_global["Tipo"] == "KM"]

    total_pacotes = (
        int(df_coletas["Pacotes"].sum()) if not df_coletas.empty else 0
    )
    total_gasto = (
        float(df_abast["Valor_Abastecimento"].sum())
        if not df_abast.empty
        else 0.0
    )
    total_km = float(df_km["KM"].sum()) if not df_km.empty else 0.0

    # Cartões de Métricas
    c1, c2, c3 = st.columns(3)
    c1.metric("📦 Total de Pacotes", total_pacotes)
    c2.metric("⛽ Gasto com Combustível", f"R$ {total_gasto:.2f}")
    c3.metric("🛣️ KM Total Registrado", f"{total_km:.1f} KM")

    st.markdown("---")

    col_graf1, col_graf2 = st.columns(2)
    with col_graf1:
      st.subheader("Pacotes por Plataforma")
      if not df_coletas.empty:
        st.bar_chart(df_coletas.groupby("Plataforma")["Pacotes"].sum())

    with col_graf2:
      st.subheader("Desempenho por Motorista (Pacotes)")
      if not df_coletas.empty:
        st.bar_chart(df_coletas.groupby("Motorista")["Pacotes"].sum())

    st.markdown("---")
    st.subheader("📋 Histórico Completo de Lançamentos")

    # Gerenciamento / Exclusão
    if st.checkbox("Habilitar exclusão de registro incorreto"):
      id_exc = st.selectbox(
          "Selecione o ID do registro:", options=df_global["ID"].tolist()
      )
      if st.button("Excluir Item Selecionado 🗑️"):
        df_global = df_global[df_global["ID"] != id_exc]
        salvar_dados(df_global)
        st.success(f"Registro ID {id_exc} removido!")
        st.rerun()

    st.dataframe(df_global, use_container_width=True)

    st.download_button(
        label="📥 Baixar Planilha de Relatório (CSV)",
        data=df_global.to_csv(index=False).encode("utf-8"),
        file_name="relatorio_geral_transportadora.csv",
        mime="text/csv",
    )
