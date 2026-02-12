# Onebeam Agent Runtime  
**A Production-Grade Multi-Model AI Orchestration System**

---

## Overview

Onebeam Agent Runtime is a provider-agnostic orchestration layer that unifies multiple frontier models under a single deterministic architecture.

The runtime supports:

- GPT-5.2 (via OpenAI)
- Claude Opus 4.6 (via Anthropic)
- Gemini 3 (via Google)

The goal is to abstract away provider-specific differences while enforcing consistent safety, tool execution control, and predictable runtime behavior.

This system demonstrates how heterogeneous LLM providers can be unified behind a secure and extensible architecture.

---

# 1. Agent Architecture

## High-Level Request Lifecycle

```
┌──────────────────────┐
│       User Input     │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│  Permission Guard    │  ← Pre-safety enforcement
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│     Model Router     │  ← Capability-based selection
└──────────┬───────────┘
           ↓
┌────────────────────────────────────┐
│        Provider Adapter Layer      │
│ ┌────────┬────────┬──────────────┐ │
│ │   GPT  │ Claude │    Gemini    │ │
│ └────────┴────────┴──────────────┘ │
└──────────┬─────────────────────────┘
           ↓
┌──────────────────────┐
│ Response Normalizer  │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Post-Safety Layer    │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│    Tool Execution    │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│     Final Output     │
└──────────────────────┘

```

---

## Core Components

### Agent Runtime (`core/agent_runtime.py`)

Responsible for:
- Orchestrating request lifecycle
- Managing conversation state
- Invoking providers
- Executing tools
- Applying safety layers
- Logging and traceability

---

### Model Router (`core/model_router.py`)

Selects the appropriate model based on:
- Task type
- Capability requirements
- Cost/latency considerations
- Policy constraints

Routing is policy-driven and extensible.

---

### Permission Guard (`core/permission_guard.py`)

Acts as a centralized policy engine:
- Validates user intent
- Blocks restricted categories
- Prevents unsafe tool invocation
- Enforces deterministic pre-request safety

---

### Provider Layer (`providers/`)

Implements a strict adapter pattern:

```
BaseProvider
 ├── OpenAIProvider
 ├── ClaudeProvider
 └── GeminiProvider
```

Each provider implements a unified `generate()` interface, ensuring the core runtime never directly depends on vendor SDK structure.

---

# 2. Model Adapter Design

The runtime uses a provider abstraction layer to normalize differences across model APIs.

All providers conform to:

```python
class BaseProvider:
    def generate(self, messages, tools=None, safety_level=None):
        pass
```

This ensures:

- Vendor independence
- Clean separation of concerns
- Easy extensibility
- Stable core logic despite SDK changes

---

## Message Unification

Internally, all models operate on a unified schema:

```
{
  "role": "system" | "user" | "assistant",
  "content": "...",
  "tool_calls": [...]
}
```

Each adapter translates between:
- Internal unified format
- Provider-specific request structure

---

## Tool Schema Normalization

Different models implement tool/function calling differently.

The runtime:

- Converts tool schemas into provider-compatible formats
- Normalizes tool-call responses
- Enforces strict tool registry validation
- Prevents arbitrary function execution

---

## Response Standardization

Provider differences are abstracted, including:

- Stop sequences
- Streaming behavior
- Refusal formats
- Error handling
- Tool invocation encoding

All responses are normalized before reaching the agent core.

---

# 3. How GPT-5.2, Claude Opus 4.6, and Gemini 3 Are Unified

The unification strategy is built on three layers:

### 1. Unified Runtime Contract
All providers implement the same `generate()` interface.

### 2. Schema Translation Layer
Adapters convert:
- Internal message format → Provider format
- Provider response → Normalized runtime format

### 3. Centralized Orchestration
Routing, safety, and tool execution are handled by the runtime — not by providers.

This ensures:

- Deterministic behavior across models
- Swappable providers
- Isolation of provider-specific behavior

---

# 4. Safety Architecture

Safety is enforced at the runtime level — not delegated solely to providers.

---

## Layer 1: Pre-Request Safety

Before any provider call:

- Input is validated
- Restricted intents are blocked
- Tool usage is checked
- Policy rules are enforced

Unsafe requests never reach a model.

---

## Layer 2: Provider Isolation

Each provider runs behind a strict adapter boundary.

If a provider:
- Returns malformed output
- Violates expected structure
- Behaves unexpectedly

The runtime intercepts and blocks propagation.

---

## Layer 3: Post-Response Safety

Every model output is validated before delivery:

- Schema validation
- Policy compliance checks
- Tool call validation
- Refusal detection
- Logging of safety violations

No response is returned without passing post-validation.

---

# How Onebeam stays safe across GPT-5.2, Claude Opus 4.6, and Gemini 3

Onebeam enforces a **model-agnostic safety contract** independent of provider guarantees.

### 1. Centralized Policy Enforcement
Safety logic lives inside the runtime.  
Providers are not trusted as sole safety authorities.

### 2. Deterministic Tool Control
Models cannot execute arbitrary system functions.  
All tools must be pre-registered via `tool_registry.py`.

### 3. Dual Safety Layers
Both pre-request and post-response validations are mandatory.

### 4. Structured Output Validation
Responses must conform to expected schema before execution.

### 5. Provider Sandbox Isolation
Each model is encapsulated inside an adapter boundary.  
Unexpected model behavior cannot compromise runtime integrity.

### 6. Audit Logging & Traceability
All:
- Routing decisions
- Safety rejections
- Tool invocations
are logged for review and debugging.

Safety enforcement remains consistent regardless of which model is selected.

---

# 5. Project Structure

```
onebeam_agent_runtime/
│
├── core/
│   ├── agent_runtime.py
│   ├── model_router.py
│   ├── permission_guard.py
│   └── logger.py
│
├── providers/
│   ├── base_provider.py
│   ├── openai_provider.py
│   ├── claude_provider.py
│   └── gemini_provider.py
│
├── agents/
├── tools/
├── schemas/
├── ui/
│   ├── app.py
│   └── templates/
│
└── main.py
```

---

# 6. How to Run Locally

This project uses mock providers and standard Python libraries only.
No external dependencies or API keys are required.

## Run the application

From the project root directory:

Using the UI:

```bash
python onebeam_agent_runtime/ui/app.py
```

Open in browser:

```
http://localhost:5000
```

---

# Engineering Principles

- Provider-agnostic core
- Explicit safety over implicit safety
- Deterministic tool execution
- Clear separation of concerns
- Extensible adapter architecture
- Centralized policy enforcement

---

# Conclusion

Onebeam Agent Runtime demonstrates how frontier AI models can be unified safely and deterministically under a single extensible orchestration system while maintaining strict safety guarantees and provider independence.
