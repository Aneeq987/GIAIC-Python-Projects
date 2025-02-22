import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="🚀 File Transformer", layout="wide")

st.title("🚀 File Transformer")
st.write("Easily switch between CSV and Excel formats with smart data optimization and insights!")

uploaded_files = st.file_uploader("📤 Upload your data files (CSV/XLSX):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_name = file.name
        file_size = file.size / 1024
        file_ext = os.path.splitext(file_name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file) if file.size > 0 else None
        elif file_ext == ".xlsx":
            df = pd.read_excel(file) if file.size > 0 else None
        else:
            st.error(f"❌ Unsupported format: {file_ext}")
            continue

        if df is None:
            st.error(f"❌ The file {file_name} contains no data.")
            continue

        st.write(f"**📜 File:** {file_name}")
        st.write(f"**📏 Size:** {file_size:.2f} KB")

        st.write("👀 **Quick Look at Data**")
        st.dataframe(df.head())

        st.subheader("🛠 **Data Refinement Tools**")
        col1, col2 = st.columns(2)

        if st.checkbox(f"🧼 Clean {file_name}"):
            with col1:
                if st.button(f"🚫 Remove Duplicates ({file_name})"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates Eliminated!")

            with col2:
                if st.button(f"🔄 Fill Missing Values ({file_name})"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Gaps Filled!")

        st.subheader("📌 **Pick Essential Columns**")
        selected_columns = st.multiselect(f"✅ Choose columns from {file_name}", df.columns, default=df.columns)
        df = df[selected_columns]

        st.subheader("📊 **Visual Insights**")
        if st.checkbox(f"📉 Display Chart for {file_name}"):
            numeric_df = df.select_dtypes(include='number')
            if not numeric_df.empty:
                st.bar_chart(numeric_df.iloc[:, :2]) 
            else:
                st.warning("⚠️ No numerical data available for graphs.")
            
        st.subheader("🔃 **Transform Format**")
        conversion_type = st.radio(f"📂 Convert {file_name} into:", ["CSV", "Excel"], key=file_name)

        if st.button(f"🔄 Process {file_name}"):
            buffer = BytesIO()
            new_extension = ".csv" if conversion_type == "CSV" else ".xlsx"
            mime_type = "text/csv" if conversion_type == "CSV" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
            else:
                df.to_excel(buffer, index=False)

            buffer.seek(0)

            st.download_button(
                label=f"⬇️ Download {file_name.replace(file_ext, new_extension)}",
                data=buffer,
                file_name=file_name.replace(file_ext, new_extension),
                mime=mime_type
            )

st.success("🎊✨ Processing Complete!")
