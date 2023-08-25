from typing import Callable

from airflow.models import Variable
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.decorators import task
import os
from datetime import datetime
from docker.types import Mount


def build_flowpyter_task(task_name=None) -> Callable:
    # Airflow gets in the way of closures here
    container_notebook_dir = os.getenv("CONTAINER_NOTEBOOK_DIR",
                                       "/opt/airflow/notebooks")
    @task.docker(
        image="flowminder/flowpyterlab:api-analyst-latest",
        task_id=task_name,
        mount_tmp_dir=False,
        mounts=[
            Mount(
                source=Variable.get("host_notebook_dir"),
                target=container_notebook_dir,
                type="bind",
            ),
        ],
        environment={"FLOWAPI_TOKEN": "{{ var.value.flowapi_token }}"},
        network_mode="container:flowapi",
        multiple_outputs=False,
    )
    # We need to include notebook_name and nb_paras args here because it isn't closing over the context for some
    # reason - could be to do with the wrapper? I'm wondering if functools.update_wrapper will solve this somehow.
    def this_task(
        execution_date=None,
        previous_notebook=None,
        nb_params=None,
        notebook_name=None,
    ):
        container_notebook_dir = os.getenv("CONTAINER_NOTEBOOK_DIR",
                                       "/opt/airflow/notebooks")
        if nb_params is None:
            nb_params = {}
        if previous_notebook is not None:
            previous_notebook = previous_notebook[
                0
            ]  # This gets put in a list when passed between tasks
        import papermill as pm

        context_params = {
            "execution_date": execution_date,
            "flowapi_url": "http://localhost:9090",  # TODO: Replace with env var
            "previous_notebook": previous_notebook,
        }
        context_params.update(nb_params)

        out_path = (
            f"{container_notebook_dir}/out/{notebook_name}-{execution_date}.ipynb"
        )
        in_path = f"{container_notebook_dir}/{notebook_name}.ipynb"
        pm.execute_notebook(
            in_path,
            out_path,
            parameters=context_params,
            progress_bar=False,
        )
        return out_path

    return this_task
