import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Wyszukiwanie duplikatów w kolumnie Task Name")

# Wczytanie pliku CSV
uploaded_file = st.file_uploader("Wgraj plik CSV (UTF-8)", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    except Exception as e:
        st.error(f"Błąd podczas wczytywania pliku CSV: {e}")
        st.stop()

    if 'Task Name' not in df.columns:
        st.error("Brak kolumny 'Task Name' w pliku CSV.")
        st.stop()

    st.subheader("Podgląd danych")
    st.dataframe(df)

    # Czyszczenie wartości: usunięcie białych znaków i zamiana na małe litery
    df['Task Name Clean'] = (
        df['Task Name']
        .astype(str)
        .str.replace(r"\s+", "", regex=True)
        .str.lower()
    )

    # Policz wystąpienia i wyłuskaj duplikaty
    counts = df['Task Name Clean'].value_counts()
    duplicates = counts[counts > 1]

    if not duplicates.empty:
        # Przygotowanie DataFrame duplikatów
        dup_df = duplicates.rename_axis('Task Name').reset_index(name='Count')

        st.subheader("Znalezione duplikaty")
        st.dataframe(dup_df)

        # Generowanie pliku Excel do pobrania
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            dup_df.to_excel(writer, index=False, sheet_name='Duplikaty')
        output.seek(0)

        st.download_button(
            label="Pobierz plik z duplikatami (Excel)",
            data=output,
            file_name="duplikaty_task_name.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("Nie znaleziono duplikatów w kolumnie 'Task Name'.")
