# Spec: `classify_safety_tier()`

**File:** `safety.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Determine whether a home repair question is safe to answer directly, requires a cautionary response, or should be refused with a referral to a licensed professional.

---

## Input / Output Contract

**Input:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `question` | `str` | The user's home repair question |

**Output:** `dict`

| Key | Type | Description |
|-----|------|-------------|
| `"tier"` | `str` | One of: `"safe"`, `"caution"`, `"refuse"` |
| `"reason"` | `str` | One sentence explaining why this tier was assigned |

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Tier definitions

*Write a one-sentence definition for each tier that is precise enough to use as part of your classification prompt. Vague definitions produce inconsistent classifications.*

**safe:**
```
A question is classified as "safe" if it involves low-risk home repair tasks that can be performed by a typical homeowner without specialized training, tools, or safety equipment.
```

**caution:**
```
Classify a user question as "caution" if it involves home repair tasks that carry moderate risk, require some specialized knowledge, tools, or safety precautions, and may benefit from professional guidance.
```

**refuse:**
```
Classify a user question as "refuse" if it involves high-risk home repair tasks that require professional expertise, specialized tools, or pose significant safety hazards, and should not be attempted by an untrained individual.
```

---

### Classification approach

*How will the LLM classify the question? Will you give it just the tier definitions, or also examples (few-shot)? Will you ask it to reason step-by-step before naming the tier, or output the tier directly?*

*Consider: what happens when a question is genuinely ambiguous — e.g., "can I replace my own outlets?" Which tier should that land in, and how does your approach handle questions at the boundary?*

```
We would give the LLM the tier definitions along with a few examples of questions for each tier (few-shot learning). We would ask it to reason step-by-step before naming the tier, ensuring that it considers the risk level, required expertise, and potential hazards. For ambiguous questions, we would instruct the LLM to classify them as "caution" to err on the side of safety, while providing a clear reasoning for its decision.
```

---

### Output format

*How will the LLM communicate the tier and reason back to you? Describe the exact text format you'll ask it to use, so you can parse it reliably.*

*The format you used in Lab 3 (`Label: X / Reasoning: Y`) is a reasonable starting point, but you're not required to use it. Whatever you choose, you'll need to parse it in code — so consider how much variation the LLM might introduce and how you'll handle that.*

```
Tier: <tier>
Tools: <tools>
Skills Involved: <skills>
Hazards: <hazards>
Reason: <reason>
```

---

### Prompt structure

*Write the actual prompt you'll use — both the system message and the user message. Don't describe it — write it. Vague prompt descriptions produce vague prompts, which produce inconsistent classifications.*

**System message:**
```
You are a home repair safety assistant. Your task is to classify user questions about home repair into one of three safety tiers: "safe", "caution", or "refuse". Use the following definitions for each tier:
- "safe": A question is classified as "safe" if it involves low-risk home repair tasks that can be performed by a typical homeowner without specialized training, tools, or safety equipment.
- "caution": Classify a user question as "caution" if it involves home repair tasks that carry moderate risk, require some specialized knowledge, tools, or safety precautions, and may benefit from professional guidance.
- "refuse": Classify a user question as "refuse" if it involves high-risk home repair tasks that require professional expertise, specialized tools, or pose significant safety hazards, and should not be attempted by an untrained individual.
```

**User message:**
```
[your prompt here]
```

---

### Caution/refuse boundary

*The most consequential classification decision is whether a question lands in "caution" or "refuse." Write down your rule for this boundary — one sentence. Then give two examples of questions that sit close to the line and explain which side they fall on and why.*

```
If a question has a high risk potential for injury or requires specialized knowledge and tools that a typical homeowner is unlikely to possess, it should be classified as "refuse"; otherwise, if it poses a moderate risk, it should be classified as "caution".

An example of a question that sits close to the line is "Can I replace my own circuit breaker?" This falls on the "refuse" side because it involves working with high-voltage electricity, which poses significant safety hazards and requires professional expertise.

Another example is "Can I install a ceiling fan myself?" This falls on the "caution" side because while it involves some risk (working with electricity and heights), it can be done safely by a homeowner with proper precautions and basic knowledge, making it less hazardous than replacing a circuit breaker.
```

---

### Fallback behavior

*What does your function return if the LLM response can't be parsed — e.g., if it produces free-form prose instead of your expected format? What happens when tier validation against `VALID_TIERS` fails?*

*Note: failing open (returning "safe" as a fallback) is more dangerous than failing closed (returning "caution"). Which makes more sense here, and why?*

```
Fall back too "caution" if the LLM response can't be parsed or if tier validation against `VALID_TIERS` fails. Failing closed makes more sense here because it errs on the side of safety, ensuring that potentially risky questions are treated with caution rather than being classified as safe when they might not be.
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 2.*

**One classification that surprised you — question, tier you expected, tier it returned, and why:**

```
One that surpised us was "How do I reset a GFCI outlet that won't reset?" as it returned "caution" instead of "safe". We expected it to be classified as "safe" because resetting a GFCI outlet is generally a low-risk task. However, the LLM likely considered the potential for electrical hazards and the need for some basic knowledge about electrical systems, leading it to classify the question as "caution".
```

**One prompt change you made after seeing the first few outputs, and what it fixed:**

```
NA
```
