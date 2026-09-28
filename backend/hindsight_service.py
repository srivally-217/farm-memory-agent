from groq import Groq
from hindsight_client import Hindsight
from dotenv import load_dotenv
import os

load_dotenv()


# ==========================================
# HINDSIGHT CLIENT
# ==========================================

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)


# ==========================================
# GROQ CLIENT
# ==========================================

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ==========================================
# HINDSIGHT MEMORY BANK
# ==========================================

BANK_ID = "farm-memory-agent-demo"


# ==========================================
# STORE FARM EVENT
# ==========================================

def store_farm_event(event):

    response = client.retain(
        bank_id=BANK_ID,
        content=event
    )

    return response


# ==========================================
# RECALL FARM MEMORY
# ==========================================

def recall_farm_memory(user_message):

    response = client.recall(
        bank_id=BANK_ID,
        query=user_message
    )

    memories = "\n".join(
        result.text for result in response.results
    )

    return memories


# ==========================================
# GENERATE FARM RESPONSE
# ==========================================

def generate_farm_response(user_message):

    # Recall memories related to the
    # farmer's current message
    memories = recall_farm_memory(user_message)

    response = groq_client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[

            {
                "role": "system",

                "content": """
You are a Farm Memory Agent.

Your key ability is to remember the farmer's previous
experiences and use them to personalize future responses.

STRICT MEMORY RULES:

1. Treat information in the provided memories as historical
facts about this farmer.


2. NEVER invent or modify:

- dates
- quantities
- measurements
- treatments
- causes
- outcomes
- weather events
- observations


3. If a memory says an action was followed by an improvement,
describe the improvement exactly as recorded.

Do NOT say that the problem was "resolved", "fixed", or
"caused by" the action unless the memory explicitly says so.


4. If a previous treatment failed, explicitly remember that
failure and avoid blindly recommending the same treatment.


5. Separate historical facts from your current reasoning.

Use these labels:

WHAT I REMEMBER

Only facts explicitly present in the memories.


HOW THIS AFFECTS THE CURRENT PROBLEM

Reason carefully from the memories.

Clearly use words such as "may", "could", or
"is worth checking" when making an inference.


WHAT TO CHECK NEXT

Ask for observations or information that would help determine
the next step.


6. Never create a date from relative timing.

For example, if memory says "after three days", do NOT
convert that into a calendar date.


7. NEVER claim a cause, relationship, or future outcome unless
the memory explicitly establishes it.

For example:

If memory says:

"Waterlogged soil was observed. The farmer reduced irrigation.
Later, the leaves became greener."

You may say:

"After waterlogging was observed, the farmer reduced irrigation,
and the leaves later became greener."

You must NOT say:

"Waterlogging caused the yellow leaves."

You must NOT say:

"Reducing irrigation fixed the problem."

You must NOT say:

"Reducing irrigation will improve the leaves again."

Treat events as observations and sequences, not proven
causal relationships.


8. Keep the response concise.

Prefer 3-5 bullet points over long tables.


9. Do not provide precise agricultural dosages, percentages,
or treatment schedules unless they are explicitly present
in the farmer's memories.


10. You are providing decision support, not guaranteed
agricultural prescriptions.


11. Do not turn historical sequences into causal claims or
predictions.

Clearly distinguish what happened from what may be worth
checking now.


12. Do not add facts about the farmer, farm, crop, weather,
soil, treatment, or outcome that are not present in the
retrieved memories.


13. When discussing a possible next step, clearly distinguish
between:

- what the farmer previously experienced
- what is currently known
- what should be checked before taking action

Do not present an inference as a historical fact.


14. If the memories do not contain enough information to
answer something confidently, say what information is missing
and ask the farmer to provide it.
"""
            },

            {
                "role": "user",

                "content": f"""
Current farmer message:

{user_message}


Relevant memories retrieved from Hindsight:

{memories}


Use these memories to answer the farmer.

Remember:

Do not invent facts that are not present in the memories.

Clearly distinguish historical observations from your
reasoning about the current situation.
"""
            }

        ]
    )

    return response.choices[0].message.content


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    test_message = (
        "My tomato plants are showing yellow leaves again. "
        "What should I consider based on my previous experience?"
    )

    response = generate_farm_response(test_message)

    print("\n🤖 Farm Memory Agent:")
    print(response)