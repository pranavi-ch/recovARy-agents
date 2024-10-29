from uagents import Agent, Bureau, Context, Model
import random

# Define a model to represent the speed data being sent
class SpeedData(Model):
    speed_data: list

# Create the speed sender agent that simulates speed data
speed_sender_agent = Agent(name="speed_sender_agent", seed="speed sender recovery phrase")

# Function to simulate user hitting the ball at different speeds and sending data to the speed agent
@speed_sender_agent.on_startup  # Send the data immediately when the agent script is run
async def send_speed_data(ctx: Context):
    # Simulate a reasonable array of 20 speed values (e.g., speeds in m/s)
    simulated_speed_data = [round(random.uniform(0.5, 1.5), 2) for _ in range(20)]  # 20 hits with speeds between 0.5 and 1.5 m/s
    
    # Log and send the simulated speed data to the speed recovery agent
    ctx.logger.info(f"Sending speed data: {simulated_speed_data}")
    await ctx.send(speed_recovery_agent.address, SpeedData(speed_data=simulated_speed_data))

# Speed recovery agent to receive the speed data
speed_recovery_agent = Agent(name="speed_recovery_agent", seed="speed recovery phrase")

@speed_recovery_agent.on_message(model=SpeedData)
async def analyze_speed_data(ctx: Context, sender: str, msg: SpeedData):
    # Log the received speed data array
    ctx.logger.info(f"Received speed data from {sender}: {msg.speed_data}")
    print(f"Speed data from game: {msg.speed_data}")  # Print for now

# Bureau setup to manage the agents
bureau = Bureau()
bureau.add(speed_sender_agent)
bureau.add(speed_recovery_agent)

if __name__ == "__main__":
    # Run the bureau, which will trigger the agents
    bureau.run()
