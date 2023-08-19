from typing import Any, Mapping
from typeguard import typechecked
from ..common.task_input import project_dir_input, project_name_input
from ..project_task.task_factory import create_ensure_project_tasks
from ...group import project_group
from ....task.cmd_task import CmdTask
from ....task.decorator import python_task
from ....task.resource_maker import ResourceMaker
from ....runner import runner
from ....config.config import version

import os

CURRENT_DIR = os.path.dirname(__file__)

###############################################################################
# Replacement Mutator Definitions
###############################################################################


@typechecked
def copy_resource_replacement_mutator(
    task: ResourceMaker, replacements: Mapping[str, str]
) -> Mapping[str, str]:
    replacements['zrbBaseProjectDir'] = os.path.basename(
        replacements.get('zrbProjectDir', '')
    )
    if replacements.get('zrbProjectName', '') == '':
        replacements['zrbProjectName'] = replacements.get(
            'zrbBaseProjectDir', ''
        )
    return replacements


###############################################################################
# Task Definitions
###############################################################################


@python_task(
    name='validate',
    inputs=[project_dir_input],
    retry=0,
)
async def validate(*args: Any, **kwargs: Any):
    project_dir = kwargs.get('project_dir')
    if os.path.isfile(os.path.join(project_dir, 'zrb_init.py')):
        raise Exception(f'Project directory already exists: {project_dir}')


copy_resource = ResourceMaker(
    name='copy-resource',
    inputs=[
        project_dir_input,
        project_name_input
    ],
    upstreams=[validate],
    replacements={
        'zrbProjectDir': '{{input.project_dir}}',
        'zrbProjectName': '{{input.project_name}}',
        'zrbVersion': version,
    },
    replacement_mutator=copy_resource_replacement_mutator,
    template_path=os.path.join(CURRENT_DIR, 'template'),
    destination_path='{{input.project_dir}}',
    excludes=[
        '*/__pycache__',
    ]
)

ensure_project_tasks = create_ensure_project_tasks(
    upstreams=[copy_resource]
)

create_project = CmdTask(
    name='create',
    group=project_group,
    upstreams=[ensure_project_tasks],
    inputs=[project_dir_input],
    cmd=[
        'set -e',
        'cd "{{input.project_dir}}"',
        'if [ ! -d .git ]',
        'then',
        '  echo Initialize project git repository',
        '  git init',
        'fi',
        'echo "Happy coding :)"',
    ]
)
runner.register(create_project)
