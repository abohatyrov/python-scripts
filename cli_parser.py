import argparse

def add(args):
    result = args.a + args.b
    print(f"{args.a} + {args.b} = {result}")

def subtract(args):
    result = args.a - args.b
    print(f"{args.a} - {args.b} = {result}")

def multiply(args):
    result = args.a * args.b
    print(f"{args.a} * {args.b} = {result}")

def divide(args):
    result = args.a / args.b
    print(f"{args.a} / {args.b} = {result}")

parser = argparse.ArgumentParser(description="A simple calculator CLI.")
subparsers = parser.add_subparsers(title="Commands", dest="command")

add_parser = subparsers.add_parser("add", help="Add two numbers.")
add_parser.add_argument("a", type=float, help="The first number.")
add_parser.add_argument("b", type=float, help="The second number.")
add_parser.set_defaults(func=add)

subtract_parser = subparsers.add_parser("subtract", help="Subtract two numbers.")
subtract_parser.add_argument("a", type=float, help="The first number.")
subtract_parser.add_argument("b", type=float, help="The second number.")
subtract_parser.set_defaults(func=subtract)

multiply_parser = subparsers.add_parser("multiply", help="Multiply two numbers.")
multiply_parser.add_argument("a", type=float, help="The first number.")
multiply_parser.add_argument("b", type=float, help="The second number.")
multiply_parser.set_defaults(func=multiply)

divide_parser = subparsers.add_parser("divide", help="Divide two numbers.")
divide_parser.add_argument("a", type=float, help="The first number.")
divide_parser.add_argument("b", type=float, help="The second number.")
divide_parser.set_defaults(func=divide)

args = parser.parse_args()
args.func(args)
