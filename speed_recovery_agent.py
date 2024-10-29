from uagents import Agent, Bureau, Context, Model

# Define a model to receive the game data (array of speed)
class GameData(Model):
    speed_data: list

# Create an agent to handle the speed data
analyzer_agent = Agent(name="analyzer", seed="analyzer recovery phrase")

# Simulate the end of the game where speed data is sent to the analyzer agent
@analyzer_agent.on_message(model=GameData)
async def analyze_speed_data(ctx: Context, sender: str, msg: GameData):
    # Log the received speed data array
    ctx.logger.info(f"Received speed data from {sender}: {msg.speed_data}")
    print(f"Speed data from game: {msg.speed_data}")  # Print for now

# Bureau setup to manage the agent(s)
bureau = Bureau()
bureau.add(analyzer_agent)

if __name__ == "__main__":
    # Start the bureau with the analyzer agent
    bureau.run()



