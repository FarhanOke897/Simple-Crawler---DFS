import requests
from bs4 import BeautifulSoup
import mysql.connector
from urllib.parse import urljoin

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="farhan"
)
cursor = db.cursor()

visited = set()

def dfs(url):
    if url in visited:
        print(f" Sudah dikunjungi: {url}")
        return
    print(f" Mengunjungi: {url}")
    visited.add(url)

    try:
        response = requests.get(url, timeout=5)  
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')

        title = str(soup.title.string.strip()) if soup.title else "No Title"

        paragraph = soup.find('p')
        content = str(paragraph.text.strip()) if paragraph else "No Content"

        try:
            cursor.execute(
                "INSERT INTO pages (url, title, content) VALUES (%s, %s, %s)", 
                (url, title, content)
            )
            db.commit()
            print(f" Data berhasil disimpan: {url} | {title} | {content[:50]}...")
        except mysql.connector.Error as err:
            print(f" Error menyimpan ke database: {err}")

        
        for link in soup.find_all('a', href=True):
            next_url = urljoin(url, link['href'])  
            if next_url not in visited:
                print(f"Menemukan link: {next_url}")
                dfs(next_url)

    except requests.exceptions.RequestException as e:
        print(f" Error mengambil {url}: {e}")


print(" Memulai DFS dari index.html...")
dfs("http://localhost/index.html")


cursor.close()
db.close()
print(" Koneksi database ditutup.")
