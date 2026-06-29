# MailFlow

Automação em Python para organizar e-mails recebidos em pastas com base no remetente, domínio ou regras de normalização de nomes. O projeto conecta em uma caixa de entrada via IMAP, analisa as mensagens e move cada e-mail para a pasta mais adequada, reduzindo trabalho manual e deixando a caixa de entrada mais limpa.

## Visão Geral

O MailFlow foi criado para automatizar a triagem de e-mails e manter a organização da caixa de entrada de forma simples. Ele lê as mensagens recebidas, identifica o remetente, normaliza nomes quando necessário e cria pastas automaticamente caso elas ainda não existam.

O fluxo atual do projeto é direto:

1. Conecta no servidor IMAP configurado no ambiente.
2. Lista as pastas existentes na conta.
3. Percorre os e-mails recebidos.
4. Extrai o domínio ou identificador do remetente.
5. Aplica um mapeamento de nomes para categorias conhecidas.
6. Cria a pasta, se necessário.
7. Move a mensagem para a pasta correta.

## Principais Funcionalidades

- Conexão com caixa de entrada via IMAP.
- Leitura de mensagens mais recentes ou da caixa completa, conforme a configuração do script.
- Detecção automática do remetente com apoio de `tldextract`.
- Mapeamento de remetentes para pastas padronizadas.
- Criação automática de pastas inexistentes.
- Movimentação dos e-mails para a pasta correspondente.
- Uso de arquivo `.env` para guardar credenciais e dados de conexão.

## Como Funciona

O comportamento do projeto está centralizado em um script principal. Ele usa variáveis de ambiente para carregar credenciais e parâmetros de conexão, acessa o servidor IMAP com `imap-tools` e processa os e-mails um a um.

Há um dicionário de normalização que converte variações de nomes de remetentes em categorias mais consistentes. Isso permite agrupar mensagens de uma mesma origem, mesmo quando o nome exibido muda levemente entre campanhas, domínios ou provedores.

## Requisitos

- Python 3.14 ou superior.
- Conta de e-mail com acesso IMAP habilitado.
- Credenciais válidas para autenticação na caixa de entrada.
- Ambiente virtual recomendado.

## Tecnologias Utilizadas

- Python
- `imap-tools`
- `python-dotenv`
- `tldextract`
- `boto3`

## Instalação

Clone o repositório e entre na pasta do projeto:

```bash
git clone <URL_DO_REPOSITORIO>
cd mailflow
```

Crie e ative um ambiente virtual, se desejar:

```bash
python -m venv .venv
source .venv/bin/activate
```

Instale as dependências usando o gerenciador que preferir:

```bash
uv sync
```

ou, com `pip`:

```bash
pip install boto3 imap-tools python-dotenv tldextract
```

## Configuração

Crie um arquivo `.env` na raiz do projeto com as variáveis necessárias:

```env
EMAIL_IMAP_SERVER=imap.seuprovedor.com
PORT_IMAP_SERVER=993
EMAIL_USER=seu-email@dominio.com
EMAIL_PASS=sua-senha-ou-token
SECURITY_IMAP=SSL

EMAIL_SMTP_SERVER=smtp.seuprovedor.com
EMAIL_SMTP_PORT=587
SECURITY_SMTP=STARTTLS
```

Observações:

- O script atual depende principalmente das configurações IMAP.
- Se o seu provedor exigir senha de aplicativo ou token, use esse método em vez da senha principal.
- Verifique se o acesso IMAP está habilitado na conta de e-mail.

## Uso

Depois de configurar o ambiente e o arquivo `.env`, execute o script principal:

```bash
python main.py
```

Durante a execução, o projeto vai:

- conectar na caixa de entrada;
- listar as pastas existentes;
- processar cada e-mail encontrado;
- criar a pasta necessária, se ela não existir;
- mover a mensagem para a categoria correspondente.

## Estrutura do Projeto

```text
.
├── main.py
├── get_folders.py
├── pyproject.toml
├── README.md
├── data/
│   ├── emails.csv
│   └── folders.txt
└── Untitled-1.json
```

### Arquivos Principais

- [main.py](main.py): script principal de organização e movimentação dos e-mails.
- [get_folders.py](get_folders.py): utilitário para listar as pastas existentes na conta.
- [pyproject.toml](pyproject.toml): definição do projeto e dependências.
- [data/emails.csv](data/emails.csv): arquivo de dados auxiliar, caso você queira usar ou expandir o projeto.
- [data/folders.txt](data/folders.txt): referência de pastas, útil para ajustes manuais ou futuras automações.

## Personalização

O projeto já inclui um dicionário de normalização de remetentes para pastas. Você pode adaptar esse mapeamento para refletir sua própria rotina, adicionando novas chaves e categorias conforme necessário.

Possíveis evoluções:

- criar regras por assunto, palavra-chave ou domínio;
- adicionar modo de simulação antes de mover mensagens;
- registrar logs em arquivo;
- transformar o script em uma CLI com comandos separados;
- adicionar suporte a múltiplas contas.

## Capturas de Tela e Mídia

Se quiser documentar visualmente o projeto, estes espaços podem ser usados no README:

### Screenshot da execução

[INSERIR IMAGEM AQUI]

### Demonstração em vídeo

[INSERIR VÍDEO AQUI]

### Exemplo de antes e depois da caixa de entrada

[INSERIR IMAGEM AQUI]

## Roadmap

- [ ] Modo dry-run para testar regras sem mover mensagens.
- [ ] Painel simples com resumo das regras aplicadas.
- [ ] Suporte a regras configuráveis por arquivo externo.
- [ ] Log estruturado para auditoria das movimentações.

## Contribuição

Contribuições são bem-vindas. Um fluxo simples de colaboração pode seguir este padrão:

1. Faça um fork do repositório.
2. Crie uma branch para sua alteração.
3. Implemente e teste a mudança.
4. Envie um pull request com uma descrição objetiva.

## Segurança

Como o projeto lida com credenciais de acesso a e-mail, mantenha o arquivo `.env` fora do controle de versão e revise com cuidado as permissões da conta usada.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo [LICENSE](/home/alvarocoelhojesus/Documents/projects/mailflow/LICENSE) para o texto completo.

## Agradecimentos

Se este projeto te ajudou a organizar melhor sua caixa de entrada, sinta-se à vontade para adaptá-lo ao seu fluxo e expandi-lo com novas automações.
