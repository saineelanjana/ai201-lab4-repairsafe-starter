from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL, VALID_TIERS

_client = Groq(api_key=GROQ_API_KEY)


def classify_safety_tier(question: str) -> dict:
    """
    Classify a home repair question into one of three safety tiers.

    TODO — Milestone 1:

    Before writing any code, complete specs/classifier-spec.md. The blank fields
    there are the decisions that drive this implementation — prompt design, tier
    definitions, output format, and edge case handling.

    Your implementation should:
      1. Build a prompt using your tier definitions that asks the LLM to classify
         the question and explain its reasoning
      2. Send a single chat completion request (no tools, no history)
      3. Parse the tier and reason out of the raw response text
      4. Validate the tier against VALID_TIERS; fall back to "caution" if the
         response can't be parsed or the tier isn't recognized
      5. Return {"tier": ..., "reason": ...}

    Returns a dict with:
      - "tier"   : str — one of "safe", "caution", "refuse"
      - "reason" : str — a brief explanation of why this tier was assigned

    The three tiers:
      - "safe"    : routine, low-risk repairs most homeowners can handle safely
      - "caution" : doable with care, but mistakes have real cost or mild risk
      - "refuse"  : high-risk repairs that require a licensed professional —
                    mistakes can cause fire, flooding, injury, or structural damage
    """
    system_message = (
        'You are a home repair safety assistant. Your task is to classify user questions '
        'about home repair into one of three safety tiers: "safe", "caution", or "refuse". '
        'Use the following definitions for each tier:\n'
        '- "safe": A question is classified as "safe" if it involves low-risk home repair tasks '
        'that can be performed by a typical homeowner without specialized training, tools, or safety equipment.\n'
        '- "caution": Classify a user question as "caution" if it involves home repair tasks that carry '
        'moderate risk, require some specialized knowledge, tools, or safety precautions, and may benefit '
        'from professional guidance.\n'
        '- "refuse": Classify a user question as "refuse" if it involves high-risk home repair tasks that '
        'require professional expertise, specialized tools, or pose significant safety hazards, and should '
        'not be attempted by an untrained individual.\n\n'
        'When in doubt between "safe" and "caution", classify as "caution". '
        'When in doubt between "caution" and "refuse", classify as "refuse".\n\n'
        'Respond in this exact format:\n'
        'Tier: <safe|caution|refuse>\n'
        'Tools: <tools needed>\n'
        'Skills Involved: <skills required>\n'
        'Hazards: <potential hazards>\n'
        'Reason: <one sentence explaining why this tier was assigned>'
    )

    user_message = (
        'Classify the following home repair question.\n\n'
        'Examples:\n\n'
        'Question: How do I patch a small hole in drywall?\n'
        'Tier: safe\n'
        'Tools: Spackle, putty knife, sandpaper\n'
        'Skills Involved: Basic patching technique\n'
        'Hazards: Minor dust\n'
        'Reason: Patching small drywall holes is a low-risk task any homeowner can handle with basic tools.\n\n'
        'Question: Can I install a ceiling fan myself?\n'
        'Tier: caution\n'
        'Tools: Screwdrivers, wire stripper, voltage tester\n'
        'Skills Involved: Basic electrical wiring, ladder safety\n'
        'Hazards: Risk of shock if wiring is done incorrectly, fall risk from ladder\n'
        'Reason: Installing a ceiling fan involves electricity and heights, which require care but can be done safely with proper precautions.\n\n'
        'Question: Can I replace my own circuit breaker?\n'
        'Tier: refuse\n'
        'Tools: Specialized electrical tools\n'
        'Skills Involved: Licensed electrician knowledge\n'
        'Hazards: High-voltage electricity, electrocution, fire hazard\n'
        'Reason: Replacing a circuit breaker involves high-voltage electricity and poses hazards that require a licensed professional.\n\n'
        f'Now classify this question:\n'
        f'Question: {question}'
    )

    try:
        response = _client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
        )
        text = response.choices[0].message.content.strip()

        tier = None
        reason = None

        for line in text.splitlines():
            lower = line.lower()
            if lower.startswith("tier:"):
                tier = line.split(":", 1)[1].strip().lower()
            elif lower.startswith("reason:"):
                reason = line.split(":", 1)[1].strip()

        if tier not in VALID_TIERS:
            tier = "caution"
            reason = reason or "Could not determine tier; defaulting to caution for safety."

        reason = reason or "No reason provided."

        return {"tier": tier, "reason": reason}

    except Exception:
        return {"tier": "caution", "reason": "Classification failed; defaulting to caution for safety."}
