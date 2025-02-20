import click

@click.command()
@click.option('--a', type=int, required=True, help='First number.')
@click.option('--b', type=int, required=True, help='Second number.')
def multiply(a, b):
    """Multiply two numbers and display the result."""
    result = a * b
    click.echo(f'{a} x {b} = {result}')
    
if __name__ == '__main__':
    multiply()