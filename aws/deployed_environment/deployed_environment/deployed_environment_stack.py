from aws_cdk import (core,
                     aws_ec2 as ec2,
                     aws_rds as rds,
                     aws_iam as iam,
                     aws_ecs as ecs,
                     aws_ecs_patterns as ecs_patterns)


def create_name(suffix: str) -> str:
    return "ap-" + suffix


class DeployedEnvironmentStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create vpc
        vpc = ec2.Vpc(self, create_name("vpc"))

        # create database
        db_name = create_name("database")
        db = rds.DatabaseInstance(
            self,
            db_name,
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_12_3),
            instance_type=ec2.InstanceType.of(
                instance_class=ec2.InstanceClass.BURSTABLE2,
                instance_size=ec2.InstanceSize.MICRO),
            instance_identifier=db_name,
            master_username="postgres",
            deletion_protection=False,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE))

        # assign permissions for ecs to access db credentials
        role = iam.Role.from_role_arn(self, "role", f"arn:aws:iam::{self.account}:role/ecsTaskExecutionRole")
        db.secret.grant_read(role)

        # create ecs components
        cluster = ecs.Cluster(self, create_name("cluster"), vpc=vpc)
        ecs_patterns.ApplicationLoadBalancedFargateService(
            self, create_name("service"),
            cluster=cluster,  # Required
            cpu=256,  # Default is 256
            desired_count=1,  # Default is 1
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry(
                    f"{self.account}.dkr.ecr.{self.region}.amazonaws.com/autistica-prototype:Latest"),
                    # "amazon/amazon-ecs-sample"),
                environment={
                    "DATABASE": ecs.Secret.from_secrets_manager(db.secret)
                }
            ),
            memory_limit_mib=512,  # Default is 512
            public_load_balancer=True)  # Default is False
