Descrição do Aplicativo: Advocacia App
O Advocacia App é um gerenciador simples e prático de processos judiciais, desenvolvido para advogados que precisam organizar seus casos de forma eficiente no dia a dia.
🎯 Objetivo principal
Facilitar a organização, o controle e o acesso rápido aos arquivos de cada processo judicial, substituindo o uso desorganizado de pastas no Windows.

✅ Principais Funcionalidades

Criação de Novo Processo
Cria uma pasta completa para cada processo com o nome do cliente e número do processo.
Gera automaticamente 7 subpastas organizadas:
Documentos
Petições
Prazos
Andamentos
Provas
Contratos
Notas

Cria automaticamente dois arquivos:
RESUMO.txt (com número do processo, cliente e data de criação)
PRAZOS.txt (para controle de prazos)


Ações Rápidas
Listar Todos os Processos: Abre a pasta principal onde todos os processos ficam salvos (~/Advocacia).
Buscar Processo: Permite buscar por qualquer termo (número do processo, nome do cliente, etc.) e abre a pasta correspondente.
Abrir Pasta do Processo: Busca e abre diretamente a pasta de um processo específico.
Fazer Backup Completo: Cria um arquivo .zip com todos os processos e pastas (com data e hora no nome).

Corretor Ortográfico
Janela dedicada com corretor ortográfico em Português do Brasil.
Marca palavras com erro em vermelho enquanto você digita.
Possui botão para corrigir automaticamente todo o texto.

Interface com Scroll
A tela principal possui barra de rolagem (scroll), permitindo que o conteúdo seja visto mesmo em telas menores ou quando mais funcionalidades forem adicionadas.

Alternância de Tema
Tema Claro (padrão ao abrir)
Tema Escuro (preto com letras brancas)
Pode alternar clicando no botão 🌙 Alternar Tema ou na engrenagem ⚙️ no canto superior direito.



📁 Estrutura de Pastas Criada
Ao criar um processo, o app gera esta estrutura:
textAdvocacia/
└── Nome_do_Cliente/
    └── Numero_do_Processo/
        ├── Documentos/
        ├── Peticoes/
        ├── Prazos/
        ├── Andamentos/
        ├── Provas/
        ├── Contratos/
        ├── Notas/
        ├── RESUMO.txt
        └── PRAZOS.txt

🎨 Características da Interface

Interface gráfica simples e intuitiva feita com Tkinter
Suporte a rolagem com a roda do mouse
Botão de configuração (engrenagem) no canto superior
Menu superior com opções
Design responsivo (pode redimensionar a janela)
