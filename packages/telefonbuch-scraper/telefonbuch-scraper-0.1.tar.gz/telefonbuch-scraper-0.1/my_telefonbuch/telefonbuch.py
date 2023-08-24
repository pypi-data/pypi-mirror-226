import base64
import json
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import os
def main():
    banner = """
                            .-')    .-') _    ('-. .-.) (`-.               _  .-')   
                        ( OO ). (  OO) )  ( OO )  / ( OO ).            ( \( -O )  
        ,--. ,--. ,--.   (_)---\_)/     '._ ,--. ,--.(_/.  \_)-.  .----.  ,------.  
    .-')| ,| |  | |  |   /    _ | |'--...__)|  | |  | \  `.'  /  /  ..  \ |   /`. ' 
    ( OO |(_| |  | | .-') \  :` `. '--.  .--'|   .|  |  \     /\ .  /  \  .|  /  | | 
    | `-'|  | |  |_|( OO ) '..`''.)   |  |   |       |   \   \ | |  |  '  ||  |_.' | 
    ,--. |  | |  | | `-' /.-._)   \   |  |   |  .-.  |  .'    \_)'  \  /  '|  .  '.' 
    |  '-'  /('  '-'(_.-' \       /   |  |   |  | |  | /  .'.  \  \  `'  / |  |\  \  
    `-----'   `-----'     `-----'    `--'   `--' `--''--'   '--'  `---''  `--' '--' 
    """

    print(banner)

    rq = requests.Session()
    rq.proxies = dict()
    page = 0
    results = []

    while True:
        page += 1
        print(f'Dumping page {page}')
        raw_query = b'{"uikw":"{*}","orderby":"NAME","kw":"{*}","firstname":"{*}","page":"' + str(page).encode() + b'"}'
        query = quote(base64.b64encode(raw_query).decode())  # Decode the base64-encoded query
        url = f"https://personensuche.dastelefonbuch.de/WntSuche?s={query}"
        rsp = rq.get(url, allow_redirects=False).text
        soup = BeautifulSoup(rsp, features='lxml')
        div_elements = soup.find_all('div', class_='entry hitlistitem')
        
        if len(div_elements) == 0:
            break
        
        for div in div_elements:
            entry = {}
            
            # Extract name
            name_element = div.find('h3').find_all('span', itemprop='givenName')
            if name_element:
                entry['givenName'] = name_element[0].text.strip()

            family_name_element = div.find('h3').find_all('span', itemprop='familyName')
            if family_name_element:
                entry['familyName'] = family_name_element[0].text.strip()
            
            # Extract address
            address_element = div.find('span', class_='address', itemprop='address')
            if address_element:
                address_parts = address_element.find_all('span')
                if len(address_parts) >= 2:
                    entry['postalCode'] = address_parts[0].text.strip()
                    entry['addressLocality'] = address_parts[1].text.strip()
            
            # Extract job title
            job_title_element = div.find('span', class_='title', itemprop='jobTitle')
            if job_title_element:
                entry['jobTitle'] = job_title_element.text.strip()
            
            # Extract picture URL
            picture_element = div.find('div', class_='foto').find('img')
            if picture_element:
                entry['pictureUrl'] = picture_element['src']
            
            # Extract Lebenslauf
            lebenslauf_element = div.find('dl', class_='resume')
            if lebenslauf_element:
                lebenslauf_items = lebenslauf_element.find_all('dt')
                lebenslauf = []
                for dt in lebenslauf_items:
                    dd = dt.find_next('dd')
                    if dd:
                        lebenslauf.append(dd.text.strip())
                entry['lebenslauf'] = lebenslauf
            
            # Extract link to original account
            link_element = div.find('a', class_='profile')
            if link_element:
                entry['accountLink'] = link_element['href']
            
            results.append(entry)
        
        # Save results to a JSON file after processing each page
        with open("telefonbuch.jsonl", "a") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

        # Clear the results list after saving to release memory
        results.clear()

    print("Data dumped and saved to telefonbuch.jsonl file.")
    os.system("sort -u telefonbuch.jsonl > /tmp/telefonbuch.jsonl")
    os.system("mv /tmp/telefonbuch.jsonl .")

if __name__ == "__main__":
    main()