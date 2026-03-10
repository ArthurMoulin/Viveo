import os
import shutil
from pathlib import Path

# Definindo o caminho da pasta no seu Desktop
# Usamos o 'r' antes das aspas para o Windows não confundir as barras \
caminho_pasta = r'C:\Users\Arthur.Moulin\Desktop\Teste\Teste_1'

# Convertemos para um objeto Path para facilitar a manipulação
diretorio = Path(caminho_pasta)

if not diretorio.exists():
    print(f"Erro: A pasta {caminho_pasta} não foi encontrada.")
else:
    arquivos = [f for f in diretorio.iterdir() if f.is_file()]
    print(f"Encontrados {len(arquivos)} arquivos para organizar.")

    for arquivo in arquivos:
        # Pega os primeiros 4 caracteres do nome do arquivo
        ano = arquivo.name[:4]

        # Verifica se o início do nome é realmente um ano (4 dígitos)
        if ano.isdigit() and len(ano) == 4:
            pasta_ano = diretorio / ano
            
            # Cria a subpasta do ano (2021, 2022, etc) se não existir
            pasta_ano.mkdir(exist_ok=True)
            
            # Move o arquivo para dentro da subpasta
            try:
                shutil.move(str(arquivo), str(pasta_ano / arquivo.name))
            except Exception as e:
                print(f"Erro ao mover {arquivo.name}: {e}")

    print("Organização por ano concluída!")