'''
# `aws_sagemaker_app_image_config`

Refer to the Terraform Registory for docs: [`aws_sagemaker_app_image_config`](https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config).
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


class SagemakerAppImageConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerAppImageConfig.SagemakerAppImageConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config aws_sagemaker_app_image_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        app_image_config_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        kernel_gateway_image_config: typing.Optional[typing.Union["SagemakerAppImageConfigKernelGatewayImageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config aws_sagemaker_app_image_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param app_image_config_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#app_image_config_name SagemakerAppImageConfig#app_image_config_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#id SagemakerAppImageConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kernel_gateway_image_config: kernel_gateway_image_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#kernel_gateway_image_config SagemakerAppImageConfig#kernel_gateway_image_config}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#tags SagemakerAppImageConfig#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#tags_all SagemakerAppImageConfig#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47e71ebb87f320b8edf45907b18d48feb2bcfb13a3448299998899c9ad0091b0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SagemakerAppImageConfigConfig(
            app_image_config_name=app_image_config_name,
            id=id,
            kernel_gateway_image_config=kernel_gateway_image_config,
            tags=tags,
            tags_all=tags_all,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putKernelGatewayImageConfig")
    def put_kernel_gateway_image_config(
        self,
        *,
        kernel_spec: typing.Union["SagemakerAppImageConfigKernelGatewayImageConfigKernelSpec", typing.Dict[builtins.str, typing.Any]],
        file_system_config: typing.Optional[typing.Union["SagemakerAppImageConfigKernelGatewayImageConfigFileSystemConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param kernel_spec: kernel_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#kernel_spec SagemakerAppImageConfig#kernel_spec}
        :param file_system_config: file_system_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#file_system_config SagemakerAppImageConfig#file_system_config}
        '''
        value = SagemakerAppImageConfigKernelGatewayImageConfig(
            kernel_spec=kernel_spec, file_system_config=file_system_config
        )

        return typing.cast(None, jsii.invoke(self, "putKernelGatewayImageConfig", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKernelGatewayImageConfig")
    def reset_kernel_gateway_image_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKernelGatewayImageConfig", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

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
    @jsii.member(jsii_name="kernelGatewayImageConfig")
    def kernel_gateway_image_config(
        self,
    ) -> "SagemakerAppImageConfigKernelGatewayImageConfigOutputReference":
        return typing.cast("SagemakerAppImageConfigKernelGatewayImageConfigOutputReference", jsii.get(self, "kernelGatewayImageConfig"))

    @builtins.property
    @jsii.member(jsii_name="appImageConfigNameInput")
    def app_image_config_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appImageConfigNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kernelGatewayImageConfigInput")
    def kernel_gateway_image_config_input(
        self,
    ) -> typing.Optional["SagemakerAppImageConfigKernelGatewayImageConfig"]:
        return typing.cast(typing.Optional["SagemakerAppImageConfigKernelGatewayImageConfig"], jsii.get(self, "kernelGatewayImageConfigInput"))

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
    @jsii.member(jsii_name="appImageConfigName")
    def app_image_config_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appImageConfigName"))

    @app_image_config_name.setter
    def app_image_config_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aa1bcecb1026484cbc5c53e99075b33970052ce2781ab702c57282fc214485f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appImageConfigName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c432c5a0a963597ca67537e0c9dd1fbf698e092e0ecc60cd84f6b12746bdd681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e74290497c7166c8d33cf551e9aaa7acbd1efdabf0e4c86c004be009d38c4845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d407a7e85f717f0bc1d256f5171833f8d98336a6c057cd86e0eadd564945a76b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerAppImageConfig.SagemakerAppImageConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "app_image_config_name": "appImageConfigName",
        "id": "id",
        "kernel_gateway_image_config": "kernelGatewayImageConfig",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class SagemakerAppImageConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        app_image_config_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        kernel_gateway_image_config: typing.Optional[typing.Union["SagemakerAppImageConfigKernelGatewayImageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param app_image_config_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#app_image_config_name SagemakerAppImageConfig#app_image_config_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#id SagemakerAppImageConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kernel_gateway_image_config: kernel_gateway_image_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#kernel_gateway_image_config SagemakerAppImageConfig#kernel_gateway_image_config}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#tags SagemakerAppImageConfig#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#tags_all SagemakerAppImageConfig#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(kernel_gateway_image_config, dict):
            kernel_gateway_image_config = SagemakerAppImageConfigKernelGatewayImageConfig(**kernel_gateway_image_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__792f7702de4eec08bc5ee3e04fe204f363b37c447d7e5d34a6e0a3ea79fb097d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument app_image_config_name", value=app_image_config_name, expected_type=type_hints["app_image_config_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kernel_gateway_image_config", value=kernel_gateway_image_config, expected_type=type_hints["kernel_gateway_image_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_image_config_name": app_image_config_name,
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
        if id is not None:
            self._values["id"] = id
        if kernel_gateway_image_config is not None:
            self._values["kernel_gateway_image_config"] = kernel_gateway_image_config
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all

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
    def app_image_config_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#app_image_config_name SagemakerAppImageConfig#app_image_config_name}.'''
        result = self._values.get("app_image_config_name")
        assert result is not None, "Required property 'app_image_config_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#id SagemakerAppImageConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kernel_gateway_image_config(
        self,
    ) -> typing.Optional["SagemakerAppImageConfigKernelGatewayImageConfig"]:
        '''kernel_gateway_image_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#kernel_gateway_image_config SagemakerAppImageConfig#kernel_gateway_image_config}
        '''
        result = self._values.get("kernel_gateway_image_config")
        return typing.cast(typing.Optional["SagemakerAppImageConfigKernelGatewayImageConfig"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#tags SagemakerAppImageConfig#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#tags_all SagemakerAppImageConfig#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerAppImageConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerAppImageConfig.SagemakerAppImageConfigKernelGatewayImageConfig",
    jsii_struct_bases=[],
    name_mapping={
        "kernel_spec": "kernelSpec",
        "file_system_config": "fileSystemConfig",
    },
)
class SagemakerAppImageConfigKernelGatewayImageConfig:
    def __init__(
        self,
        *,
        kernel_spec: typing.Union["SagemakerAppImageConfigKernelGatewayImageConfigKernelSpec", typing.Dict[builtins.str, typing.Any]],
        file_system_config: typing.Optional[typing.Union["SagemakerAppImageConfigKernelGatewayImageConfigFileSystemConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param kernel_spec: kernel_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#kernel_spec SagemakerAppImageConfig#kernel_spec}
        :param file_system_config: file_system_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#file_system_config SagemakerAppImageConfig#file_system_config}
        '''
        if isinstance(kernel_spec, dict):
            kernel_spec = SagemakerAppImageConfigKernelGatewayImageConfigKernelSpec(**kernel_spec)
        if isinstance(file_system_config, dict):
            file_system_config = SagemakerAppImageConfigKernelGatewayImageConfigFileSystemConfig(**file_system_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__926d3fa289e0f6e38503a6b950f22f8b39a147bebdcd3ebef128ed9407ea026e)
            check_type(argname="argument kernel_spec", value=kernel_spec, expected_type=type_hints["kernel_spec"])
            check_type(argname="argument file_system_config", value=file_system_config, expected_type=type_hints["file_system_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kernel_spec": kernel_spec,
        }
        if file_system_config is not None:
            self._values["file_system_config"] = file_system_config

    @builtins.property
    def kernel_spec(
        self,
    ) -> "SagemakerAppImageConfigKernelGatewayImageConfigKernelSpec":
        '''kernel_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#kernel_spec SagemakerAppImageConfig#kernel_spec}
        '''
        result = self._values.get("kernel_spec")
        assert result is not None, "Required property 'kernel_spec' is missing"
        return typing.cast("SagemakerAppImageConfigKernelGatewayImageConfigKernelSpec", result)

    @builtins.property
    def file_system_config(
        self,
    ) -> typing.Optional["SagemakerAppImageConfigKernelGatewayImageConfigFileSystemConfig"]:
        '''file_system_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#file_system_config SagemakerAppImageConfig#file_system_config}
        '''
        result = self._values.get("file_system_config")
        return typing.cast(typing.Optional["SagemakerAppImageConfigKernelGatewayImageConfigFileSystemConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerAppImageConfigKernelGatewayImageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerAppImageConfig.SagemakerAppImageConfigKernelGatewayImageConfigFileSystemConfig",
    jsii_struct_bases=[],
    name_mapping={
        "default_gid": "defaultGid",
        "default_uid": "defaultUid",
        "mount_path": "mountPath",
    },
)
class SagemakerAppImageConfigKernelGatewayImageConfigFileSystemConfig:
    def __init__(
        self,
        *,
        default_gid: typing.Optional[jsii.Number] = None,
        default_uid: typing.Optional[jsii.Number] = None,
        mount_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_gid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#default_gid SagemakerAppImageConfig#default_gid}.
        :param default_uid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#default_uid SagemakerAppImageConfig#default_uid}.
        :param mount_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#mount_path SagemakerAppImageConfig#mount_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f855fa0ff41719855e3d162e64b27bac10146c3f6bf6e203e8cefe488ed621c5)
            check_type(argname="argument default_gid", value=default_gid, expected_type=type_hints["default_gid"])
            check_type(argname="argument default_uid", value=default_uid, expected_type=type_hints["default_uid"])
            check_type(argname="argument mount_path", value=mount_path, expected_type=type_hints["mount_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_gid is not None:
            self._values["default_gid"] = default_gid
        if default_uid is not None:
            self._values["default_uid"] = default_uid
        if mount_path is not None:
            self._values["mount_path"] = mount_path

    @builtins.property
    def default_gid(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#default_gid SagemakerAppImageConfig#default_gid}.'''
        result = self._values.get("default_gid")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_uid(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#default_uid SagemakerAppImageConfig#default_uid}.'''
        result = self._values.get("default_uid")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mount_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#mount_path SagemakerAppImageConfig#mount_path}.'''
        result = self._values.get("mount_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerAppImageConfigKernelGatewayImageConfigFileSystemConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerAppImageConfigKernelGatewayImageConfigFileSystemConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerAppImageConfig.SagemakerAppImageConfigKernelGatewayImageConfigFileSystemConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52713e1be1a7a697da4834b2dbe13b903111fd58cc1200434748b1746ca2f116)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDefaultGid")
    def reset_default_gid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultGid", []))

    @jsii.member(jsii_name="resetDefaultUid")
    def reset_default_uid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultUid", []))

    @jsii.member(jsii_name="resetMountPath")
    def reset_mount_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMountPath", []))

    @builtins.property
    @jsii.member(jsii_name="defaultGidInput")
    def default_gid_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultGidInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultUidInput")
    def default_uid_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultUidInput"))

    @builtins.property
    @jsii.member(jsii_name="mountPathInput")
    def mount_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mountPathInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultGid")
    def default_gid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultGid"))

    @default_gid.setter
    def default_gid(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e26171ef99bc0b6729cbf907a2cdbf658c54bd544b9027eef48c3cd8352560b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultGid", value)

    @builtins.property
    @jsii.member(jsii_name="defaultUid")
    def default_uid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultUid"))

    @default_uid.setter
    def default_uid(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7fbe17ba36f1981f3e278e885aeae026b8067503fe334592ea096f610955d25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultUid", value)

    @builtins.property
    @jsii.member(jsii_name="mountPath")
    def mount_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountPath"))

    @mount_path.setter
    def mount_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ebbe679dda15d239dcc5275dd9e8654256a505273442d47e55c9c7fdb9323ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountPath", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerAppImageConfigKernelGatewayImageConfigFileSystemConfig]:
        return typing.cast(typing.Optional[SagemakerAppImageConfigKernelGatewayImageConfigFileSystemConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerAppImageConfigKernelGatewayImageConfigFileSystemConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8083c5451c600068526eb708f8e4abe33b5b8cd48eb3be4d76cf11e6b832ffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerAppImageConfig.SagemakerAppImageConfigKernelGatewayImageConfigKernelSpec",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "display_name": "displayName"},
)
class SagemakerAppImageConfigKernelGatewayImageConfigKernelSpec:
    def __init__(
        self,
        *,
        name: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#name SagemakerAppImageConfig#name}.
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#display_name SagemakerAppImageConfig#display_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ec7570363f71ca8196ab6ffa5a1d6c0a0b9ca1903121613d0b8abd605d163e9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if display_name is not None:
            self._values["display_name"] = display_name

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#name SagemakerAppImageConfig#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#display_name SagemakerAppImageConfig#display_name}.'''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerAppImageConfigKernelGatewayImageConfigKernelSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerAppImageConfigKernelGatewayImageConfigKernelSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerAppImageConfig.SagemakerAppImageConfigKernelGatewayImageConfigKernelSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa90cc6fa78b3536430a2234d4aba53c9ff377da76f488a907a5230bb859c0b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a34ac1cbd7d63100bd28266f417d7a89962f4f7fdeb82bb819cd9ec14573f88a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7458fd4028f5e9a54467a99fedaa0eede92674fae12fbe2c4382e59c1795b92c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerAppImageConfigKernelGatewayImageConfigKernelSpec]:
        return typing.cast(typing.Optional[SagemakerAppImageConfigKernelGatewayImageConfigKernelSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerAppImageConfigKernelGatewayImageConfigKernelSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ad549453d611b6b4d84cb16e77a7fba15571fc7897dfa4a7b0110a950650eba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerAppImageConfigKernelGatewayImageConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerAppImageConfig.SagemakerAppImageConfigKernelGatewayImageConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd190f03dbf58363944e49e6151967795e9367d32e9af4db933c42d435069a3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFileSystemConfig")
    def put_file_system_config(
        self,
        *,
        default_gid: typing.Optional[jsii.Number] = None,
        default_uid: typing.Optional[jsii.Number] = None,
        mount_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_gid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#default_gid SagemakerAppImageConfig#default_gid}.
        :param default_uid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#default_uid SagemakerAppImageConfig#default_uid}.
        :param mount_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#mount_path SagemakerAppImageConfig#mount_path}.
        '''
        value = SagemakerAppImageConfigKernelGatewayImageConfigFileSystemConfig(
            default_gid=default_gid, default_uid=default_uid, mount_path=mount_path
        )

        return typing.cast(None, jsii.invoke(self, "putFileSystemConfig", [value]))

    @jsii.member(jsii_name="putKernelSpec")
    def put_kernel_spec(
        self,
        *,
        name: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#name SagemakerAppImageConfig#name}.
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/sagemaker_app_image_config#display_name SagemakerAppImageConfig#display_name}.
        '''
        value = SagemakerAppImageConfigKernelGatewayImageConfigKernelSpec(
            name=name, display_name=display_name
        )

        return typing.cast(None, jsii.invoke(self, "putKernelSpec", [value]))

    @jsii.member(jsii_name="resetFileSystemConfig")
    def reset_file_system_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileSystemConfig", []))

    @builtins.property
    @jsii.member(jsii_name="fileSystemConfig")
    def file_system_config(
        self,
    ) -> SagemakerAppImageConfigKernelGatewayImageConfigFileSystemConfigOutputReference:
        return typing.cast(SagemakerAppImageConfigKernelGatewayImageConfigFileSystemConfigOutputReference, jsii.get(self, "fileSystemConfig"))

    @builtins.property
    @jsii.member(jsii_name="kernelSpec")
    def kernel_spec(
        self,
    ) -> SagemakerAppImageConfigKernelGatewayImageConfigKernelSpecOutputReference:
        return typing.cast(SagemakerAppImageConfigKernelGatewayImageConfigKernelSpecOutputReference, jsii.get(self, "kernelSpec"))

    @builtins.property
    @jsii.member(jsii_name="fileSystemConfigInput")
    def file_system_config_input(
        self,
    ) -> typing.Optional[SagemakerAppImageConfigKernelGatewayImageConfigFileSystemConfig]:
        return typing.cast(typing.Optional[SagemakerAppImageConfigKernelGatewayImageConfigFileSystemConfig], jsii.get(self, "fileSystemConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="kernelSpecInput")
    def kernel_spec_input(
        self,
    ) -> typing.Optional[SagemakerAppImageConfigKernelGatewayImageConfigKernelSpec]:
        return typing.cast(typing.Optional[SagemakerAppImageConfigKernelGatewayImageConfigKernelSpec], jsii.get(self, "kernelSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerAppImageConfigKernelGatewayImageConfig]:
        return typing.cast(typing.Optional[SagemakerAppImageConfigKernelGatewayImageConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerAppImageConfigKernelGatewayImageConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a3a94441a609ee8a4ed837a62eb93f759472d6ceb7aa17d58b527ee2b5e21db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "SagemakerAppImageConfig",
    "SagemakerAppImageConfigConfig",
    "SagemakerAppImageConfigKernelGatewayImageConfig",
    "SagemakerAppImageConfigKernelGatewayImageConfigFileSystemConfig",
    "SagemakerAppImageConfigKernelGatewayImageConfigFileSystemConfigOutputReference",
    "SagemakerAppImageConfigKernelGatewayImageConfigKernelSpec",
    "SagemakerAppImageConfigKernelGatewayImageConfigKernelSpecOutputReference",
    "SagemakerAppImageConfigKernelGatewayImageConfigOutputReference",
]

publication.publish()

def _typecheckingstub__47e71ebb87f320b8edf45907b18d48feb2bcfb13a3448299998899c9ad0091b0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    app_image_config_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    kernel_gateway_image_config: typing.Optional[typing.Union[SagemakerAppImageConfigKernelGatewayImageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__0aa1bcecb1026484cbc5c53e99075b33970052ce2781ab702c57282fc214485f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c432c5a0a963597ca67537e0c9dd1fbf698e092e0ecc60cd84f6b12746bdd681(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e74290497c7166c8d33cf551e9aaa7acbd1efdabf0e4c86c004be009d38c4845(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d407a7e85f717f0bc1d256f5171833f8d98336a6c057cd86e0eadd564945a76b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__792f7702de4eec08bc5ee3e04fe204f363b37c447d7e5d34a6e0a3ea79fb097d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    app_image_config_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    kernel_gateway_image_config: typing.Optional[typing.Union[SagemakerAppImageConfigKernelGatewayImageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__926d3fa289e0f6e38503a6b950f22f8b39a147bebdcd3ebef128ed9407ea026e(
    *,
    kernel_spec: typing.Union[SagemakerAppImageConfigKernelGatewayImageConfigKernelSpec, typing.Dict[builtins.str, typing.Any]],
    file_system_config: typing.Optional[typing.Union[SagemakerAppImageConfigKernelGatewayImageConfigFileSystemConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f855fa0ff41719855e3d162e64b27bac10146c3f6bf6e203e8cefe488ed621c5(
    *,
    default_gid: typing.Optional[jsii.Number] = None,
    default_uid: typing.Optional[jsii.Number] = None,
    mount_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52713e1be1a7a697da4834b2dbe13b903111fd58cc1200434748b1746ca2f116(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e26171ef99bc0b6729cbf907a2cdbf658c54bd544b9027eef48c3cd8352560b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7fbe17ba36f1981f3e278e885aeae026b8067503fe334592ea096f610955d25(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ebbe679dda15d239dcc5275dd9e8654256a505273442d47e55c9c7fdb9323ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8083c5451c600068526eb708f8e4abe33b5b8cd48eb3be4d76cf11e6b832ffa(
    value: typing.Optional[SagemakerAppImageConfigKernelGatewayImageConfigFileSystemConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ec7570363f71ca8196ab6ffa5a1d6c0a0b9ca1903121613d0b8abd605d163e9(
    *,
    name: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa90cc6fa78b3536430a2234d4aba53c9ff377da76f488a907a5230bb859c0b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34ac1cbd7d63100bd28266f417d7a89962f4f7fdeb82bb819cd9ec14573f88a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7458fd4028f5e9a54467a99fedaa0eede92674fae12fbe2c4382e59c1795b92c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ad549453d611b6b4d84cb16e77a7fba15571fc7897dfa4a7b0110a950650eba(
    value: typing.Optional[SagemakerAppImageConfigKernelGatewayImageConfigKernelSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd190f03dbf58363944e49e6151967795e9367d32e9af4db933c42d435069a3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a3a94441a609ee8a4ed837a62eb93f759472d6ceb7aa17d58b527ee2b5e21db(
    value: typing.Optional[SagemakerAppImageConfigKernelGatewayImageConfig],
) -> None:
    """Type checking stubs"""
    pass
