'''
# `aws_glue_job`

Refer to the Terraform Registory for docs: [`aws_glue_job`](https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class GlueJob(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueJob.GlueJob",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job aws_glue_job}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        command: typing.Union["GlueJobCommand", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        role_arn: builtins.str,
        connections: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        execution_class: typing.Optional[builtins.str] = None,
        execution_property: typing.Optional[typing.Union["GlueJobExecutionProperty", typing.Dict[builtins.str, typing.Any]]] = None,
        glue_version: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        non_overridable_arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        notification_property: typing.Optional[typing.Union["GlueJobNotificationProperty", typing.Dict[builtins.str, typing.Any]]] = None,
        number_of_workers: typing.Optional[jsii.Number] = None,
        security_configuration: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        worker_type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job aws_glue_job} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param command: command block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#command GlueJob#command}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#name GlueJob#name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#role_arn GlueJob#role_arn}.
        :param connections: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#connections GlueJob#connections}.
        :param default_arguments: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#default_arguments GlueJob#default_arguments}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#description GlueJob#description}.
        :param execution_class: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#execution_class GlueJob#execution_class}.
        :param execution_property: execution_property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#execution_property GlueJob#execution_property}
        :param glue_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#glue_version GlueJob#glue_version}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#id GlueJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_capacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#max_capacity GlueJob#max_capacity}.
        :param max_retries: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#max_retries GlueJob#max_retries}.
        :param non_overridable_arguments: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#non_overridable_arguments GlueJob#non_overridable_arguments}.
        :param notification_property: notification_property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#notification_property GlueJob#notification_property}
        :param number_of_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#number_of_workers GlueJob#number_of_workers}.
        :param security_configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#security_configuration GlueJob#security_configuration}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#tags GlueJob#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#tags_all GlueJob#tags_all}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#timeout GlueJob#timeout}.
        :param worker_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#worker_type GlueJob#worker_type}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0983076a5a37b1adb90a2d464044a77b2fd1117d838b2804fb98c1d0d5b173e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GlueJobConfig(
            command=command,
            name=name,
            role_arn=role_arn,
            connections=connections,
            default_arguments=default_arguments,
            description=description,
            execution_class=execution_class,
            execution_property=execution_property,
            glue_version=glue_version,
            id=id,
            max_capacity=max_capacity,
            max_retries=max_retries,
            non_overridable_arguments=non_overridable_arguments,
            notification_property=notification_property,
            number_of_workers=number_of_workers,
            security_configuration=security_configuration,
            tags=tags,
            tags_all=tags_all,
            timeout=timeout,
            worker_type=worker_type,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putCommand")
    def put_command(
        self,
        *,
        script_location: builtins.str,
        name: typing.Optional[builtins.str] = None,
        python_version: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param script_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#script_location GlueJob#script_location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#name GlueJob#name}.
        :param python_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#python_version GlueJob#python_version}.
        :param runtime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#runtime GlueJob#runtime}.
        '''
        value = GlueJobCommand(
            script_location=script_location,
            name=name,
            python_version=python_version,
            runtime=runtime,
        )

        return typing.cast(None, jsii.invoke(self, "putCommand", [value]))

    @jsii.member(jsii_name="putExecutionProperty")
    def put_execution_property(
        self,
        *,
        max_concurrent_runs: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrent_runs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#max_concurrent_runs GlueJob#max_concurrent_runs}.
        '''
        value = GlueJobExecutionProperty(max_concurrent_runs=max_concurrent_runs)

        return typing.cast(None, jsii.invoke(self, "putExecutionProperty", [value]))

    @jsii.member(jsii_name="putNotificationProperty")
    def put_notification_property(
        self,
        *,
        notify_delay_after: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param notify_delay_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#notify_delay_after GlueJob#notify_delay_after}.
        '''
        value = GlueJobNotificationProperty(notify_delay_after=notify_delay_after)

        return typing.cast(None, jsii.invoke(self, "putNotificationProperty", [value]))

    @jsii.member(jsii_name="resetConnections")
    def reset_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnections", []))

    @jsii.member(jsii_name="resetDefaultArguments")
    def reset_default_arguments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultArguments", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExecutionClass")
    def reset_execution_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionClass", []))

    @jsii.member(jsii_name="resetExecutionProperty")
    def reset_execution_property(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionProperty", []))

    @jsii.member(jsii_name="resetGlueVersion")
    def reset_glue_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGlueVersion", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaxCapacity")
    def reset_max_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxCapacity", []))

    @jsii.member(jsii_name="resetMaxRetries")
    def reset_max_retries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRetries", []))

    @jsii.member(jsii_name="resetNonOverridableArguments")
    def reset_non_overridable_arguments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNonOverridableArguments", []))

    @jsii.member(jsii_name="resetNotificationProperty")
    def reset_notification_property(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationProperty", []))

    @jsii.member(jsii_name="resetNumberOfWorkers")
    def reset_number_of_workers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumberOfWorkers", []))

    @jsii.member(jsii_name="resetSecurityConfiguration")
    def reset_security_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityConfiguration", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetWorkerType")
    def reset_worker_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerType", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> "GlueJobCommandOutputReference":
        return typing.cast("GlueJobCommandOutputReference", jsii.get(self, "command"))

    @builtins.property
    @jsii.member(jsii_name="executionProperty")
    def execution_property(self) -> "GlueJobExecutionPropertyOutputReference":
        return typing.cast("GlueJobExecutionPropertyOutputReference", jsii.get(self, "executionProperty"))

    @builtins.property
    @jsii.member(jsii_name="notificationProperty")
    def notification_property(self) -> "GlueJobNotificationPropertyOutputReference":
        return typing.cast("GlueJobNotificationPropertyOutputReference", jsii.get(self, "notificationProperty"))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional["GlueJobCommand"]:
        return typing.cast(typing.Optional["GlueJobCommand"], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionsInput")
    def connections_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "connectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultArgumentsInput")
    def default_arguments_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "defaultArgumentsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="executionClassInput")
    def execution_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionClassInput"))

    @builtins.property
    @jsii.member(jsii_name="executionPropertyInput")
    def execution_property_input(self) -> typing.Optional["GlueJobExecutionProperty"]:
        return typing.cast(typing.Optional["GlueJobExecutionProperty"], jsii.get(self, "executionPropertyInput"))

    @builtins.property
    @jsii.member(jsii_name="glueVersionInput")
    def glue_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "glueVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="maxCapacityInput")
    def max_capacity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxCapacityInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRetriesInput")
    def max_retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetriesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nonOverridableArgumentsInput")
    def non_overridable_arguments_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "nonOverridableArgumentsInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationPropertyInput")
    def notification_property_input(
        self,
    ) -> typing.Optional["GlueJobNotificationProperty"]:
        return typing.cast(typing.Optional["GlueJobNotificationProperty"], jsii.get(self, "notificationPropertyInput"))

    @builtins.property
    @jsii.member(jsii_name="numberOfWorkersInput")
    def number_of_workers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numberOfWorkersInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="securityConfigurationInput")
    def security_configuration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="workerTypeInput")
    def worker_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "connections"))

    @connections.setter
    def connections(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d673703ec42448867a01399721901aef946957f844baab73a79889a68a8bc9e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connections", value)

    @builtins.property
    @jsii.member(jsii_name="defaultArguments")
    def default_arguments(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "defaultArguments"))

    @default_arguments.setter
    def default_arguments(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91704f17a0eee40be4828cadf3053d5c14695a1b80b4f344729ab05a7984c7f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultArguments", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e962a6c1dbeca5d6d4b37eaf2ead162e1d0924b535c70cd81a0f3e8b077b1369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="executionClass")
    def execution_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionClass"))

    @execution_class.setter
    def execution_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__035895538a9bfc5916d93775d89658d94253c471e979fd49c3cf2fb6c5627b29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionClass", value)

    @builtins.property
    @jsii.member(jsii_name="glueVersion")
    def glue_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "glueVersion"))

    @glue_version.setter
    def glue_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9573db644b3bb09df25cf85a98f721fa5a0ff1707a3ce23282d0ecddaa3e58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "glueVersion", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8e2b4a1f00e04184067d6bf979762470bcaae5c7dab296c6165aa200f3c468a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="maxCapacity")
    def max_capacity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxCapacity"))

    @max_capacity.setter
    def max_capacity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4a144066e12645a65d7c4177afa9aa79456cd1f3bbe47c13293a4e8396f5807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxCapacity", value)

    @builtins.property
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRetries"))

    @max_retries.setter
    def max_retries(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02072b73eef7b71ec8c5c2b6c8632b57e7a1a815e671d67dc4be01b8b5390410)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetries", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__150ade938d1bbbc493b4240934556608c145920b27488d308a3c97a35fe27617)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="nonOverridableArguments")
    def non_overridable_arguments(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "nonOverridableArguments"))

    @non_overridable_arguments.setter
    def non_overridable_arguments(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2491eeb74b8a3e7f101d692134a18058b2073967197c62039c159bbe60732bc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nonOverridableArguments", value)

    @builtins.property
    @jsii.member(jsii_name="numberOfWorkers")
    def number_of_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numberOfWorkers"))

    @number_of_workers.setter
    def number_of_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__013ac8372401db3185f3f16a0ef44c8f5b217f309ae7c21082ea34513b1a382e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numberOfWorkers", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0873a7854da323eb39428cf1ecca8a01d0d406ebf3a7768abcdb5209276ccbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="securityConfiguration")
    def security_configuration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityConfiguration"))

    @security_configuration.setter
    def security_configuration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bf24edd9c1558d9c7ffa03e428011e1694a71e9c4f32f8a8de1b9cd9369497e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37dc6893b13503529d0d58a02077844db38432007ccc4d3e09bd3ba49e6a3b9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9c4d5862966e4efd381b24252f4f69474429efc4bcf6ad79b2bcc297c84b401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3f0f3d3dbf2555dc4cebc59aed7734df2e863055c163b89394c1db2228b51a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value)

    @builtins.property
    @jsii.member(jsii_name="workerType")
    def worker_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workerType"))

    @worker_type.setter
    def worker_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae472e0c17dfa260a9135f57ee8b4ad78f88fac97ee11ebeaaa5b4f3a03001f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerType", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.glueJob.GlueJobCommand",
    jsii_struct_bases=[],
    name_mapping={
        "script_location": "scriptLocation",
        "name": "name",
        "python_version": "pythonVersion",
        "runtime": "runtime",
    },
)
class GlueJobCommand:
    def __init__(
        self,
        *,
        script_location: builtins.str,
        name: typing.Optional[builtins.str] = None,
        python_version: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param script_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#script_location GlueJob#script_location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#name GlueJob#name}.
        :param python_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#python_version GlueJob#python_version}.
        :param runtime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#runtime GlueJob#runtime}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a073d517d4910d8b90fc9874dce1467d15f777662fc2f465e75f206d22bc676)
            check_type(argname="argument script_location", value=script_location, expected_type=type_hints["script_location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument python_version", value=python_version, expected_type=type_hints["python_version"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "script_location": script_location,
        }
        if name is not None:
            self._values["name"] = name
        if python_version is not None:
            self._values["python_version"] = python_version
        if runtime is not None:
            self._values["runtime"] = runtime

    @builtins.property
    def script_location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#script_location GlueJob#script_location}.'''
        result = self._values.get("script_location")
        assert result is not None, "Required property 'script_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#name GlueJob#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def python_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#python_version GlueJob#python_version}.'''
        result = self._values.get("python_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#runtime GlueJob#runtime}.'''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueJobCommand(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueJobCommandOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueJob.GlueJobCommandOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f335ce967c912d299e87f0560b3a3affb413be392d5296a655f1cb96ea2b864)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPythonVersion")
    def reset_python_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPythonVersion", []))

    @jsii.member(jsii_name="resetRuntime")
    def reset_runtime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntime", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pythonVersionInput")
    def python_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pythonVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeInput")
    def runtime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptLocationInput")
    def script_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scriptLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e52cfae71ded6e5ea8c2539568479ebf6e62a6529c0ec38f3c363a44c7d8cd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="pythonVersion")
    def python_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pythonVersion"))

    @python_version.setter
    def python_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5efb7f4c69c45b343860b37ebab8472a0e39beef6dfc99e4a7816eaee1adc143)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pythonVersion", value)

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__638fe14d2e27d9f4d310021d601cde5e7b5dd8435a89dc1e18843abd90638753)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value)

    @builtins.property
    @jsii.member(jsii_name="scriptLocation")
    def script_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scriptLocation"))

    @script_location.setter
    def script_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__432e2f5d742ba3e19fc82bbb3203710fb250f70b435d5b3dca7b873be9d59f75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptLocation", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GlueJobCommand]:
        return typing.cast(typing.Optional[GlueJobCommand], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GlueJobCommand]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e287cc57c754ae957d83fce548f3c1b78d30e6440defa2faf44b788e0dc1109e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.glueJob.GlueJobConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "command": "command",
        "name": "name",
        "role_arn": "roleArn",
        "connections": "connections",
        "default_arguments": "defaultArguments",
        "description": "description",
        "execution_class": "executionClass",
        "execution_property": "executionProperty",
        "glue_version": "glueVersion",
        "id": "id",
        "max_capacity": "maxCapacity",
        "max_retries": "maxRetries",
        "non_overridable_arguments": "nonOverridableArguments",
        "notification_property": "notificationProperty",
        "number_of_workers": "numberOfWorkers",
        "security_configuration": "securityConfiguration",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeout": "timeout",
        "worker_type": "workerType",
    },
)
class GlueJobConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        command: typing.Union[GlueJobCommand, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        role_arn: builtins.str,
        connections: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        execution_class: typing.Optional[builtins.str] = None,
        execution_property: typing.Optional[typing.Union["GlueJobExecutionProperty", typing.Dict[builtins.str, typing.Any]]] = None,
        glue_version: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        non_overridable_arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        notification_property: typing.Optional[typing.Union["GlueJobNotificationProperty", typing.Dict[builtins.str, typing.Any]]] = None,
        number_of_workers: typing.Optional[jsii.Number] = None,
        security_configuration: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        worker_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param command: command block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#command GlueJob#command}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#name GlueJob#name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#role_arn GlueJob#role_arn}.
        :param connections: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#connections GlueJob#connections}.
        :param default_arguments: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#default_arguments GlueJob#default_arguments}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#description GlueJob#description}.
        :param execution_class: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#execution_class GlueJob#execution_class}.
        :param execution_property: execution_property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#execution_property GlueJob#execution_property}
        :param glue_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#glue_version GlueJob#glue_version}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#id GlueJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_capacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#max_capacity GlueJob#max_capacity}.
        :param max_retries: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#max_retries GlueJob#max_retries}.
        :param non_overridable_arguments: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#non_overridable_arguments GlueJob#non_overridable_arguments}.
        :param notification_property: notification_property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#notification_property GlueJob#notification_property}
        :param number_of_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#number_of_workers GlueJob#number_of_workers}.
        :param security_configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#security_configuration GlueJob#security_configuration}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#tags GlueJob#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#tags_all GlueJob#tags_all}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#timeout GlueJob#timeout}.
        :param worker_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#worker_type GlueJob#worker_type}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(command, dict):
            command = GlueJobCommand(**command)
        if isinstance(execution_property, dict):
            execution_property = GlueJobExecutionProperty(**execution_property)
        if isinstance(notification_property, dict):
            notification_property = GlueJobNotificationProperty(**notification_property)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70e13f1ce4a6ddc4ccfa87affe691b571f525e5f206e3a43bed54b245f739c71)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument connections", value=connections, expected_type=type_hints["connections"])
            check_type(argname="argument default_arguments", value=default_arguments, expected_type=type_hints["default_arguments"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument execution_class", value=execution_class, expected_type=type_hints["execution_class"])
            check_type(argname="argument execution_property", value=execution_property, expected_type=type_hints["execution_property"])
            check_type(argname="argument glue_version", value=glue_version, expected_type=type_hints["glue_version"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument non_overridable_arguments", value=non_overridable_arguments, expected_type=type_hints["non_overridable_arguments"])
            check_type(argname="argument notification_property", value=notification_property, expected_type=type_hints["notification_property"])
            check_type(argname="argument number_of_workers", value=number_of_workers, expected_type=type_hints["number_of_workers"])
            check_type(argname="argument security_configuration", value=security_configuration, expected_type=type_hints["security_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument worker_type", value=worker_type, expected_type=type_hints["worker_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "command": command,
            "name": name,
            "role_arn": role_arn,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if connections is not None:
            self._values["connections"] = connections
        if default_arguments is not None:
            self._values["default_arguments"] = default_arguments
        if description is not None:
            self._values["description"] = description
        if execution_class is not None:
            self._values["execution_class"] = execution_class
        if execution_property is not None:
            self._values["execution_property"] = execution_property
        if glue_version is not None:
            self._values["glue_version"] = glue_version
        if id is not None:
            self._values["id"] = id
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if non_overridable_arguments is not None:
            self._values["non_overridable_arguments"] = non_overridable_arguments
        if notification_property is not None:
            self._values["notification_property"] = notification_property
        if number_of_workers is not None:
            self._values["number_of_workers"] = number_of_workers
        if security_configuration is not None:
            self._values["security_configuration"] = security_configuration
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if timeout is not None:
            self._values["timeout"] = timeout
        if worker_type is not None:
            self._values["worker_type"] = worker_type

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def command(self) -> GlueJobCommand:
        '''command block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#command GlueJob#command}
        '''
        result = self._values.get("command")
        assert result is not None, "Required property 'command' is missing"
        return typing.cast(GlueJobCommand, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#name GlueJob#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#role_arn GlueJob#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connections(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#connections GlueJob#connections}.'''
        result = self._values.get("connections")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def default_arguments(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#default_arguments GlueJob#default_arguments}.'''
        result = self._values.get("default_arguments")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#description GlueJob#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_class(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#execution_class GlueJob#execution_class}.'''
        result = self._values.get("execution_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_property(self) -> typing.Optional["GlueJobExecutionProperty"]:
        '''execution_property block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#execution_property GlueJob#execution_property}
        '''
        result = self._values.get("execution_property")
        return typing.cast(typing.Optional["GlueJobExecutionProperty"], result)

    @builtins.property
    def glue_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#glue_version GlueJob#glue_version}.'''
        result = self._values.get("glue_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#id GlueJob#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#max_capacity GlueJob#max_capacity}.'''
        result = self._values.get("max_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#max_retries GlueJob#max_retries}.'''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def non_overridable_arguments(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#non_overridable_arguments GlueJob#non_overridable_arguments}.'''
        result = self._values.get("non_overridable_arguments")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def notification_property(self) -> typing.Optional["GlueJobNotificationProperty"]:
        '''notification_property block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#notification_property GlueJob#notification_property}
        '''
        result = self._values.get("notification_property")
        return typing.cast(typing.Optional["GlueJobNotificationProperty"], result)

    @builtins.property
    def number_of_workers(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#number_of_workers GlueJob#number_of_workers}.'''
        result = self._values.get("number_of_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def security_configuration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#security_configuration GlueJob#security_configuration}.'''
        result = self._values.get("security_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#tags GlueJob#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#tags_all GlueJob#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#timeout GlueJob#timeout}.'''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def worker_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#worker_type GlueJob#worker_type}.'''
        result = self._values.get("worker_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueJobConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.glueJob.GlueJobExecutionProperty",
    jsii_struct_bases=[],
    name_mapping={"max_concurrent_runs": "maxConcurrentRuns"},
)
class GlueJobExecutionProperty:
    def __init__(
        self,
        *,
        max_concurrent_runs: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrent_runs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#max_concurrent_runs GlueJob#max_concurrent_runs}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50d53cb786d387f3a2e006c67ae1fea4a9576cce50f42105fbb0ed3f8e307709)
            check_type(argname="argument max_concurrent_runs", value=max_concurrent_runs, expected_type=type_hints["max_concurrent_runs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_concurrent_runs is not None:
            self._values["max_concurrent_runs"] = max_concurrent_runs

    @builtins.property
    def max_concurrent_runs(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#max_concurrent_runs GlueJob#max_concurrent_runs}.'''
        result = self._values.get("max_concurrent_runs")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueJobExecutionProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueJobExecutionPropertyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueJob.GlueJobExecutionPropertyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d06995acfeb32f10fa9b80e5e7e20b78c1fce187b34127314a5416e2e4f6c0df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxConcurrentRuns")
    def reset_max_concurrent_runs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConcurrentRuns", []))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentRunsInput")
    def max_concurrent_runs_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrentRunsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentRuns")
    def max_concurrent_runs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrentRuns"))

    @max_concurrent_runs.setter
    def max_concurrent_runs(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a85d69a5a8fb1feafa7ee4cea2c4e3965797f78b457c3a0283e4143fb5048dae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrentRuns", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GlueJobExecutionProperty]:
        return typing.cast(typing.Optional[GlueJobExecutionProperty], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GlueJobExecutionProperty]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d038b129ba4bc4f5460a93a577be2aad01cfd542b768212c61165e126417aa5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.glueJob.GlueJobNotificationProperty",
    jsii_struct_bases=[],
    name_mapping={"notify_delay_after": "notifyDelayAfter"},
)
class GlueJobNotificationProperty:
    def __init__(
        self,
        *,
        notify_delay_after: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param notify_delay_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#notify_delay_after GlueJob#notify_delay_after}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69d36cb48288ee3a80cdac85fe6d8c8b9c4e7edb71724edf6b9e31afad92b621)
            check_type(argname="argument notify_delay_after", value=notify_delay_after, expected_type=type_hints["notify_delay_after"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if notify_delay_after is not None:
            self._values["notify_delay_after"] = notify_delay_after

    @builtins.property
    def notify_delay_after(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/glue_job#notify_delay_after GlueJob#notify_delay_after}.'''
        result = self._values.get("notify_delay_after")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueJobNotificationProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueJobNotificationPropertyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueJob.GlueJobNotificationPropertyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86123be9f8843d3d930f0ef4dae0419bbfe722bc60e1199098592c30395cc5c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNotifyDelayAfter")
    def reset_notify_delay_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotifyDelayAfter", []))

    @builtins.property
    @jsii.member(jsii_name="notifyDelayAfterInput")
    def notify_delay_after_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "notifyDelayAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyDelayAfter")
    def notify_delay_after(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "notifyDelayAfter"))

    @notify_delay_after.setter
    def notify_delay_after(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__013c37a803e10ee3a45c8768c829e74eea29b006320ba149d64e124fb270a908)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifyDelayAfter", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GlueJobNotificationProperty]:
        return typing.cast(typing.Optional[GlueJobNotificationProperty], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GlueJobNotificationProperty],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae5a0096fa8ddb91b5d256c4c143c21227e2616983f31cf6de9fb04bf926aff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "GlueJob",
    "GlueJobCommand",
    "GlueJobCommandOutputReference",
    "GlueJobConfig",
    "GlueJobExecutionProperty",
    "GlueJobExecutionPropertyOutputReference",
    "GlueJobNotificationProperty",
    "GlueJobNotificationPropertyOutputReference",
]

publication.publish()

def _typecheckingstub__c0983076a5a37b1adb90a2d464044a77b2fd1117d838b2804fb98c1d0d5b173e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    command: typing.Union[GlueJobCommand, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    role_arn: builtins.str,
    connections: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    execution_class: typing.Optional[builtins.str] = None,
    execution_property: typing.Optional[typing.Union[GlueJobExecutionProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    glue_version: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    max_capacity: typing.Optional[jsii.Number] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    non_overridable_arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    notification_property: typing.Optional[typing.Union[GlueJobNotificationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    number_of_workers: typing.Optional[jsii.Number] = None,
    security_configuration: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    worker_type: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d673703ec42448867a01399721901aef946957f844baab73a79889a68a8bc9e1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91704f17a0eee40be4828cadf3053d5c14695a1b80b4f344729ab05a7984c7f6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e962a6c1dbeca5d6d4b37eaf2ead162e1d0924b535c70cd81a0f3e8b077b1369(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__035895538a9bfc5916d93775d89658d94253c471e979fd49c3cf2fb6c5627b29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9573db644b3bb09df25cf85a98f721fa5a0ff1707a3ce23282d0ecddaa3e58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8e2b4a1f00e04184067d6bf979762470bcaae5c7dab296c6165aa200f3c468a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a144066e12645a65d7c4177afa9aa79456cd1f3bbe47c13293a4e8396f5807(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02072b73eef7b71ec8c5c2b6c8632b57e7a1a815e671d67dc4be01b8b5390410(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__150ade938d1bbbc493b4240934556608c145920b27488d308a3c97a35fe27617(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2491eeb74b8a3e7f101d692134a18058b2073967197c62039c159bbe60732bc8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__013ac8372401db3185f3f16a0ef44c8f5b217f309ae7c21082ea34513b1a382e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0873a7854da323eb39428cf1ecca8a01d0d406ebf3a7768abcdb5209276ccbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bf24edd9c1558d9c7ffa03e428011e1694a71e9c4f32f8a8de1b9cd9369497e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37dc6893b13503529d0d58a02077844db38432007ccc4d3e09bd3ba49e6a3b9c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c4d5862966e4efd381b24252f4f69474429efc4bcf6ad79b2bcc297c84b401(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3f0f3d3dbf2555dc4cebc59aed7734df2e863055c163b89394c1db2228b51a5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae472e0c17dfa260a9135f57ee8b4ad78f88fac97ee11ebeaaa5b4f3a03001f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a073d517d4910d8b90fc9874dce1467d15f777662fc2f465e75f206d22bc676(
    *,
    script_location: builtins.str,
    name: typing.Optional[builtins.str] = None,
    python_version: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f335ce967c912d299e87f0560b3a3affb413be392d5296a655f1cb96ea2b864(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e52cfae71ded6e5ea8c2539568479ebf6e62a6529c0ec38f3c363a44c7d8cd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5efb7f4c69c45b343860b37ebab8472a0e39beef6dfc99e4a7816eaee1adc143(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__638fe14d2e27d9f4d310021d601cde5e7b5dd8435a89dc1e18843abd90638753(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__432e2f5d742ba3e19fc82bbb3203710fb250f70b435d5b3dca7b873be9d59f75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e287cc57c754ae957d83fce548f3c1b78d30e6440defa2faf44b788e0dc1109e(
    value: typing.Optional[GlueJobCommand],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e13f1ce4a6ddc4ccfa87affe691b571f525e5f206e3a43bed54b245f739c71(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    command: typing.Union[GlueJobCommand, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    role_arn: builtins.str,
    connections: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    execution_class: typing.Optional[builtins.str] = None,
    execution_property: typing.Optional[typing.Union[GlueJobExecutionProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    glue_version: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    max_capacity: typing.Optional[jsii.Number] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    non_overridable_arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    notification_property: typing.Optional[typing.Union[GlueJobNotificationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    number_of_workers: typing.Optional[jsii.Number] = None,
    security_configuration: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    worker_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50d53cb786d387f3a2e006c67ae1fea4a9576cce50f42105fbb0ed3f8e307709(
    *,
    max_concurrent_runs: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d06995acfeb32f10fa9b80e5e7e20b78c1fce187b34127314a5416e2e4f6c0df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a85d69a5a8fb1feafa7ee4cea2c4e3965797f78b457c3a0283e4143fb5048dae(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d038b129ba4bc4f5460a93a577be2aad01cfd542b768212c61165e126417aa5d(
    value: typing.Optional[GlueJobExecutionProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d36cb48288ee3a80cdac85fe6d8c8b9c4e7edb71724edf6b9e31afad92b621(
    *,
    notify_delay_after: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86123be9f8843d3d930f0ef4dae0419bbfe722bc60e1199098592c30395cc5c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__013c37a803e10ee3a45c8768c829e74eea29b006320ba149d64e124fb270a908(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae5a0096fa8ddb91b5d256c4c143c21227e2616983f31cf6de9fb04bf926aff(
    value: typing.Optional[GlueJobNotificationProperty],
) -> None:
    """Type checking stubs"""
    pass
