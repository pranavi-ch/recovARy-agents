from flask import Flask
from flask_cors import CORS
import wrapper_agent
import asyncio
app = Flask(__name__)


CORS(app, resources={r"/data": {"origins": "http://localhost:3000"}})
CORS(app, resources={r"/data": {"origins": "http://localhost:3000"}}, supports_credentials=True)


@app.route('/data', methods=['POST'])
def tr():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_until_complete(wrapper_agent.generate_groq_combined_plan)
    return "LOL"

if __name__ == '__main__':
    app.run(port=5173, use_reloader=False, threaded=True)