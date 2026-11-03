# Avaliação manual do modelo

## Resultado geral

Foram revisadas manualmente as oito avaliações processadas pelo Gemini. Sete classificações de sentimento foram consideradas aceitáveis; a avaliação 4 teve um erro claro de sarcasmo. A avaliação 8 é mista e foi marcada como neutra porque o projeto ainda não tem uma categoria "misto".

| ID | Sentimento esperado | Resultado | Observação |
|---:|---|---|---|
| 1 | Negativo | Acerto | Identificou atraso e comida fria. |
| 2 | Negativo | Aceitável | O hambúrguer foi elogiado, mas a embalagem rasgada e o molho vazado são a reclamação principal. |
| 3 | Positivo | Acerto | Identificou o elogio ao entregador e a entrega antes do prazo. A ação sugerida teve o erro de escrita "Elogar". |
| 4 | Negativo | Erro | Interpretou literalmente o sarcasmo sobre uma entrega que demorou duas horas e marcou como positivo. |
| 5 | Negativo | Acerto | Identificou a reclamação de custo-benefício e porção pequena. |
| 6 | Positivo | Acerto | "Ótimo" expressa satisfação, mas é curto e não permite identificar um tema específico. |
| 7 | Negativo | Acerto | Identificou o erro de pedido e a restrição ignorada. |
| 8 | Misto / neutro | Aceitável | Atendimento ruim e comida boa; "neutro" representa o equilíbrio, mas o projeto não oferece uma categoria "misto". |

## Erros e limitações observados

- Sarcasmo na avaliação 4 foi interpretado como elogio literal.
- A ação da avaliação 3 contém o erro de escrita "Elogar".
- Avaliações mistas não têm uma categoria própria; a avaliação 8 foi classificada como neutra.
- Textos muito curtos, como "ótimo", permitem detectar sentimento, mas não um tema específico.
