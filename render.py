import argparse

import jinja2
import yaml
import os


def load_template(template_filename):
    with open(template_filename, 'r') as f:
        template_content = f.read()

    return jinja2.Template(template_content)


def load_vars(var_filename):
    loaded_vars = {}
    with open(var_filename, 'r') as f:
        secrets_content = f.read()
    content = yaml.full_load(secrets_content) or {}
    assert(isinstance(content, dict))
    loaded_vars.update(content)

    return loaded_vars


def save_output(result, output_filename):
    with open(output_filename, 'w') as f:
        f.write(result)


def render(args):
    
    
    template_filename = args.template_filename
    var_filename = args.var_filename
    
    template = load_template(template_filename)
    loaded_vars = load_vars(var_filename)
    
    if args.env_vars:
        env_vars_section = build_env_vars_section(args.env_vars)
        loaded_vars.update({'ENV_VARIABLES': env_vars_section})

    result = template.render(**loaded_vars)

    assert(template_filename.endswith('.template'))
    output_filename = template_filename.replace('.template', '')
    
    save_output(result, output_filename)


def build_env_vars_section(env_vars):
    content = 'env_variables:' + os.linesep
    for k, v in list(env_vars.items()):
        content += '  {}: {}'.format(k, v)
        content += os.linesep
        
    return content


class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value
            
            
def get_args():
    parser = argparse.ArgumentParser(
        description='Render a template file with variable injection',
    )

    parser.add_argument(
        dest='template_filename',
        help='Input template'
    )

    parser.add_argument(
        dest='var_filename',
        help='Variable file'
    )
    
    parser.add_argument(
        '-e', '--env', nargs='*', action=ParseKwargs, dest='env_vars', 
        help='Extra environment properties', default={}
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    
    render(args)
