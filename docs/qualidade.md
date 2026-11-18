# Qualidade · Verificador de soluções

## 10/11/2026, 17:01 · 63 problemas

A primeira análise deu 63 problemas, todos de gravidade média, sem críticos nem altos.

Eram todos de acessibilidade. A regra `app-include-accessible-label` deu 51, a `app-include-tab-index` deu 9 e a `app-include-readable-screen-name` deu 3.

A M1 gerada tinha 20, a Copilot 16, a Contoso Coffee Machines 13, a M6 8, a M3 4, e a biblioteca e o modelo Split-screen 1 cada.

Não havia avisos de fórmulas, de delegação nem de desempenho.

## 12/11/2026, 08:24 · 97 problemas

Com as duas apps da segunda passagem, a contagem subiu para 97 problemas médios, outra vez todos de acessibilidade, espalhados pelas 9 apps.

## 12/11/2026, 08:30 a 09:05 · correção

As correções foram feitas no Verificador de aplicações do Studio, app a app. Cada app só foi guardada e publicada depois de o verificador mostrar "Não foram encontrados erros".

Os botões e ícones ganharam etiquetas em português, como "Voltar", "Guardar registo", "Editar registo", "Eliminar registo", "Criar novo registo" e "Procurar máquinas".

Nos campos dos formulários, a etiqueta é `Parent.DisplayName`, para acompanhar o nome do cartão sem ser escrita à mão.

As galerias e os ícones clicáveis ficaram com `TabIndex = 0`. Isto obriga a dar etiqueta a cada ícone, e por isso o verificador mostrava erros novos depois de cada ronda.

Três ecrãs foram renomeados. O `Screen1` da M3 passou a "Welcome Screen", o do modelo a "Split Screen" e o da biblioteca a "Component Test Screen".

## 12/11/2026, 09:04 · 0 problemas

O Verificador de soluções deu 0 problemas em todas as gravidades.

A exportação 1.0.0.1 é das 08:25, antes destas correções. A primeira exportação limpa será a 1.0.0.2.

## Verificação no repositório

Depois da sincronização, `python -m tools.learn validar` confirma o YAML, o schema oficial e a sintaxe das fórmulas em todas as apps. O CI corre-o em cada push.
