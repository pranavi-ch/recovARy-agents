from uagents import Agent, Context, Model
from groq import Groq
import json

# Open and load the JSON file with patient data
with open('patient_data.json', 'r') as file:
    patient_dict = json.load(file)

cause_of_stroke = patient_dict["stroke_details"]["cause"]
date_of_stroke = patient_dict["stroke_details"]["date_of_stroke"]

# Define the message model for stroke cause
class StrokeCause(Model):
    message: str

# Create the Stroke Cause agent
cause_stroke_agent = Agent(
    name="cause_stroke_agent",
    port=8003,
    seed="cause_stroke_secret_phrase",
)

# Groq API client
client = Groq(api_key="<>")

@cause_stroke_agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Hello, I'm {ctx.agent.name}")

# Handle requests from the wrapper agent
@cause_stroke_agent.on_message(model=StrokeCause)
async def handle_stroke_cause(ctx: Context, sender: str, msg: StrokeCause):
    ctx.logger.info(f"Received request for Stroke Cause recovery plan")
    stroke_cause_plan = await generate_stroke_cause_plan()
    await ctx.send(sender, StrokeCause(message=stroke_cause_plan))

async def generate_stroke_cause_plan():
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": f"Generate a recovery plan for an {cause_of_stroke} stroke that occurred on {date_of_stroke}."}
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    cause_stroke_agent.run()
