#!/usr/bin/env python3

from aws_cdk import Stack, aws_sqs as sqs, App, CfnOutput
from constructs import Construct


class StackA(Stack):
    queue_name = ""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        queue = sqs.Queue(
            self,
            "StackASqsQueueLogicalId",
            queue_name="StackAQueueName",
        )
        self.queue_name = queue.queue_name

        CfnOutput(self, "StackAQueueName", value=queue.queue_name)


class StackB(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, stack_props: dict, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cross_stack_queue_name = stack_props["queue_name"]

        queue = sqs.Queue(
            self,
            "StackBSqsQueueLogicalId",
            queue_name=f"StackBQueueName{cross_stack_queue_name}",
        )

        CfnOutput(self, "StackBQueueName", value=queue.queue_name)


app = App()
stackA = StackA(app, "StackA")
stackB = StackB(app, "StackB", {"queue_name": stackA.queue_name})
app.synth()
