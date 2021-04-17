import streamlit as st
import pandas as pd

import boto3
import s3fs

BUCKET_NAME = "covid19-oe"
FILE_KEY = "districts_over_time.csv"


@st.cache
def get_data_frame():
    return pd.read_csv(f"s3://{BUCKET_NAME}/{FILE_KEY}", delimiter=';')


df = get_data_frame()
districts = list(df.Bezirk.unique())

st.title("COVID-19 in Austria")
selected = st.multiselect("Select districts", options=districts, default="Linz(Stadt)")


def prepare_plot_df(data, selected_districts):
    output = pd.DataFrame()
    for district in selected_districts:
        district_df = data.loc[data['Bezirk'] == district]
        output[district] = 100_000 * district_df['AnzahlFaelle7Tage'].values / district_df['AnzEinwohner'].values / 7

    output.index = pd.to_datetime(data['Time'].unique(), format="%d.%m.%Y %H:%M:%S")
    return output


if len(selected) > 0:
    plot_df = prepare_plot_df(df, selected)
    st.text("Seven day average of cases per 100.000 citizens")
    st.line_chart(data=plot_df)

if __name__ == "__main__":
    print(f'Reading S3 bucket: [s3://{BUCKET_NAME}/{FILE_KEY}] ...')
    df = get_data_frame()
    print(df.tail())
