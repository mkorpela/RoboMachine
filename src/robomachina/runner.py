import sys
import robomachina

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    with open(input_file, 'r') as inp:
        with open(output_file, 'w') as out:
            model = robomachina.parse(inp.read())
            robomachina.generate_all_dfs(model, 10, out)
