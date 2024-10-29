from uagents import Agent, Context, Model
from groq import Groq
from flask import Flask
from flask_cors import CORS
import time



# Define models for the different agent responses
class AgeGender(Model):
    message: str

class BodyPartsImpacted(Model):
    message: str

class StrokeCause(Model):
    message: str

class GameData(Model):
    message: str

class CombinedRecoveryPlan(Model):
    combined_plan: str

# Create the Wrapper Agent
wrapper_agent = Agent(
    name="wrapper_agent",
    port=8006,
    seed="wrapper_agent_secret_phrase",
)

# Groq API client
client = Groq(api_key="<>")

# Variables to store agent responses
age_gender_response = None
body_parts_response = None
stroke_cause_response = None
game_data_response = None

@wrapper_agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Hello, I'm {ctx.agent.name}")

# Request data from all agents
async def request_all_data(ctx: Context):
    await request_age_gender_data(ctx)
    await request_body_parts_data(ctx)
    await request_stroke_cause_data(ctx)
    await request_game_data(ctx)

async def request_age_gender_data(ctx: Context):
    global age_gender_response
    await ctx.send("agent1_age_gender_address", AgeGender(message="Request age and gender plan"))

async def request_body_parts_data(ctx: Context):
    global body_parts_response
    await ctx.send("agent1_body_parts_address", BodyPartsImpacted(message="Request body parts recovery plan"))

async def request_stroke_cause_data(ctx: Context):
    global stroke_cause_response
    await ctx.send("agent1_stroke_cause_address", StrokeCause(message="Request stroke cause recovery plan"))

async def request_game_data(ctx: Context):
    global game_data_response
    await ctx.send("agent1_snap_ar_address", GameData(message="Request game data recovery plan"))

# Handle agent responses
@wrapper_agent.on_message(model=AgeGender)
async def handle_age_gender_response(ctx: Context, sender: str, msg: AgeGender):
    global age_gender_response
    age_gender_response = msg.message

@wrapper_agent.on_message(model=BodyPartsImpacted)
async def handle_body_parts_response(ctx: Context, sender: str, msg: BodyPartsImpacted):
    global body_parts_response
    body_parts_response = msg.message

@wrapper_agent.on_message(model=StrokeCause)
async def handle_stroke_cause_response(ctx: Context, sender: str, msg: StrokeCause):
    global stroke_cause_response
    stroke_cause_response = msg.message

@wrapper_agent.on_message(model=GameData)
async def handle_game_data_response(ctx: Context, sender: str, msg: GameData):
    global game_data_response
    game_data_response = msg.message

# Generate recovery plan using Groq LLM
async def generate_groq_combined_plan():
    prompt = (
        f"Age and Gender Plan: {age_gender_response}\n\n"
        f"Body Parts Impacted Plan: {body_parts_response}\n\n"
        f"Stroke Cause Plan: {stroke_cause_response}\n\n"
        f"Game Data Plan: {game_data_response} (more weight on this)\n\n"
        "Provide a plan focusing on these aspects that a patient can go home and do for an hour max based on the plans made beforehand on specific metrics, including physical therapy and cognitive exercises. Only provide the plan and do not give a preliminary and or post plan debreif on it. Just print out the plan."
    )
    
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192",
    )
    with open('./personalized_weekly_plan.txt', mode='w') as file:
        file.write(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content

# Handle POST request to trigger plan generation
@wrapper_agent.on_rest_post("/generate_plan", None, CombinedRecoveryPlan)
async def handle_generate_plan(ctx: Context):
    await request_all_data(ctx)
    time.sleep(5)  # Simulate wait for responses
    combined_plan = await generate_groq_combined_plan()
    return CombinedRecoveryPlan(combined_plan=combined_plan)

if __name__ == "__main__":
    wrapper_agent.run()
