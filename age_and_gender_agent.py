from uagents import Agent, Context, Model
from groq import Groq

# Define the message model for age and gender
class AgeGender(Model):
    message: str

# Create the Age and Gender agent
age_gender_agent = Agent(
    name="age_gender_agent",
    port=8002,
    seed="age_gender_secret_phrase",
)

# Groq API client
client = Groq(api_key="<>")

@age_gender_agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Hello, I'm {ctx.agent.name}")

# Handle requests from the wrapper agent
@age_gender_agent.on_message(model=AgeGender)
async def handle_age_gender(ctx: Context, sender: str, msg: AgeGender):
    ctx.logger.info(f"Received request for Age and Gender recovery plan")
    age_gender_plan = await generate_age_gender_plan()
    await ctx.send(sender, AgeGender(message=age_gender_plan))

async def generate_age_gender_plan():
    # Call Groq to generate the recovery plan based on age and gender
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": "Generate a recovery plan for a patient based on their age and gender."}
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    age_gender_agent.run()
