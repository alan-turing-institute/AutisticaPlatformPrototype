from aws_cdk import (core,
                     aws_ec2 as ec2,
                     aws_rds as rds,
                     aws_ecr as ecr,
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

        # create ecs components
        cluster = ecs.Cluster(self, create_name("cluster"), vpc=vpc)
        service_construct = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, create_name("service"),
            cluster=cluster,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_ecr_repository(
                    ecr.Repository.from_repository_name(
                        self,
                        create_name("ecr-repo"),
                        "autistica-prototype")),
                environment={
                    "DATABASE": ecs.Secret.from_secrets_manager(db.secret).arn
                }
            ),
            public_load_balancer=True)

        # assign permissions for ecs to access db
        db.secret.grant_read(service_construct.task_definition.execution_role)
        # db.connections.security_groups.append(service_construct.service.connections.security_groups)
        db.connections.security_groups[0].add_ingress_rule(
            service_construct.service.connections.security_groups[0],
            ec2.Port.tcp(5432))
