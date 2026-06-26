# Spec: `generate_safe_response()`

**File:** `responder.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Generate a response to a home repair question that is appropriate to its safety tier. The same question gets a fundamentally different answer depending on the tier — not just a disclaimer tacked on, but a different behavior: answer fully, answer with warnings, or decline to give instructions entirely.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `question` | `str` | The user's home repair question |
| `tier` | `str` | The safety tier: `"safe"`, `"caution"`, or `"refuse"` |

**Output:** `str` — the response to show to the user

---

## Design Decisions

*Complete the fields below before writing any code. The most important fields are the three system prompts. Write them out fully — don't just describe what you want.*

---

### System prompt: "safe" tier

*Write the exact system prompt text for a safe question. It should produce helpful, specific, actionable answers.*

```
For a safe user question, provide a clear, step-by-step answer that is easy to follow. Include any necessary safety precautions, but assume the user has basic home repair skills and tools. Be concise and avoid unnecessary technical jargon.
```

---

### System prompt: "caution" tier

*Write the exact system prompt text for a caution question. What safety language should be present? How firm should the "consider a professional" message be — a gentle mention or a clear recommendation?*

```
For a caution user question, provide a helpful answer that includes clear safety warnings and precautions. Emphasize the potential risks involved and suggest upfront that the user consider consulting a licensed professional if they are unsure or inexperienced. Avoid giving detailed step-by-step instructions that could lead to harm.
```

---

### System prompt: "refuse" tier

*This is the most important one to get right. Write the exact system prompt for refusing to answer.*

*Two goals that are in tension: (1) the response must NOT provide how-to instructions, even a little. (2) the response should still be genuinely useful — explaining why the task is dangerous and what the user should do instead.*

*Before writing this prompt, use Plan mode with your AI tool. Share your draft refuse prompt and ask it: "What are ways an LLM might still provide dangerous instructions despite this system prompt?" Revise until you've addressed the failure modes it identifies.*

```
For a refuse user question, do not provide any step-by-step instructions, procedures, or guidance on how to perform the task. Instead, clearly explain why the task is dangerous and emphasize that it requires professional expertise. Advise the user to hire a licensed professional and provide information on how to find one. Avoid giving any general advice that could be interpreted as instructions.
```

---

### Grounding the refuse response

*The grounding problem from Lab 1 applies here, with higher stakes: even with a strong system prompt, an LLM may "helpfully" provide partial instructions before pivoting to "you should hire a professional." How will you prevent that?*

*Hint: "be careful" doesn't work. Explicit, behavioral instructions ("do not provide any steps, procedures, or instructions — not even general guidance") work better. What will yours say?*

```
Do not provide any steps, procedures, or instructions — not even general guidance. Emphasize that the task is dangerous and requires professional expertise. Advise the user to hire a licensed professional and provide information on how to find one. Avoid any language that could be interpreted as instructions or guidance.
```

---

### Fallback for unknown tier

*What should your function do if it receives a tier value that isn't "safe", "caution", or "refuse" — e.g., "unknown" while the classifier is still a stub? Write the fallback behavior and explain why.*

```
For an unknown tier, default to caution behavior. Provide a response that includes safety warnings and suggests consulting a licensed professional. This ensures that the user is not given potentially unsafe instructions while still receiving some guidance on how to proceed safely.
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 3.*

**A "refuse" response that was still too helpful and what you changed to fix it:**

```
NA
```

**The tier where the LLM's default behavior was closest to what you wanted (and which tier required the most prompt iteration):**

```
iT DID WHAT WE MENTIONED IN THE SPEC
```
