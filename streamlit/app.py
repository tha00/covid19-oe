import streamlit as st
import pandas as pd

import boto3
import s3fs

BUCKET_NAME = 'covid19-oe'
FILE_KEY = 'districts_over_time.csv'

TIME_COL = 'Time'
DISTRICT_COL = 'Bezirk'
VALUE_COL = 'SevenDayAvgPer1e5'


def get_data_frame():
    """Loads the data from S3 into a pandas DataFrame."""
    data = pd.read_csv(f"s3://{BUCKET_NAME}/{FILE_KEY}", delimiter=';')
    data[TIME_COL] = pd.to_datetime(data[TIME_COL], format="%d.%m.%Y %H:%M:%S")
    return data


def add_seven_day_avg_per_100_000(data):
    """Computes the seven day average number of cases per 100.000 citizens and adds it as a column."""
    data[VALUE_COL] = 100_000 * data['AnzahlFaelle7Tage'].values / data['AnzEinwohner'].values / 7
    return data


def prepare_plot_df(data, selected_districts):
    """Prepares a data frame with one column per selected district."""
    result = pd.DataFrame()
    for district in selected_districts:
        district_df = data.loc[data[DISTRICT_COL] == district]
        result[district] = district_df[VALUE_COL].values
    result.index = data[TIME_COL].unique()
    return result


def prepare_absolute_ranking(data):
    """Prepares a data frames of districts ranked by latest seven day averages."""
    result = data.loc[data['Time'] == data['Time'].max()]
    result = result[[DISTRICT_COL, VALUE_COL]] \
        .sort_values(VALUE_COL, ascending=False) \
        .rename(columns={VALUE_COL: 'Value'}) \
        .set_index(DISTRICT_COL)
    result['Value'] = result['Value'].map('{:,.2f}'.format)
    return shorten_data(result)


def prepare_relative_ranking(data):
    """Prepares a data frames of districts ranked by the change in seven day averages compared to previous week."""
    now = data[TIME_COL].max()
    latest, past = [
        data
            .loc[data[TIME_COL] == now - pd.Timedelta(offset, unit='days')]
            .set_index(DISTRICT_COL)
        for offset in [0, 7]]
    result = latest.join(past, lsuffix='_latest', rsuffix='_past')

    result['Change'] = 100 * (result[VALUE_COL + '_latest'] / result[VALUE_COL + '_past'] - 1)
    result = result[['Change']].sort_values('Change', ascending=False)
    result['Change'] = result['Change'].map('{:+,.2f}'.format) + '%'
    return shorten_data(result)


def shorten_data(data, length=5):
    """Cuts out the middle part of a large data frame."""
    return pd.concat([
        data.head(length),
        pd.DataFrame({col: '..' for col in data.columns}, index=['..']),
        data.tail(length)
    ])


df = get_data_frame()
districts = list(df.Bezirk.unique())
df = add_seven_day_avg_per_100_000(df)

st.title("COVID-19 in Austria")
st.text("Seven day average of cases per 100.000 citizens")
selected = st.multiselect("Select districts", options=districts, default="Linz(Stadt)")

# Cases over time plot
if len(selected) > 0:
    plot_df = prepare_plot_df(df, selected)
    st.line_chart(data=plot_df)

# Current and change to last week ranking
st.header('Statistics')
abs_, rel_ = st.beta_columns(2)

with abs_:
    st.text('Latest seven day average per 100.000')
    st.dataframe(prepare_absolute_ranking(df))

with rel_:
    st.text('Change compared to last week\'s value')
    st.dataframe(prepare_relative_ranking(df))

if __name__ == "__main__":
    print(f'Reading S3 bucket: [s3://{BUCKET_NAME}/{FILE_KEY}] ...')
    df = get_data_frame()
    print(df.tail())
