# cdk_pipeline/pipeline_stack.py
from aws_cdk import (
    Stack,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as actions,
    aws_codebuild as codebuild,
    aws_secretsmanager as secretsmanager,
)
from constructs import Construct

class MyPipelineStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        github_secret = secretsmanager.Secret.from_secret_name_v2(
            self, "GitHubToken",
            "GitHubPATCdk"
        )

        source_output = codepipeline.Artifact()
        build_output = codepipeline.Artifact()

        existing_build_project = codebuild.Project.from_project_name(self, "ExistingBuildProject", "pythonCdkBuildProject")

        pipeline = codepipeline.Pipeline(self, "MyPipeline",
            stages=[
                codepipeline.StageProps(
                    stage_name="Source",
                    actions=[
                        actions.GitHubSourceAction(
                            action_name="GitHub_Source",
                            owner="POW2KOR",
                            repo="CDK-Python",
                            oauth_token=github_secret.secret_value,
                            output=source_output,
                            branch="main"
                        )
                    ]
                ),
                codepipeline.StageProps(
                    stage_name="Build",
                    actions=[
                        actions.CodeBuildAction(
                            action_name="CodeBuild",
                            project=existing_build_project,
                            input=source_output,
                            outputs=[build_output]
                        )
                    ]
                )
            ]
        )