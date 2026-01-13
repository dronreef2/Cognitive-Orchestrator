# Cognitive Orchestrator 🧠

Este projeto é uma implementação técnica de um blueprint para Inteligência Aumentada. Diferente de scripts simples de chat, esta arquitetura prioriza a **verificação cruzada (cross-verification)** e o **Human-in-the-Loop**.

## Os 4 Pilares da Arquitetura
1.  **Stack Híbrida**: Utiliza múltiplos provedores (OpenAI, Google, Open-Source) para evitar viés de modelo único.
2.  **Fluxo de Refinaria**: Pesquisa (Gemini) -> Crítica (DeepSeek/Llama) -> Polimento (GPT-4).
3.  **Segurança Cognitiva**: O sistema exige interação humana em pontos críticos para evitar "piloto automático".
4.  **Guardrails**: Verificações básicas de alucinação e consistência.

## Por que “Inteligência Aumentada”?
O objetivo não é substituir o humano, mas **potencializar** a tomada de decisão. O humano continua como autoridade final, enquanto os agentes automatizados aceleram pesquisa, checagem lógica e polimento de linguagem.

## Como evitamos atrofia cognitiva
- **Human-in-the-Loop obrigatório**: a função `guardrails.verify()` bloqueia o fluxo até que o usuário aprove manualmente a saída crítica.
- **Stack híbrida**: múltiplos modelos (Gemini, Ollama, OpenAI) reduzem dependência de um único viés.
- **Etapa de crítica dedicada**: força reflexão sobre lacunas e riscos antes de qualquer ação ou publicação.

## Execução rápida
1. Configure as credenciais esperadas pelo [LiteLLM](https://docs.litellm.ai/docs/providers). Exemplos:
   - `OPENAI_API_KEY` para modelos OpenAI.
   - `GEMINI_API_KEY` para modelos Gemini.
   - `OLLAMA_BASE_URL` se estiver rodando um servidor Ollama local.
2. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Rode o orquestrador:
   ```bash
   python main.py
   ```
4. Fluxo:
   - **Researcher (Gemini)** coleta contexto.
   - **Critic (Ollama/Llama)** testa lógica e aponta riscos.
   - **Guardrails** pedem aprovação humana antes de seguir.
   - **Editor (OpenAI)** entrega um resumo polido.
