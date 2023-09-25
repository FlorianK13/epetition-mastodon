from mastodon import Mastodon
from download_petition import get_10k_petitionen
import csv
import os

def main():
    mastodon = Mastodon(access_token = 'pytooter_usercred.secret')
    petitionen_list = get_10k_petitionen()
    if petitionen_list is None:
        return None
    if len(petitionen_list) >2:
        return None
    
    for petition in petitionen_list:
        if is_already_posted(petition):
            return None
               
        mastodon.status_post(petition["post"], visibility="public", language="de")

def is_already_posted(petition):
    id = petition["id"]
    post = petition["post"]
    csv_file = "posts.csv"
    
    # Check if the csv_file exists, create it if not
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["id", "post"])

    # Read the csv_file to check if the given id exists
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if row[0] == str(id):
                return True

    # If the id doesn't exist, append it to the csv and return False
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([id, post])
    
    return False


if __name__ == "__main__":
    main()