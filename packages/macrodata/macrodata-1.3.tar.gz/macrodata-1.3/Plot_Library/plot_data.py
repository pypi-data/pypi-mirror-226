import pandas as pd
from pandas_datareader import wb
import country_converter as coco
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
import imageio
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
import matplotlib.pyplot as plt
from tqdm import tqdm
from .acquire_data import acquire_data

def plot_data(df,variable_name, duration, output_dir='gifs'):
    # Создаем директорию для сохранения гифок
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Удаляем все предыдущие изображения из директории
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    pio.renderers.default = "png"
    png_files = []

    #numeric_cols = df.select_dtypes(include=np.number)
    numeric_cols = df.select_dtypes(include=[np.number, 'object'])
    numeric_cols = numeric_cols.apply(pd.to_numeric, errors='coerce')
    numeric_cols = df.loc[:, numeric_cols.notna().any()]
    # Преобразуем все ячейки в числа, игнорируя ошибки
    values = []
    for col in numeric_cols.columns:
        col_values = pd.to_numeric(numeric_cols[col], errors='coerce').dropna().tolist()
        if col_values:
            values.extend(col_values)

    # вычисляем квантили
    if values:
        q_min = np.quantile(values, 0.05)
        q_max = np.quantile(values, 0.95)
    else:
        q_min = 20
        q_max = 80

    years = range(1960, 2025)
    for year in tqdm(years, desc="Processing years"):
        year_str = str(year)
        col_name = f'{variable_name} {year_str}'
        if col_name not in df.columns:
            continue

        # Создать карту
        map_data = dict(
            type='choropleth',
            locations=df['Country Code'],
            z=df[col_name],
            text=df['Country'],
            zmin=q_min,
            zmax=q_max
        )

        map_layout = dict(title=col_name, geo=dict(showframe=True))
        map_actual = go.Figure(data=[map_data], layout=map_layout)
        filename = f"{col_name}.png"
        filepath = os.path.join(output_dir, filename)
        png_files.append(filepath)
        pio.write_image(map_actual, filepath)

    gif_filename = os.path.join(output_dir, f'{variable_name}.gif')
    with imageio.get_writer(gif_filename, mode='I', duration=duration) as writer:
        for filename in png_files:
            image = imageio.imread(filename)
            writer.append_data(image)

    # Remove PNG files
    for filename in png_files:
        os.remove(filename)

    # Convert the GIF animation to another GIF file using moviepy
    clip = VideoFileClip(gif_filename)
    clip_duration = clip.duration
    if clip_duration < duration:
        raise ValueError("Duration of the clip is less than the duration of the animation")
    start_time = duration
    end_time = clip_duration - duration
    subclip = clip.subclip(start_time, end_time)
    subclip.write_gif(os.path.join(output_dir, f"{variable_name}_final.gif"), loop=True)


def make_gif(variable_name,duration = 0.1, countries='all', start_date='1960-01-01', end_date='2022-12-31'):
    variables_dict = {
    "GDP per capita (constant 2010 US$)": "NY.GDP.PCAP.KD",
    "GDP growth (annual %)": "NY.GDP.MKTP.KD.ZG",
    "Inflation, consumer prices (annual %)": "FP.CPI.TOTL.ZG",
    "Trade (% of GDP)": "NE.TRD.GNFS.ZS",
    "Foreign direct investment, net inflows (% of GDP)": "BX.KLT.DINV.WD.GD.ZS",
    "Net migration": "SM.POP.NETM",
    "Population, total": "SP.POP.TOTL",
    "Urban population (% of total population)": "SP.URB.TOTL.IN.ZS",
    "Rural population (% of total population)": "SP.RUR.TOTL.ZS",
    "Life expectancy at birth, total (years)": "SP.DYN.LE00.IN",
    "Mortality rate, under-5 (per 1,000 live births)": "SH.DYN.MORT",
    "Prevalence of undernourishment (% of population)": "SN.ITK.DEFC.ZS",
    "CO2 emissions (metric tons per capita)": "EN.ATM.CO2E.PC",
    "Renewable energy consumption (% of total final energy consumption)": "EG.FEC.RNEW.ZS",
    "Electric power consumption (kWh per capita)": "EG.USE.ELEC.KH.PC",
    "Mobile cellular subscriptions (per 100 people)": "IT.CEL.SETS.P2",
    "Internet users (per 100 people)": "IT.NET.USER.P2",
    "Labor force participation rate, total (% of total population ages 15+)": "SL.TLF.TOTL.IN.ZS",
    "Unemployment, total (% of total labor force)": "SL.UEM.TOTL.ZS",}
    variable = variables_dict[variable_name]
    df = acquire_data( variable_name,variable, countries, start_date, end_date)
    plot_data(df, variable_name, duration)
        