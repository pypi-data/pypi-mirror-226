import sys
import click
from getstoken.parserkube import print_contexts,get_token

@click.group()
@click.version_option("1.0.0")
def main():
    """A token fetcher CLI for GKE Cluster"""
    pass


@main.command()
@click.argument('file_path', required=False)
def printContext(**kwargs):
    print_contexts()
    

@main.command()
@click.argument('name', required=False)
def gettoken(**kwargs):
    get_token()


if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("Get Token")
    main()