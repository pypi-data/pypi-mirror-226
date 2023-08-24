import typer
from rich import print

app = typer.Typer()

@app.callback()
def callback():
    """
    MLxploit - An Exploitation Framework for AI/Machine Learning
    """

@app.command()
def attack(
    module: str = typer.Option(prompt=True, help="Attack module", show_default="Adversarial Examples"),
    target: str = typer.Option(prompt=True, help="Target model to be attacked")):
    """
    Attack ML model
    """
    print(f"[green]{module} Attack {target} model")
