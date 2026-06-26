from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_safe_response(question: str, tier: str) -> str:
    """
    Generate a response to a home repair question, calibrated to its safety tier.

    TODO — Milestone 2:

    Before writing any code, complete specs/responder-spec.md. The most important
    fields are the three system prompts — one per tier. Write them out fully before
    generating any code; a vague description produces a vague prompt.

    `tier` is one of "safe", "caution", or "refuse" — returned by classify_safety_tier().

    Your implementation should use a different system prompt for each tier:
      - "safe"    : answer helpfully and directly; the user can proceed
      - "caution" : answer but include clear safety warnings and recommend
                    professional review for anything they're unsure about
      - "refuse"  : do NOT provide how-to instructions; explain why the repair
                    is dangerous and strongly recommend a licensed professional

    The refuse case is the hardest to get right. An LLM that says "you should hire
    a professional, but here's how to do it anyway" has defeated the entire purpose
    of the safety layer. Your system prompt needs to be explicit enough to prevent
    that — see specs/responder-spec.md for the design decision field on grounding.

    If tier is unrecognized (e.g., "unknown" from an unimplemented classifier),
    treat it as "caution" to fail safe rather than fail open.

    Return the response as a plain string.
    """
    system_prompts = {
        "safe": (
            "You are a helpful home repair assistant. The user's question has been reviewed and "
            "is safe for a typical homeowner to attempt. Provide a clear, step-by-step answer that "
            "is easy to follow. Include any necessary safety precautions, but assume the user has "
            "basic home repair skills and tools. Be concise and avoid unnecessary technical jargon."
        ),
        "caution": (
            "You are a home repair safety assistant. The user's question involves a task that carries "
            "moderate risk and requires care. Provide a helpful answer, but lead with a clear safety "
            "warning before any instructions. Throughout your response, highlight the specific risks "
            "involved and make a clear, explicit recommendation that the user consult or hire a licensed "
            "professional if they are unsure or inexperienced. Do not provide detailed step-by-step "
            "instructions that could lead to harm if followed without proper expertise."
        ),
        "refuse": (
            "You are a home repair safety assistant. The user's question involves a high-risk task that "
            "must only be performed by a licensed professional. "
            "YOUR ONLY JOB IS TO DECLINE AND REDIRECT — DO NOT provide any steps, procedures, methods, "
            "techniques, or instructions of any kind — not even general guidance, partial steps, or "
            "'things to keep in mind.' Do not explain how the task works at a technical level, as that "
            "information could be used as implicit instructions. "
            "Instead: (1) clearly state that you cannot provide guidance on this task, "
            "(2) explain in plain terms why it is dangerous and what can go wrong, and "
            "(3) advise the user to hire a licensed professional and suggest how to find one "
            "(e.g., checking state licensing boards, asking for referrals, verifying credentials). "
            "If you catch yourself about to describe a procedure or step — stop and redirect instead."
        ),
    }

    system_message = system_prompts.get(tier, system_prompts["caution"])

    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content.strip()
