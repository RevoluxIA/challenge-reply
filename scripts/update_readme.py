# scripts/update_readme.py
import os

# Pega a variável de ambiente GITHUB_REPOSITORY fornecida pela Action
repo_full_name = os.environ.get("GITHUB_REPOSITORY")
if not repo_full_name:
    raise ValueError("A variável de ambiente GITHUB_REPOSITORY não foi definida.")

# Divide para obter o nome do repositório e monta o link
repo_name_only = repo_full_name.split('/')[-1]
repo_link = f"https://github.com/{repo_full_name}"

# Lê o template
with open('README.template.md', 'r') as f:
    readme_content = f.read()

# Substitui os placeholders
readme_content = readme_content.replace('%{REPO_NAME}%', repo_name_only)
readme_content = readme_content.replace('%{REPO_LINK}%', repo_link)

# Escreve o novo README.md
with open('README.md', 'w') as f:
    f.write(readme_content)

print(f"README atualizado com sucesso para o repositório: {repo_name_only}")