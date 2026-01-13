# Cognitive Orchestrator 🧠

Este projeto é uma implementação técnica de um blueprint para Inteligência Aumentada. Diferente de scripts simples de chat, esta arquitetura prioriza a **verificação cruzada (cross-verification)** e o **Human-in-the-Loop**.

## Os 4 Pilares da Arquitetura
1.  **Stack Híbrida**: Utiliza múltiplos provedores (OpenAI, Google, Open-Source) para evitar viés de modelo único.
2.  **Fluxo de Refinaria**: Pesquisa (Gemini) -> Crítica (DeepSeek/Llama) -> Polimento (GPT-4).
3.  **Segurança Cognitiva**: O sistema exige interação humana em pontos críticos para evitar "piloto automático".
4.  **Guardrails**: Verificações básicas de alucinação e consistência.
