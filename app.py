import streamlit as st
import pandas as pd
import zipfile
import io

st.title("📊 Outil CSV - Concaténation & Split")

mode = st.radio("Choisir une action :", ["Concaténer des fichiers CSV", "Splitter un fichier CSV"])

if mode == "Concaténer des fichiers CSV":
    st.subheader("📎 Concaténation")
    uploaded_files = st.file_uploader("Uploader plusieurs fichiers CSV", type="csv", accept_multiple_files=True)

    if uploaded_files:
        dfs = [pd.read_csv(f) for f in uploaded_files]
        df_final = pd.concat(dfs, ignore_index=True)

        st.success(f"{len(uploaded_files)} fichiers concaténés.")

        csv_output = df_final.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Télécharger le fichier concaténé", csv_output, file_name="fichier_concatene.csv", mime="text/csv")

elif mode == "Splitter un fichier CSV":
    st.subheader("✂️ Split")
    uploaded_file = st.file_uploader("Uploader un fichier CSV à splitter", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        total_rows = len(df)
        max_splits = min(50, total_rows)

        n_parts = st.number_input("Nombre de splits souhaités :", min_value=2, max_value=max_splits, step=1)

        if st.button("🔪 Splitter"):
            part_size = total_rows // n_parts
            dfs = []

            for i in range(n_parts):
                start = i * part_size
                end = None if i == n_parts - 1 else (i + 1) * part_size
                dfs.append(df.iloc[start:end])

            # Créer un fichier zip en mémoire
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for i, df_part in enumerate(dfs, start=1):
                    csv_bytes = df_part.to_csv(index=False).encode('utf-8')
                    zip_file.writestr(f"part{i}.csv", csv_bytes)

            zip_buffer.seek(0)

            st.success(f"{n_parts} fichiers créés et ajoutés à l'archive ZIP.")
            st.download_button("📦 Télécharger l'archive ZIP", zip_buffer, file_name="fichiers_splittes.zip", mime="application/zip")
