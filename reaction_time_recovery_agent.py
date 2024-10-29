# Define a model to receive reaction time data
from uagents import Agent, Bureau, Context, Model

class ReactionTimeData(Model):
    reaction_time_data: list

# Create an agent to handle reaction time data
reaction_time_agent = Agent(name="reaction_time_agent", seed="reaction recovery phrase")

# Simulate the end of the game where reaction time data is sent to the reaction time agent
@reaction_time_agent.on_message(model=ReactionTimeData)
async def analyze_reaction_time_data(ctx: Context, sender: str, msg: ReactionTimeData):
    # Log the received reaction time data array
    ctx.logger.info(f"Received reaction time data from {sender}: {msg.reaction_time_data}")
    print(f"Reaction time data from game: {msg.reaction_time_data}")  # Print for now
