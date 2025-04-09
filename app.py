import streamlit as st
import pandas as pd
import plotly.express as px

# Настройка страницы Streamlit
st.set_page_config(page_title="Excel Data Visualizer", layout="wide")

# Заголовок приложения
st.title("📊 Продажи на маркетплейсах")
st.markdown("Загрузите Excel-файл")

# Загрузка файла
uploaded_file = st.file_uploader("Выберите Excel-файл", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Чтение данных из Excel
        df = pd.read_excel(uploaded_file, skiprows=1)
        df = df[df['Группа услуг'] == 'Продажи']
        df.reset_index(drop=True, inplace=True)
        print(df.columns)



        st.subheader("Суммарные продажи по месяцам")

        df['Дата начисления'] = df['Дата начисления'].astype(str)
        df['Дата начисления'] = pd.to_datetime(df['Дата начисления']).dt.strftime('%Y-%m-%d')

        df['month'] = pd.to_datetime(df['Дата начисления']).dt.to_period('M').dt.to_timestamp()

        # Группируем по месяцу (и другим нужным полям, например, по площадке)
        monthly_df = df.groupby(['month'], as_index=False).agg({
            'Сумма итого, руб': ['sum', 'mean', 'count'],  # Сумма, среднее, количество дней с продажами
        })

        # Упрощаем мультииндекс в колонках
        monthly_df.columns = ['Месяц', 'Суммарный чек', 'Средний чек', 'Количество заказов']

        st.dataframe(monthly_df.head())


        # Выбор столбцов для визуализации
        st.subheader("Настройки визуализации")
        columns = monthly_df.columns.tolist()

        col1, col2 = st.columns(2)

        with col1:
            x_axis = st.selectbox("Выберите столбец для оси X", options=columns)

        with col2:
            y_axis = st.selectbox("Выберите столбец для оси Y", options=columns)

        # Выбор типа графика
        chart_type = st.selectbox(
            "Выберите тип графика",
            ["Линейный", "Столбчатый", "Круговой", "Точечный", "Гистограмма"]
        )

        # Построение графика
        st.subheader("Визуализация данных")

        if chart_type == "Линейный":
            fig = px.line(monthly_df, x=x_axis, y=y_axis, title=f"Линейный график: {y_axis} по {x_axis}")
        elif chart_type == "Столбчатый":
            fig = px.bar(monthly_df, x=x_axis, y=y_axis, title=f"Столбчатая диаграмма: {y_axis} по {x_axis}")
        elif chart_type == "Круговой":
            fig = px.pie(monthly_df, names=x_axis, values=y_axis, title=f"Круговая диаграмма: {y_axis} по {x_axis}")
        elif chart_type == "Точечный":
            fig = px.scatter(monthly_df, x=x_axis, y=y_axis, title=f"Точечный график: {y_axis} по {x_axis}")
        elif chart_type == "Гистограмма":
            fig = px.histogram(monthly_df, x=x_axis, title=f"Гистограмма: распределение {x_axis}")

        st.plotly_chart(fig, use_container_width=True)

        # Дополнительная информация о данных
        st.subheader("Статистика данных")
        st.write(monthly_df.describe())
    except Exception as e:
        st.error(f"Произошла ошибка при обработке файла: {e}")
else:
    st.info("Пожалуйста, загрузите Excel-файл для визуализации данных.")
