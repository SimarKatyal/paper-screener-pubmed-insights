import typer
from paper-screener.core import run_pipeline

app = typer.Typer()

def get_papers_list(
    query: str,
    retmax: int = 20,
    debug: bool = False,
    file: str = None
):
    df = run_pipeline(query, retmax, debug)
    if file:
        df.to_csv(file, index = False)
        typer.echo(f"Saved to {file}")
    else:
        typer.echo(df.to_string(index = False))
    
if __name__ == "__main__":
    app()
