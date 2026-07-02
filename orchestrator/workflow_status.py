from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class WorkflowStep:

    name: str

    status: str = "Waiting"

    started: str | None = None

    completed: str | None = None

    duration: float = 0.0


class WorkflowStatus:

    def __init__(self):

        self.steps = {

            "planner": WorkflowStep("Planner"),

            "memory": WorkflowStep("Memory Retrieval"),

            "knowledge": WorkflowStep("Knowledge Retrieval"),

            "executor": WorkflowStep("Executor"),

            "reviewer": WorkflowStep("Reviewer"),

            "finished": WorkflowStep("Finished")

        }

    # ----------------------------------

    def start(self, step):

        self.steps[step].status = "Running"

        self.steps[step].started = datetime.now()

    # ----------------------------------

    def complete(self, step):

        obj = self.steps[step]

        obj.completed = datetime.now()

        obj.status = "Completed"

        obj.duration = round(

            (

                obj.completed -

                obj.started

            ).total_seconds(),

            2

        )

    # ----------------------------------

    def finish(self):

        self.steps["finished"].status = "Completed"

    # ----------------------------------

    def to_list(self):

        result = []

        for step in self.steps.values():

            result.append(

                {

                    "Step": step.name,

                    "Status": step.status,

                    "Duration (sec)": step.duration

                }

            )

        return result