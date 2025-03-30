import os
import shutil

def copy_directory(src, dest):
    """Copia o conteúdo de um diretório src para o diretório dest."""
    
    # Verifica se o diretório de destino existe; se não, cria
    if not os.path.exists(dest):
        os.makedirs(dest)
    
    # Itera sobre todos os arquivos e subdiretórios no diretório de origem
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        
        # Se for um diretório, faz a chamada recursiva
        if os.path.isdir(src_path):
            copy_directory(src_path, dest_path)
        else:
            # Caso contrário, copia o arquivo
            shutil.copy2(src_path, dest_path)
            print(f"Copied {src_path} to {dest_path}")
