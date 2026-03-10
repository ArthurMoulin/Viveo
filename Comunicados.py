import pandas as pd
import requests
import zipfile
import io
import os
from playwright.sync_api import sync_playwright
import time

CVM_CODE = 25682
TICKER = "VVEO3"
YEARS = [2021, 2022, 2023, 2024] # 
base_folder = f"Documentos_{TICKER}_Final"
os.makedirs(base_folder, exist_ok=True)

def baixar_documento():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True) # Habilita downloads
        page = context.new_page()

        for year in YEARS:
            url_zip = f"https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/IPE/DADOS/ipe_cia_aberta_{year}.zip"
            r = requests.get(url_zip)
            with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                csv_name = f"ipe_cia_aberta_{year}.csv"
                with z.open(csv_name) as f:
                    df = pd.read_csv(f, sep=';', encoding='ISO-8859-1')
                    vveo_docs = df[df['Codigo_CVM'] == CVM_CODE]

                    for _, row in vveo_docs.iterrows():
                        link = row['Link_Download']
                        protocolo = row['Protocolo_Entrega']
                        assunto = "".join(x for x in str(row['Assunto']) if x.isalnum() or x in "._- ")[:50]
                        filename = f"{row['Data_Referencia']}_{assunto}_{protocolo}.pdf"
                        filepath = os.path.join(base_folder, filename)

                        if os.path.exists(filepath): continue

                        print(f"  [TENTANDO] {filename}")
                        
                        try:
                            # Preparamos o Playwright para esperar um possível download
                            with page.expect_download(timeout=10000) as download_info:
                                try:
                                    # Tentamos navegar
                                    page.goto(link, wait_until="commit", timeout=15000)
                                    # Se não disparou download, ele vai tentar renderizar como PDF
                                    time.sleep(2)
                                    page.pdf(path=filepath, format="A4", print_background=True)
                                    print(f"    [OK] Renderizado como PDF.")
                                except Exception as e:
                                    if "Download is starting" in str(e):
                                        # Se cair aqui, o download_info será preenchido
                                        download = download_info.value
                                        download.save_as(filepath)
                                        print(f"    [OK] PDF original baixado.")
                                    else:
                                        print(f"    [ERRO] {e}")
                        except Exception as e:
                            print(f"    [AVISO] Timeout ou erro no link: {protocolo}")

        browser.close()

if __name__ == "__main__":
    baixar_documento()