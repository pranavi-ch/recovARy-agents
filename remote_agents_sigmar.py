from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
import random

# Define a model to represent the speed data being sent
class SpeedData(Model):
    speed_data: list

# Define the recipient's address where the data will be sent
RECIPIENT_ADDRESS = "agent1qvm7v76zs6w2x90xvq99yc5xh7c2thjtm44zc09me556zxnra627gkf4zum"

# Create the agent "sigmar"
sigmar = Agent(
    name="sigmar",
    port=8000,
    seed="sigmar secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

# Fund the agent if it's low on balance (optional, depends on your use case)
fund_agent_if_low(sigmar.wallet.address())

# Function to send random speed data at intervals
@sigmar.on_interval(period=100.0)  # Adjust the interval as needed
async def send_speed_data(ctx: Context):
    # Simulate a reasonable array of 20 random speed values (e.g., speeds in m/s)
    simulated_speed_data = [round(random.uniform(0.5, 2.5), 2) for _ in range(20)]  # Speeds between 0.5 and 2.5 m/s
    
    # Log the generated speed data and send it to the recipient agent
    ctx.logger.info(f"Sending speed data: {simulated_speed_data}")
    await ctx.send(RECIPIENT_ADDRESS, SpeedData(speed_data=simulated_speed_data))

# Handle incoming messages (if needed, can be adjusted for further interaction)
@sigmar.on_message(model=SpeedData)
async def message_handler(ctx: Context, sender: str, msg: SpeedData):
    ctx.logger.info(f"Received speed data from {sender}: {msg.speed_data}")

if __name__ == "__main__":
    sigmar.run()
