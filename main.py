from dotenv import load_dotenv
load_dotenv()
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.agent_graph import custom_graph

if __name__ == "__main__":

    from pprint import pprint
    inputs = {"question": "Who is the president of fisk university?"}

    for output in custom_graph.stream(inputs):
        for key, value in output.items():
            pprint(f"Finished running: {key}:")
    print(value["generation"])
