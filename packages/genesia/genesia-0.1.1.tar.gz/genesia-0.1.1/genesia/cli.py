import click
import socketio
import os.path as osp
from yaspin import yaspin
from yaspin.spinners import Spinners
from genesia_templates import create_project_from_template, available_templates

class DynamicText:
    def __init__(self, init_value):
        self.value = init_value

    def update(self, new_value):
        self.value = new_value

    def __str__(self):
        return self.value

@click.group()
def cli():
    pass

@cli.command("create")
@click.option('--name', help='Name of the project', required=True)
@click.option('--template', type=click.Choice(available_templates), help='Template to use (see more https://github.com/ThomasCloarec/genesia-templates)', required=True)
@click.option('--prompt', prompt='Describe what you want to do', help='Describe what you want to do', required=True)
@click.option('--openai-api-key', prompt='OpenAI API key', help='OpenAI API key', required=True, hide_input=True)
def create_project(name, template, prompt, openai_api_key):
    assert not osp.exists(name), f'Project {name} already exists'

    text = DynamicText("Connecting to our AI...")

    with yaspin(Spinners.pong, text=text, color="yellow") as spinner:
        sio = socketio.Client()

        def on_create_project_response(data):
            if data['status'] == 'error':
                print(data['message'])
            elif data['status'] == 'success':
                assert 'result' in data, '[Internal Error] No result in response'
                result = data['result']
                print('result', result)
                create_project_from_template(template, name, result)
                print('Project {} created'.format(name))
            sio.disconnect()

        @sio.on("connect")
        def on_connect():
            text.update("Generating your project...")
            sio.emit("create_project", {"name": name, "template": template, "prompt": prompt, "api_key": openai_api_key}, callback=on_create_project_response)

        @sio.on("create_project")
        def on_create_project(msg):
            spinner.write(text)
            text.update(msg)

        @sio.on("disconnect")
        def on_disconnect():
            sio.disconnect()

        # sio.connect("http://localhost:8000/")
        sio.connect("https://genesia-api.onrender.com/")

        try:
            sio.wait()
        except KeyboardInterrupt:
            pass
        finally:
            sio.disconnect()

def run_cli():
    try:
        cli()
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    run_cli()