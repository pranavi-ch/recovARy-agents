from uagents import Agent, Context, Model
from groq import Groq
import requests
import json

# API endpoint and request configuration
API_URL = "https://x8ki-letl-twmt.n7.xano.io/api:k_DP2pKT/patient_scores/{patient_scores_id}"
# Headers if any required for API request
HEADERS = {
    "Content-Type": "application/json"
}

# Function to fetch the game scores using an API call
def fetch_scores(patient_scores_id, game_type):
    url = API_URL.replace("{patient_scores_id}", str(patient_scores_id))

    # Request payload with game type
    payload = {
        "game_type": game_type  # "TT" for table tennis or "FN" for finger navigation, etc.
    }

    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Return the JSON data from the API response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching scores: {e}")
        return None

# Define the message model for game statistics
class GameData(Model):
    message: str

# Create the Snap AR Game Statistics agent
snap_ar_agent = Agent(
    name="snap_ar_agent",
    port=8004,
    seed="snap_ar_secret_phrase",
)

# Groq API client
client = Groq(api_key="<>")

@snap_ar_agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Hello, I'm {ctx.agent.name}")

# Handle requests from the wrapper agent
@snap_ar_agent.on_message(model=GameData)
async def handle_game_data(ctx: Context, sender: str, msg: GameData):
    ctx.logger.info(f"Received request for Game Data recovery plan")
    game_data_plan = await generate_game_data_plan()
    await ctx.send(sender, GameData(message=game_data_plan))

async def generate_game_data_plan():
    # Fetching patient data from the API with patient_scores_id and game_type
    tennis_data = fetch_scores("TT")
    fruit_data = fetch_scores("FN")

    if tennis_data is None:
        return "Error: Could not fetch game scores."

    # Extract speed and reaction time data from the API response
    speed_str = tennis_data["scores_text"]
    reaction_time_str = fruit_data["scores_text"]

    print(speed_str)
    print(reaction_time_str)
    

    # Call Groq API to generate a recovery plan based on fetched data
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": (
                    f"Generate a recovery plan based on the following speed data: {speed_str} "
                    f"and reaction time data: {reaction_time_str}. Focus on physical and cognitive exercises."
                )
            }
        ],
        model="gemma-7b-it",
    )

    print("YOOO")
    print(speed_str)
    # Return the generated recovery plan
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    snap_ar_agent.run()
