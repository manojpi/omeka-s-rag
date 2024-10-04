import typer
from dotenv import load_dotenv
load_dotenv()
import sys
import os
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

app = typer.Typer(invoke_without_command=True) # Initialize the typer cli with no command support

from src.agent_graph import custom_graph

@app.command()
def defualt():

    while (True):
        question = input("What is your question? ")
        if not question:
            return
        inputs = {"question": question}

        for output in custom_graph.stream(inputs):
            for key, value in output.items():
                pprint(f"Finished running: {key}:")
        print(value["generation"])

if __name__ == "__main__":

    app()
    
