import json
import logging

import click

from cli.check_multithread import MultiThreadsTelnetJob

logger=logging.getLogger("Check Port")

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-i', '--input', default="check_port_list.txt", type=str, help='input file Default : check_port_list.txt.')
@click.option('-o', '--output', default ="_check_port_result.json", type=str, help='output file Default : _check_port_result.json.')
@click.option('-n', '--number-thread', default=500, show_default=True, type=int, help='End block/ISO date/Unix time.')
def check_ports(input,output,number_thread):
    work_data = []
    with open(input, "r") as f:
        lines = f.readlines()
        for line in lines:
            work_data.append(line)
    job = MultiThreadsTelnetJob(work_iterable=work_data, max_workers=number_thread)

    job.run()
    result = job.get_result()

    # Serializing json
    json_object = json.dumps(result, indent=4)

    # Writing to sample.json
    with open(output, "w") as outfile:
        outfile.write(json_object)

@click.group()
@click.version_option(version='2.3.0')
@click.pass_context
def cli(ctx):
    pass


# export
cli.add_command(check_ports, "check_ports")

cli()