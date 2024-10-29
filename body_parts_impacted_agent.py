from uagents import Agent, Context, Model
from groq import Groq
import json

# Open and load the JSON file with patient data
with open('patient_data.json', 'r') as file:
    patient_dict = json.load(file)

# Access the 'affected_body_parts' array
affected_body_parts = patient_dict["stroke_details"]["affected_body_parts"]

# Define the message model for body parts impacted
class BodyPartsImpacted(Model):
    message: str

# Create the Body Parts Impacted agent
body_parts_agent = Agent(
    name="body_parts_agent",
    port=8005,
    seed="body_parts_secret_phrase",
)

# Groq API client
client = Groq(api_key="<>")

@body_parts_agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Hello, I'm {ctx.agent.name}")

# Handle requests from the wrapper agent
@body_parts_agent.on_message(model=BodyPartsImpacted)
async def handle_body_parts(ctx: Context, sender: str, msg: BodyPartsImpacted):
    ctx.logger.info(f"Received request for Body Parts recovery plan")
    body_parts_plan = await generate_body_parts_plan()
    await ctx.send(sender, BodyPartsImpacted(message=body_parts_plan))

async def generate_body_parts_plan(ctx):
    body_parts_str = ', '.join(affected_body_parts)
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": f"Generate a recovery plan focusing on these body parts: {body_parts_str}."}
        ],
        model="llama3-8b-8192",
    )
    
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    body_parts_agent.run()
