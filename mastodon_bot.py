from mastodon import Mastodon
from download_petition import get_10k_petitionen
import os
import csv
import pandas as pd
from datetime import date



def main():
    today = date.today()
    print("Today's date:", today)
    mastodon = Mastodon(access_token = 'pytooter_usercred.secret')
    petitionen_list = get_10k_petitionen()
    if petitionen_list is None:
        return None
    if len(petitionen_list) >2:
        print(f"Petition list longer than 2: {petitionen_list}")
        return None
    
    for petition in petitionen_list:
        if is_already_posted(petition):
            print("Post already posted")
            continue
            
        else:
            mastodon.status_post(petition["post"], visibility="public", language="de")
            print("New post was uploaded to troet.cafe")

def is_already_posted(petition):
    id = int(petition["id"])
    post = petition["post"].split(".nc.html")[0]+".nc.html"
    csv_file = "posts.csv"
    
    # Check if the csv_file exists, create it if not
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["id", "post"])

    # Read the csv_file to check if the given id exists
    posts_df = pd.read_csv(csv_file, encoding="latin", index_col="id")
    
    for df_index, row in posts_df.iterrows():
        if df_index == id:
                return True
        print(row)
    new_df = pd.DataFrame({"post": [post]}, index=[id]).rename_axis("id")
    posts_df = pd.concat([posts_df, new_df])
    posts_df.to_csv(csv_file, encoding="latin")
    return False



if __name__ == "__main__":
    main()