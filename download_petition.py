import requests
import pandas as pd
from datetime import datetime
import re
from io import StringIO
import pdb

def get_current_petitions() -> pd.DataFrame:
    url = "https://epetitionen.bundestag.de/epet/petuebersicht/mz.nc.content.teaser-petitionen-table.$$$.sort.mz_d.ssi.true.status.2.page.0.batchsize.10.html" 
    response = requests.get(url=url)
    website = response.text
    df = pd.read_html(StringIO(website))[0]
    df['end_date_string'] = df['Mitzeichnungsfrist'].str.extract(r'(\d{2}\.\d{2}.\d{4}$)')
    df['end_date'] = pd.to_datetime(df['end_date_string'], format='%d.%m.%Y')
    df['days_until'] = (df['end_date'] - pd.to_datetime(datetime.today().date())).dt.days

    petition_links = re.findall(r'href="([^"]+)"', website)


    df['url'] = ''
    for index, row in df.iterrows():
        id = row["Id-Nr."]
        subpage = [s for s in petition_links if f"Petition_{id}.nc.html" in s][0]
        url = f"https://epetitionen.bundestag.de{subpage}"
        df.at[index, 'url'] = url
    return df


def get_10k_petitionen() -> list:
    df = get_current_petitions()
    post_list = []

    for _, row in df.iterrows():
        if row["Mitzeichnungen"]>10000:
            post = f'Eine neue Petition hat mehr als 10.000 Unterschriften: \n Titel: {row["Titel"]} \n Mitzeichnungen: {row["Mitzeichnungen"]} \n Diese Petition endet in {row["days_until"]} Tagen am {row["end_date_string"]} \n Link: {row["url"]} \n #bundestag #petition'
            petition_id = row["Id-Nr."]
            post_list.append(
                {
                    "id": petition_id,
                    "post": post
                }
            )
 

    
    return post_list
    
if __name__=="__main__":
    get_10k_petitionen()