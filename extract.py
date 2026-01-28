import json, time, os
from dotenv import load_dotenv
from groq import Groq
from schemas import Shipment
from prompts import PROMPT_V2
from tqdm import tqdm

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# Load input files
emails = json.load(open("emails_input.json"))
ports = json.load(open("port_codes_reference.json"))

# Build port lookup
PORT_LOOKUP = {}
for p in ports:
    PORT_LOOKUP[p["name"].lower()] = p["code"]

def call_llm(prompt, retries=3):
    for i in range(retries):
        try:
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            return res.choices[0].message.content  
        except Exception as e:
            print("\n GROQ ERROR:", e)
            time.sleep(2 ** i)
    return None


results = []

for email in tqdm(emails):
    prompt = PROMPT_V2.format(
        subject=email["subject"],
        body=email["body"]
    )

    raw = call_llm(prompt)


    # If LLM totally failed
    if raw is None:
        results.append(Shipment(
            id=email["id"],
            product_line=None,
            origin_port_code=None,
            origin_port_name=None,
            destination_port_code=None,
            destination_port_name=None,
            incoterm=None,
            cargo_weight_kg=None,
            cargo_cbm=None,
            is_dangerous=False
        ).model_dump())
        continue

    try:
        import re

        match = re.search(r"\{.*\}", raw, re.S)
        if not match:
            raise ValueError("No JSON found in LLM output")

        data = json.loads(match.group())
        shipment = Shipment(id=email["id"], **data)
        results.append(shipment.model_dump())

    except Exception as ex:
        print("Parse error:", ex)

        results.append(Shipment(
            id=email["id"],
            product_line=None,
            origin_port_code=None,
            origin_port_name=None,
            destination_port_code=None,
            destination_port_name=None,
            incoterm=None,
            cargo_weight_kg=None,
            cargo_cbm=None,
            is_dangerous=False
        ).model_dump())


json.dump(results, open("output.json", "w"), indent=2)
print("output.json generated")
