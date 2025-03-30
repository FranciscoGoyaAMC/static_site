# Static Site Generator  

Este é um **Gerador de Sites Estáticos** desenvolvido em **Python**, que converte arquivos **Markdown** em páginas **HTML** utilizando um modelo (`template.html`). O projeto mantém a estrutura de diretórios original e gera um site navegável a partir do conteúdo fornecido.  

## 📌 Funcionalidades  

✅ Conversão de arquivos **Markdown** para **HTML**  
✅ Geração automática de **todas as páginas** do site  
✅ Manutenção da **estrutura de diretórios** original  
✅ Suporte a **listas, títulos, parágrafos, negrito, itálico, código e citações**  
✅ Aplicação de um **template HTML** com placeholders (`{{ Title }}` e `{{ Content }}`)  
✅ Cópia de **arquivos estáticos** (CSS, imagens) para o diretório público  
✅ **Testes automatizados** para garantir a funcionalidade do parser  

## 🛠️ Tecnologias Utilizadas  

- **Python 3**  
- **Markdown**  
- **HTML**  
- **CSS**  
- **Shell Script** (para automação de execução e testes)  

## 📂 Estrutura do Projeto  

```
📦 static-site-generator  
 ┣ 📂 content           # Arquivos Markdown que serão convertidos  
 ┃ ┣ 📜 index.md        # Página inicial  
 ┃ ┣ 📂 blog            # Diretório de posts do blog  
 ┃ ┣ 📂 contact         # Diretório de contato  
 ┣ 📂 public            # Diretório onde as páginas HTML geradas são armazenadas  
 ┣ 📂 static            # Arquivos estáticos (CSS, imagens)  
 ┃ ┣ 📜 index.css       # Estilos CSS  
 ┣ 📂 src               # Código-fonte do gerador  
 ┃ ┣ 📜 blocktype.py    # Identificação de tipos de blocos Markdown  
 ┃ ┣ 📜 generator.py    # Geração de páginas HTML  
 ┃ ┣ 📜 htmlnode.py     # Classe base para nós HTML  
 ┃ ┣ 📜 leafnode.py     # Classe para nós HTML sem filhos  
 ┃ ┣ 📜 parentnode.py   # Classe para nós HTML com filhos  
 ┃ ┣ 📜 markdown.py     # Conversão de Markdown para HTML  
 ┃ ┣ 📜 textnode.py     # Representação de texto formatado  
 ┃ ┣ 📜 main.py         # Script principal do projeto  
 ┣ 📂 tests             # Testes unitários  
 ┃ ┣ 📜 test_markdown.py  
 ┃ ┣ 📜 test_htmlnode.py  
 ┣ 📜 .gitignore        # Arquivos ignorados pelo Git  
 ┣ 📜 README.md         # Documentação do projeto  
 ┣ 📜 template.html     # Modelo HTML para as páginas  
 ┣ 📜 main.sh           # Script para rodar o servidor local  
 ┣ 📜 test.sh           # Script para rodar os testes  
```

## 🚀 Como Usar  

### 1️⃣ Clonar o Repositório  

```sh
git clone https://github.com/FranciscoGoyaAMC/static_site.git
cd static-site-generator
```

### 2️⃣ Criar e Ativar um Ambiente Virtual  

```sh
python -m venv venv
source venv/bin/activate  # No Linux/macOS
venv\Scripts\activate      # No Windows
```

### 3️⃣ Instalar Dependências  

```sh
pip install -r requirements.txt
```

### 4️⃣ Gerar o Site  

```sh
python src/main.py
```

Isso converterá todos os arquivos `.md` em `.html` dentro do diretório `public/`.

### 5️⃣ Visualizar o Site  

Para iniciar um servidor local e visualizar o site, execute:  

```sh
./main.sh
```

Então, acesse [http://localhost:8888](http://localhost:8888) no navegador.  

## ✅ Testes  

Para rodar os testes automatizados:  

```sh
./test.sh
```

## 📜 Licença  

Este projeto é de código aberto e está disponível sob a licença MIT.  
