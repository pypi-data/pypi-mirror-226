'''
# `aws_lb_listener`

Refer to the Terraform Registory for docs: [`aws_lb_listener`](https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener).
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


class LbListener(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lbListener.LbListener",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener aws_lb_listener}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        default_action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LbListenerDefaultAction", typing.Dict[builtins.str, typing.Any]]]],
        load_balancer_arn: builtins.str,
        alpn_policy: typing.Optional[builtins.str] = None,
        certificate_arn: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
        ssl_policy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["LbListenerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener aws_lb_listener} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param default_action: default_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#default_action LbListener#default_action}
        :param load_balancer_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#load_balancer_arn LbListener#load_balancer_arn}.
        :param alpn_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#alpn_policy LbListener#alpn_policy}.
        :param certificate_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#certificate_arn LbListener#certificate_arn}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#id LbListener#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#port LbListener#port}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#protocol LbListener#protocol}.
        :param ssl_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#ssl_policy LbListener#ssl_policy}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#tags LbListener#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#tags_all LbListener#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#timeouts LbListener#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e05f9c031e1db2706dcfe3b4556e44f5c3e75642d2ab0be31c5f0e4273bad93)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LbListenerConfig(
            default_action=default_action,
            load_balancer_arn=load_balancer_arn,
            alpn_policy=alpn_policy,
            certificate_arn=certificate_arn,
            id=id,
            port=port,
            protocol=protocol,
            ssl_policy=ssl_policy,
            tags=tags,
            tags_all=tags_all,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putDefaultAction")
    def put_default_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LbListenerDefaultAction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07952a1a8fb697491ad46974796b0f5db51120cdb230f5265b9a047588242e50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDefaultAction", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(self, *, read: typing.Optional[builtins.str] = None) -> None:
        '''
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#read LbListener#read}.
        '''
        value = LbListenerTimeouts(read=read)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAlpnPolicy")
    def reset_alpn_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlpnPolicy", []))

    @jsii.member(jsii_name="resetCertificateArn")
    def reset_certificate_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateArn", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetSslPolicy")
    def reset_ssl_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslPolicy", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="defaultAction")
    def default_action(self) -> "LbListenerDefaultActionList":
        return typing.cast("LbListenerDefaultActionList", jsii.get(self, "defaultAction"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "LbListenerTimeoutsOutputReference":
        return typing.cast("LbListenerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="alpnPolicyInput")
    def alpn_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alpnPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateArnInput")
    def certificate_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateArnInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultActionInput")
    def default_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LbListenerDefaultAction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LbListenerDefaultAction"]]], jsii.get(self, "defaultActionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerArnInput")
    def load_balancer_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancerArnInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="sslPolicyInput")
    def ssl_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslPolicyInput"))

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
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LbListenerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LbListenerTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="alpnPolicy")
    def alpn_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alpnPolicy"))

    @alpn_policy.setter
    def alpn_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2342b47a81580b4b42811f77f8cb0922118259bec9c23c495b20e832daf5f7bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alpnPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateArn"))

    @certificate_arn.setter
    def certificate_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be09bbacab395102713596a51a4f4f230188bb3f18194596dacd5892cfda25ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateArn", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4961ea0372c39fbc5d8a6c295bd5d8a94e9c3f20c1aa62b009a30d3bb5cce8e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerArn"))

    @load_balancer_arn.setter
    def load_balancer_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1e464cc333c8727720158eb312a7abc0aff4a07cc2331ede0a2d6661b93081f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerArn", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__938fecbd77628b8318619b71bef7aed9f775c38d25058078cb5a89179ebaa5ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be1335717b4a1c12d11f296111a26fa2b556af88fd82b6d1aa57802d1e251b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="sslPolicy")
    def ssl_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslPolicy"))

    @ssl_policy.setter
    def ssl_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60537b1272b8503fbf708018a7b23fb5a018487579a0ad41756f20133f9f7b13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce5caed2d49e715e74cd8eaaaf79b1922b386518366ccc2c26fcd74d53bb2d21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7af321ceb45b673a68c5a16584cc67e079ba03a404930ab679d4f5de827d3ef3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lbListener.LbListenerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "default_action": "defaultAction",
        "load_balancer_arn": "loadBalancerArn",
        "alpn_policy": "alpnPolicy",
        "certificate_arn": "certificateArn",
        "id": "id",
        "port": "port",
        "protocol": "protocol",
        "ssl_policy": "sslPolicy",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
    },
)
class LbListenerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        default_action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LbListenerDefaultAction", typing.Dict[builtins.str, typing.Any]]]],
        load_balancer_arn: builtins.str,
        alpn_policy: typing.Optional[builtins.str] = None,
        certificate_arn: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
        ssl_policy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["LbListenerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param default_action: default_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#default_action LbListener#default_action}
        :param load_balancer_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#load_balancer_arn LbListener#load_balancer_arn}.
        :param alpn_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#alpn_policy LbListener#alpn_policy}.
        :param certificate_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#certificate_arn LbListener#certificate_arn}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#id LbListener#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#port LbListener#port}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#protocol LbListener#protocol}.
        :param ssl_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#ssl_policy LbListener#ssl_policy}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#tags LbListener#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#tags_all LbListener#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#timeouts LbListener#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = LbListenerTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a9cb2ead8a3e1523913faf81dedc14718a024fb9e7458cf0efc1b06ac86fd77)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument default_action", value=default_action, expected_type=type_hints["default_action"])
            check_type(argname="argument load_balancer_arn", value=load_balancer_arn, expected_type=type_hints["load_balancer_arn"])
            check_type(argname="argument alpn_policy", value=alpn_policy, expected_type=type_hints["alpn_policy"])
            check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument ssl_policy", value=ssl_policy, expected_type=type_hints["ssl_policy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_action": default_action,
            "load_balancer_arn": load_balancer_arn,
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
        if alpn_policy is not None:
            self._values["alpn_policy"] = alpn_policy
        if certificate_arn is not None:
            self._values["certificate_arn"] = certificate_arn
        if id is not None:
            self._values["id"] = id
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def default_action(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LbListenerDefaultAction"]]:
        '''default_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#default_action LbListener#default_action}
        '''
        result = self._values.get("default_action")
        assert result is not None, "Required property 'default_action' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LbListenerDefaultAction"]], result)

    @builtins.property
    def load_balancer_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#load_balancer_arn LbListener#load_balancer_arn}.'''
        result = self._values.get("load_balancer_arn")
        assert result is not None, "Required property 'load_balancer_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alpn_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#alpn_policy LbListener#alpn_policy}.'''
        result = self._values.get("alpn_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#certificate_arn LbListener#certificate_arn}.'''
        result = self._values.get("certificate_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#id LbListener#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#port LbListener#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#protocol LbListener#protocol}.'''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#ssl_policy LbListener#ssl_policy}.'''
        result = self._values.get("ssl_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#tags LbListener#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#tags_all LbListener#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["LbListenerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#timeouts LbListener#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["LbListenerTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbListenerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lbListener.LbListenerDefaultAction",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "authenticate_cognito": "authenticateCognito",
        "authenticate_oidc": "authenticateOidc",
        "fixed_response": "fixedResponse",
        "forward": "forward",
        "order": "order",
        "redirect": "redirect",
        "target_group_arn": "targetGroupArn",
    },
)
class LbListenerDefaultAction:
    def __init__(
        self,
        *,
        type: builtins.str,
        authenticate_cognito: typing.Optional[typing.Union["LbListenerDefaultActionAuthenticateCognito", typing.Dict[builtins.str, typing.Any]]] = None,
        authenticate_oidc: typing.Optional[typing.Union["LbListenerDefaultActionAuthenticateOidc", typing.Dict[builtins.str, typing.Any]]] = None,
        fixed_response: typing.Optional[typing.Union["LbListenerDefaultActionFixedResponse", typing.Dict[builtins.str, typing.Any]]] = None,
        forward: typing.Optional[typing.Union["LbListenerDefaultActionForward", typing.Dict[builtins.str, typing.Any]]] = None,
        order: typing.Optional[jsii.Number] = None,
        redirect: typing.Optional[typing.Union["LbListenerDefaultActionRedirect", typing.Dict[builtins.str, typing.Any]]] = None,
        target_group_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#type LbListener#type}.
        :param authenticate_cognito: authenticate_cognito block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#authenticate_cognito LbListener#authenticate_cognito}
        :param authenticate_oidc: authenticate_oidc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#authenticate_oidc LbListener#authenticate_oidc}
        :param fixed_response: fixed_response block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#fixed_response LbListener#fixed_response}
        :param forward: forward block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#forward LbListener#forward}
        :param order: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#order LbListener#order}.
        :param redirect: redirect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#redirect LbListener#redirect}
        :param target_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#target_group_arn LbListener#target_group_arn}.
        '''
        if isinstance(authenticate_cognito, dict):
            authenticate_cognito = LbListenerDefaultActionAuthenticateCognito(**authenticate_cognito)
        if isinstance(authenticate_oidc, dict):
            authenticate_oidc = LbListenerDefaultActionAuthenticateOidc(**authenticate_oidc)
        if isinstance(fixed_response, dict):
            fixed_response = LbListenerDefaultActionFixedResponse(**fixed_response)
        if isinstance(forward, dict):
            forward = LbListenerDefaultActionForward(**forward)
        if isinstance(redirect, dict):
            redirect = LbListenerDefaultActionRedirect(**redirect)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3face0812180d37cd8274fe0b875786d8e41acab2f0fc57ce5925adf9384829)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument authenticate_cognito", value=authenticate_cognito, expected_type=type_hints["authenticate_cognito"])
            check_type(argname="argument authenticate_oidc", value=authenticate_oidc, expected_type=type_hints["authenticate_oidc"])
            check_type(argname="argument fixed_response", value=fixed_response, expected_type=type_hints["fixed_response"])
            check_type(argname="argument forward", value=forward, expected_type=type_hints["forward"])
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
            check_type(argname="argument redirect", value=redirect, expected_type=type_hints["redirect"])
            check_type(argname="argument target_group_arn", value=target_group_arn, expected_type=type_hints["target_group_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if authenticate_cognito is not None:
            self._values["authenticate_cognito"] = authenticate_cognito
        if authenticate_oidc is not None:
            self._values["authenticate_oidc"] = authenticate_oidc
        if fixed_response is not None:
            self._values["fixed_response"] = fixed_response
        if forward is not None:
            self._values["forward"] = forward
        if order is not None:
            self._values["order"] = order
        if redirect is not None:
            self._values["redirect"] = redirect
        if target_group_arn is not None:
            self._values["target_group_arn"] = target_group_arn

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#type LbListener#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authenticate_cognito(
        self,
    ) -> typing.Optional["LbListenerDefaultActionAuthenticateCognito"]:
        '''authenticate_cognito block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#authenticate_cognito LbListener#authenticate_cognito}
        '''
        result = self._values.get("authenticate_cognito")
        return typing.cast(typing.Optional["LbListenerDefaultActionAuthenticateCognito"], result)

    @builtins.property
    def authenticate_oidc(
        self,
    ) -> typing.Optional["LbListenerDefaultActionAuthenticateOidc"]:
        '''authenticate_oidc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#authenticate_oidc LbListener#authenticate_oidc}
        '''
        result = self._values.get("authenticate_oidc")
        return typing.cast(typing.Optional["LbListenerDefaultActionAuthenticateOidc"], result)

    @builtins.property
    def fixed_response(self) -> typing.Optional["LbListenerDefaultActionFixedResponse"]:
        '''fixed_response block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#fixed_response LbListener#fixed_response}
        '''
        result = self._values.get("fixed_response")
        return typing.cast(typing.Optional["LbListenerDefaultActionFixedResponse"], result)

    @builtins.property
    def forward(self) -> typing.Optional["LbListenerDefaultActionForward"]:
        '''forward block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#forward LbListener#forward}
        '''
        result = self._values.get("forward")
        return typing.cast(typing.Optional["LbListenerDefaultActionForward"], result)

    @builtins.property
    def order(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#order LbListener#order}.'''
        result = self._values.get("order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def redirect(self) -> typing.Optional["LbListenerDefaultActionRedirect"]:
        '''redirect block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#redirect LbListener#redirect}
        '''
        result = self._values.get("redirect")
        return typing.cast(typing.Optional["LbListenerDefaultActionRedirect"], result)

    @builtins.property
    def target_group_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#target_group_arn LbListener#target_group_arn}.'''
        result = self._values.get("target_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbListenerDefaultAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lbListener.LbListenerDefaultActionAuthenticateCognito",
    jsii_struct_bases=[],
    name_mapping={
        "user_pool_arn": "userPoolArn",
        "user_pool_client_id": "userPoolClientId",
        "user_pool_domain": "userPoolDomain",
        "authentication_request_extra_params": "authenticationRequestExtraParams",
        "on_unauthenticated_request": "onUnauthenticatedRequest",
        "scope": "scope",
        "session_cookie_name": "sessionCookieName",
        "session_timeout": "sessionTimeout",
    },
)
class LbListenerDefaultActionAuthenticateCognito:
    def __init__(
        self,
        *,
        user_pool_arn: builtins.str,
        user_pool_client_id: builtins.str,
        user_pool_domain: builtins.str,
        authentication_request_extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        on_unauthenticated_request: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        session_cookie_name: typing.Optional[builtins.str] = None,
        session_timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param user_pool_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#user_pool_arn LbListener#user_pool_arn}.
        :param user_pool_client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#user_pool_client_id LbListener#user_pool_client_id}.
        :param user_pool_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#user_pool_domain LbListener#user_pool_domain}.
        :param authentication_request_extra_params: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#authentication_request_extra_params LbListener#authentication_request_extra_params}.
        :param on_unauthenticated_request: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#on_unauthenticated_request LbListener#on_unauthenticated_request}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#scope LbListener#scope}.
        :param session_cookie_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#session_cookie_name LbListener#session_cookie_name}.
        :param session_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#session_timeout LbListener#session_timeout}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__095766fa2e6f31689406b03429dcfaac15c3983d65d5d565c230b5899ef2d6e2)
            check_type(argname="argument user_pool_arn", value=user_pool_arn, expected_type=type_hints["user_pool_arn"])
            check_type(argname="argument user_pool_client_id", value=user_pool_client_id, expected_type=type_hints["user_pool_client_id"])
            check_type(argname="argument user_pool_domain", value=user_pool_domain, expected_type=type_hints["user_pool_domain"])
            check_type(argname="argument authentication_request_extra_params", value=authentication_request_extra_params, expected_type=type_hints["authentication_request_extra_params"])
            check_type(argname="argument on_unauthenticated_request", value=on_unauthenticated_request, expected_type=type_hints["on_unauthenticated_request"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument session_cookie_name", value=session_cookie_name, expected_type=type_hints["session_cookie_name"])
            check_type(argname="argument session_timeout", value=session_timeout, expected_type=type_hints["session_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_pool_arn": user_pool_arn,
            "user_pool_client_id": user_pool_client_id,
            "user_pool_domain": user_pool_domain,
        }
        if authentication_request_extra_params is not None:
            self._values["authentication_request_extra_params"] = authentication_request_extra_params
        if on_unauthenticated_request is not None:
            self._values["on_unauthenticated_request"] = on_unauthenticated_request
        if scope is not None:
            self._values["scope"] = scope
        if session_cookie_name is not None:
            self._values["session_cookie_name"] = session_cookie_name
        if session_timeout is not None:
            self._values["session_timeout"] = session_timeout

    @builtins.property
    def user_pool_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#user_pool_arn LbListener#user_pool_arn}.'''
        result = self._values.get("user_pool_arn")
        assert result is not None, "Required property 'user_pool_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_pool_client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#user_pool_client_id LbListener#user_pool_client_id}.'''
        result = self._values.get("user_pool_client_id")
        assert result is not None, "Required property 'user_pool_client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_pool_domain(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#user_pool_domain LbListener#user_pool_domain}.'''
        result = self._values.get("user_pool_domain")
        assert result is not None, "Required property 'user_pool_domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication_request_extra_params(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#authentication_request_extra_params LbListener#authentication_request_extra_params}.'''
        result = self._values.get("authentication_request_extra_params")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def on_unauthenticated_request(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#on_unauthenticated_request LbListener#on_unauthenticated_request}.'''
        result = self._values.get("on_unauthenticated_request")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#scope LbListener#scope}.'''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_cookie_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#session_cookie_name LbListener#session_cookie_name}.'''
        result = self._values.get("session_cookie_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#session_timeout LbListener#session_timeout}.'''
        result = self._values.get("session_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbListenerDefaultActionAuthenticateCognito(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LbListenerDefaultActionAuthenticateCognitoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lbListener.LbListenerDefaultActionAuthenticateCognitoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36427a8405cd0e22e20a8ec220dc3aa2a2cde29bc8d86fa638b8c4c8d7aa3974)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthenticationRequestExtraParams")
    def reset_authentication_request_extra_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationRequestExtraParams", []))

    @jsii.member(jsii_name="resetOnUnauthenticatedRequest")
    def reset_on_unauthenticated_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnUnauthenticatedRequest", []))

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @jsii.member(jsii_name="resetSessionCookieName")
    def reset_session_cookie_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionCookieName", []))

    @jsii.member(jsii_name="resetSessionTimeout")
    def reset_session_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="authenticationRequestExtraParamsInput")
    def authentication_request_extra_params_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "authenticationRequestExtraParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="onUnauthenticatedRequestInput")
    def on_unauthenticated_request_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onUnauthenticatedRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionCookieNameInput")
    def session_cookie_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionCookieNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionTimeoutInput")
    def session_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="userPoolArnInput")
    def user_pool_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPoolArnInput"))

    @builtins.property
    @jsii.member(jsii_name="userPoolClientIdInput")
    def user_pool_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPoolClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="userPoolDomainInput")
    def user_pool_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPoolDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationRequestExtraParams")
    def authentication_request_extra_params(
        self,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "authenticationRequestExtraParams"))

    @authentication_request_extra_params.setter
    def authentication_request_extra_params(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0e9b12f6b8eca4686871d620f3392f216c3688903b733c37faf302082a330a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationRequestExtraParams", value)

    @builtins.property
    @jsii.member(jsii_name="onUnauthenticatedRequest")
    def on_unauthenticated_request(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onUnauthenticatedRequest"))

    @on_unauthenticated_request.setter
    def on_unauthenticated_request(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f893d90b51e9151426e4fe723c7cff028eeb207282ca1e352445365c7c3787eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onUnauthenticatedRequest", value)

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6845de12a3f3427c83d62021eea28bc86ee571eecfd3d9ef03122f5852be66d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value)

    @builtins.property
    @jsii.member(jsii_name="sessionCookieName")
    def session_cookie_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionCookieName"))

    @session_cookie_name.setter
    def session_cookie_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79d4b7f3c289d1ea4db7ea885388407422a9db279229b7a729632e1c863a4108)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionCookieName", value)

    @builtins.property
    @jsii.member(jsii_name="sessionTimeout")
    def session_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionTimeout"))

    @session_timeout.setter
    def session_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cadf625aebff884fb2e16306eacb7247b8f5307af052390c27962f91b02636c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="userPoolArn")
    def user_pool_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPoolArn"))

    @user_pool_arn.setter
    def user_pool_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f33b6993992f07fe55b66be2980fb8210418f3d4939229486cc2a70c0dc75ec9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPoolArn", value)

    @builtins.property
    @jsii.member(jsii_name="userPoolClientId")
    def user_pool_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPoolClientId"))

    @user_pool_client_id.setter
    def user_pool_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90bd4271bf62bac602c3d438511894f9658672463ed2aa156bf3855948444f76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPoolClientId", value)

    @builtins.property
    @jsii.member(jsii_name="userPoolDomain")
    def user_pool_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPoolDomain"))

    @user_pool_domain.setter
    def user_pool_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dd39c7cad48cc6aeef95f48a93e459cac17a22d8cb5b052293b181cff4ce866)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPoolDomain", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LbListenerDefaultActionAuthenticateCognito]:
        return typing.cast(typing.Optional[LbListenerDefaultActionAuthenticateCognito], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LbListenerDefaultActionAuthenticateCognito],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc3756598e296bd1b1fd3c0160cc221217ba9d5afb873e368ef9231035a0cb07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lbListener.LbListenerDefaultActionAuthenticateOidc",
    jsii_struct_bases=[],
    name_mapping={
        "authorization_endpoint": "authorizationEndpoint",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "issuer": "issuer",
        "token_endpoint": "tokenEndpoint",
        "user_info_endpoint": "userInfoEndpoint",
        "authentication_request_extra_params": "authenticationRequestExtraParams",
        "on_unauthenticated_request": "onUnauthenticatedRequest",
        "scope": "scope",
        "session_cookie_name": "sessionCookieName",
        "session_timeout": "sessionTimeout",
    },
)
class LbListenerDefaultActionAuthenticateOidc:
    def __init__(
        self,
        *,
        authorization_endpoint: builtins.str,
        client_id: builtins.str,
        client_secret: builtins.str,
        issuer: builtins.str,
        token_endpoint: builtins.str,
        user_info_endpoint: builtins.str,
        authentication_request_extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        on_unauthenticated_request: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        session_cookie_name: typing.Optional[builtins.str] = None,
        session_timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param authorization_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#authorization_endpoint LbListener#authorization_endpoint}.
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#client_id LbListener#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#client_secret LbListener#client_secret}.
        :param issuer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#issuer LbListener#issuer}.
        :param token_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#token_endpoint LbListener#token_endpoint}.
        :param user_info_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#user_info_endpoint LbListener#user_info_endpoint}.
        :param authentication_request_extra_params: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#authentication_request_extra_params LbListener#authentication_request_extra_params}.
        :param on_unauthenticated_request: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#on_unauthenticated_request LbListener#on_unauthenticated_request}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#scope LbListener#scope}.
        :param session_cookie_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#session_cookie_name LbListener#session_cookie_name}.
        :param session_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#session_timeout LbListener#session_timeout}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f03f7b8b895017730827726386876781f0bc83cd89af750517ff6e8a47fbd91)
            check_type(argname="argument authorization_endpoint", value=authorization_endpoint, expected_type=type_hints["authorization_endpoint"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
            check_type(argname="argument token_endpoint", value=token_endpoint, expected_type=type_hints["token_endpoint"])
            check_type(argname="argument user_info_endpoint", value=user_info_endpoint, expected_type=type_hints["user_info_endpoint"])
            check_type(argname="argument authentication_request_extra_params", value=authentication_request_extra_params, expected_type=type_hints["authentication_request_extra_params"])
            check_type(argname="argument on_unauthenticated_request", value=on_unauthenticated_request, expected_type=type_hints["on_unauthenticated_request"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument session_cookie_name", value=session_cookie_name, expected_type=type_hints["session_cookie_name"])
            check_type(argname="argument session_timeout", value=session_timeout, expected_type=type_hints["session_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorization_endpoint": authorization_endpoint,
            "client_id": client_id,
            "client_secret": client_secret,
            "issuer": issuer,
            "token_endpoint": token_endpoint,
            "user_info_endpoint": user_info_endpoint,
        }
        if authentication_request_extra_params is not None:
            self._values["authentication_request_extra_params"] = authentication_request_extra_params
        if on_unauthenticated_request is not None:
            self._values["on_unauthenticated_request"] = on_unauthenticated_request
        if scope is not None:
            self._values["scope"] = scope
        if session_cookie_name is not None:
            self._values["session_cookie_name"] = session_cookie_name
        if session_timeout is not None:
            self._values["session_timeout"] = session_timeout

    @builtins.property
    def authorization_endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#authorization_endpoint LbListener#authorization_endpoint}.'''
        result = self._values.get("authorization_endpoint")
        assert result is not None, "Required property 'authorization_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#client_id LbListener#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#client_secret LbListener#client_secret}.'''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def issuer(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#issuer LbListener#issuer}.'''
        result = self._values.get("issuer")
        assert result is not None, "Required property 'issuer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token_endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#token_endpoint LbListener#token_endpoint}.'''
        result = self._values.get("token_endpoint")
        assert result is not None, "Required property 'token_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_info_endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#user_info_endpoint LbListener#user_info_endpoint}.'''
        result = self._values.get("user_info_endpoint")
        assert result is not None, "Required property 'user_info_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication_request_extra_params(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#authentication_request_extra_params LbListener#authentication_request_extra_params}.'''
        result = self._values.get("authentication_request_extra_params")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def on_unauthenticated_request(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#on_unauthenticated_request LbListener#on_unauthenticated_request}.'''
        result = self._values.get("on_unauthenticated_request")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#scope LbListener#scope}.'''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_cookie_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#session_cookie_name LbListener#session_cookie_name}.'''
        result = self._values.get("session_cookie_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#session_timeout LbListener#session_timeout}.'''
        result = self._values.get("session_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbListenerDefaultActionAuthenticateOidc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LbListenerDefaultActionAuthenticateOidcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lbListener.LbListenerDefaultActionAuthenticateOidcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b492e094ad4f10f8519827362a3aaa77bba8cf2458d5242758dadbeb71846df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthenticationRequestExtraParams")
    def reset_authentication_request_extra_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationRequestExtraParams", []))

    @jsii.member(jsii_name="resetOnUnauthenticatedRequest")
    def reset_on_unauthenticated_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnUnauthenticatedRequest", []))

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @jsii.member(jsii_name="resetSessionCookieName")
    def reset_session_cookie_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionCookieName", []))

    @jsii.member(jsii_name="resetSessionTimeout")
    def reset_session_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="authenticationRequestExtraParamsInput")
    def authentication_request_extra_params_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "authenticationRequestExtraParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationEndpointInput")
    def authorization_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerInput")
    def issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerInput"))

    @builtins.property
    @jsii.member(jsii_name="onUnauthenticatedRequestInput")
    def on_unauthenticated_request_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onUnauthenticatedRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionCookieNameInput")
    def session_cookie_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionCookieNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionTimeoutInput")
    def session_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenEndpointInput")
    def token_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="userInfoEndpointInput")
    def user_info_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInfoEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationRequestExtraParams")
    def authentication_request_extra_params(
        self,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "authenticationRequestExtraParams"))

    @authentication_request_extra_params.setter
    def authentication_request_extra_params(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceb155cfe8f0b586c356c7d406678e7df645b8ca41bd1514924389ac044883d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationRequestExtraParams", value)

    @builtins.property
    @jsii.member(jsii_name="authorizationEndpoint")
    def authorization_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationEndpoint"))

    @authorization_endpoint.setter
    def authorization_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e83dd5171f43a544d6298baaea5ddd5c50be890e4206c6cf6b6e682e880beba4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe795009eb0676ae6c333ffd6c55d354a4b6ec77201bd5a3b16d0722755dedc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__212e1f828616515320f313026d440ce3126fdbfa6bc5ce5cd8e17dfabbff6f6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value)

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @issuer.setter
    def issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61c099af595a427c0996199f4341e2db993505f30dc549a3d9ca814a6b8be74d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuer", value)

    @builtins.property
    @jsii.member(jsii_name="onUnauthenticatedRequest")
    def on_unauthenticated_request(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onUnauthenticatedRequest"))

    @on_unauthenticated_request.setter
    def on_unauthenticated_request(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a043d0012c9ba9ef1d5ade6509aab3fbdaae94bec7f68be1f74d70e1b39466a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onUnauthenticatedRequest", value)

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__472e173443c892f47073ae197cc2759d47bbd5045c620621137d5b3e799d8846)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value)

    @builtins.property
    @jsii.member(jsii_name="sessionCookieName")
    def session_cookie_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionCookieName"))

    @session_cookie_name.setter
    def session_cookie_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d1ca2635ddf7cd7a0b64b89ee4c952ccec9f1b9a90a8f7003e009ba1b522efc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionCookieName", value)

    @builtins.property
    @jsii.member(jsii_name="sessionTimeout")
    def session_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionTimeout"))

    @session_timeout.setter
    def session_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d2b4f603ab0c9f8f750b80131ae8e6566918ffd168e2c757e9bd3c72a4ce87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="tokenEndpoint")
    def token_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenEndpoint"))

    @token_endpoint.setter
    def token_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86fa58911889e072edcb5acd16ab5c420a300325d66426fe6be9c4e3430c2193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="userInfoEndpoint")
    def user_info_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userInfoEndpoint"))

    @user_info_endpoint.setter
    def user_info_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40e96845f3c354429cb5548d006ba2815b72c6a63ad848f68cbbcf143631d37d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userInfoEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LbListenerDefaultActionAuthenticateOidc]:
        return typing.cast(typing.Optional[LbListenerDefaultActionAuthenticateOidc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LbListenerDefaultActionAuthenticateOidc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6833fe9fc4a284f3e46f247b73a8428580c9da8ebc311b2b6a88f57cb10eafe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lbListener.LbListenerDefaultActionFixedResponse",
    jsii_struct_bases=[],
    name_mapping={
        "content_type": "contentType",
        "message_body": "messageBody",
        "status_code": "statusCode",
    },
)
class LbListenerDefaultActionFixedResponse:
    def __init__(
        self,
        *,
        content_type: builtins.str,
        message_body: typing.Optional[builtins.str] = None,
        status_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#content_type LbListener#content_type}.
        :param message_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#message_body LbListener#message_body}.
        :param status_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#status_code LbListener#status_code}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23014c7a7f68dcabada65bee01e0f37ca8a0d62132d5abf68c7b335f6e3e745f)
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument message_body", value=message_body, expected_type=type_hints["message_body"])
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content_type": content_type,
        }
        if message_body is not None:
            self._values["message_body"] = message_body
        if status_code is not None:
            self._values["status_code"] = status_code

    @builtins.property
    def content_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#content_type LbListener#content_type}.'''
        result = self._values.get("content_type")
        assert result is not None, "Required property 'content_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def message_body(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#message_body LbListener#message_body}.'''
        result = self._values.get("message_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#status_code LbListener#status_code}.'''
        result = self._values.get("status_code")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbListenerDefaultActionFixedResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LbListenerDefaultActionFixedResponseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lbListener.LbListenerDefaultActionFixedResponseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d8b3b4e4fb1cd87c73d3a360c1458b8411f24c9beb4cc2b1db35defe3028c46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMessageBody")
    def reset_message_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageBody", []))

    @jsii.member(jsii_name="resetStatusCode")
    def reset_status_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatusCode", []))

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="messageBodyInput")
    def message_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="statusCodeInput")
    def status_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__286c2a654f4f12ef143ca0087c463e4dd15c8c61d78d8c3fc8a4c2cf2900f109)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value)

    @builtins.property
    @jsii.member(jsii_name="messageBody")
    def message_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageBody"))

    @message_body.setter
    def message_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e83b975cbaa5628ead906a47e3e7bf555eef3a3b1b9ff71c2cff489db3de791)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageBody", value)

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusCode"))

    @status_code.setter
    def status_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dfb7020a477167cd50e2d3f935a694ae639024a360343942eceb286da12e0e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusCode", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LbListenerDefaultActionFixedResponse]:
        return typing.cast(typing.Optional[LbListenerDefaultActionFixedResponse], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LbListenerDefaultActionFixedResponse],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa82b680b9ef16cd128f64c6099351727e287a8cecd438b9ffcb8fae1bd04595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lbListener.LbListenerDefaultActionForward",
    jsii_struct_bases=[],
    name_mapping={"target_group": "targetGroup", "stickiness": "stickiness"},
)
class LbListenerDefaultActionForward:
    def __init__(
        self,
        *,
        target_group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LbListenerDefaultActionForwardTargetGroup", typing.Dict[builtins.str, typing.Any]]]],
        stickiness: typing.Optional[typing.Union["LbListenerDefaultActionForwardStickiness", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param target_group: target_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#target_group LbListener#target_group}
        :param stickiness: stickiness block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#stickiness LbListener#stickiness}
        '''
        if isinstance(stickiness, dict):
            stickiness = LbListenerDefaultActionForwardStickiness(**stickiness)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__316fd60f78368b0f63f89a55f4c066026e4602de7ea4a9e09f3c270561e5e60c)
            check_type(argname="argument target_group", value=target_group, expected_type=type_hints["target_group"])
            check_type(argname="argument stickiness", value=stickiness, expected_type=type_hints["stickiness"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_group": target_group,
        }
        if stickiness is not None:
            self._values["stickiness"] = stickiness

    @builtins.property
    def target_group(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LbListenerDefaultActionForwardTargetGroup"]]:
        '''target_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#target_group LbListener#target_group}
        '''
        result = self._values.get("target_group")
        assert result is not None, "Required property 'target_group' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LbListenerDefaultActionForwardTargetGroup"]], result)

    @builtins.property
    def stickiness(self) -> typing.Optional["LbListenerDefaultActionForwardStickiness"]:
        '''stickiness block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#stickiness LbListener#stickiness}
        '''
        result = self._values.get("stickiness")
        return typing.cast(typing.Optional["LbListenerDefaultActionForwardStickiness"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbListenerDefaultActionForward(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LbListenerDefaultActionForwardOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lbListener.LbListenerDefaultActionForwardOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7739b11ea260cc0839609a56f1e189a0fcfa8af8080c2d271c3252985c15a19b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putStickiness")
    def put_stickiness(
        self,
        *,
        duration: jsii.Number,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#duration LbListener#duration}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#enabled LbListener#enabled}.
        '''
        value = LbListenerDefaultActionForwardStickiness(
            duration=duration, enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putStickiness", [value]))

    @jsii.member(jsii_name="putTargetGroup")
    def put_target_group(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LbListenerDefaultActionForwardTargetGroup", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e0d1472b70a9488a4eb36359477f939c755c991ac844e63933f94385d949df3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargetGroup", [value]))

    @jsii.member(jsii_name="resetStickiness")
    def reset_stickiness(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStickiness", []))

    @builtins.property
    @jsii.member(jsii_name="stickiness")
    def stickiness(self) -> "LbListenerDefaultActionForwardStickinessOutputReference":
        return typing.cast("LbListenerDefaultActionForwardStickinessOutputReference", jsii.get(self, "stickiness"))

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(self) -> "LbListenerDefaultActionForwardTargetGroupList":
        return typing.cast("LbListenerDefaultActionForwardTargetGroupList", jsii.get(self, "targetGroup"))

    @builtins.property
    @jsii.member(jsii_name="stickinessInput")
    def stickiness_input(
        self,
    ) -> typing.Optional["LbListenerDefaultActionForwardStickiness"]:
        return typing.cast(typing.Optional["LbListenerDefaultActionForwardStickiness"], jsii.get(self, "stickinessInput"))

    @builtins.property
    @jsii.member(jsii_name="targetGroupInput")
    def target_group_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LbListenerDefaultActionForwardTargetGroup"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LbListenerDefaultActionForwardTargetGroup"]]], jsii.get(self, "targetGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LbListenerDefaultActionForward]:
        return typing.cast(typing.Optional[LbListenerDefaultActionForward], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LbListenerDefaultActionForward],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a75d4b53471f504ebc99b2a476e3ff436e9bf1ab4b12f74f4c83cdde34aa1dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lbListener.LbListenerDefaultActionForwardStickiness",
    jsii_struct_bases=[],
    name_mapping={"duration": "duration", "enabled": "enabled"},
)
class LbListenerDefaultActionForwardStickiness:
    def __init__(
        self,
        *,
        duration: jsii.Number,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#duration LbListener#duration}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#enabled LbListener#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77251f30e372ffd2caa7a88894d135805a58587ba447a5c780aee9b14d98e5f9)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "duration": duration,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def duration(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#duration LbListener#duration}.'''
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#enabled LbListener#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbListenerDefaultActionForwardStickiness(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LbListenerDefaultActionForwardStickinessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lbListener.LbListenerDefaultActionForwardStickinessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1394a64052b7e1860f9711039e25157622d0f7b66358f92f8d600ba50701996b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85903ed1970818c162df1ca7aca1ec71557fd865f94a6ac29aaa55debf6af9a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b528e55f81c511b2a698701794454d891478daf25161ad8769f071c45f5e2b5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LbListenerDefaultActionForwardStickiness]:
        return typing.cast(typing.Optional[LbListenerDefaultActionForwardStickiness], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LbListenerDefaultActionForwardStickiness],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__478f8e1278405bdd1cb8753883c1e4b234d98526f0bc2c1ebaebe72af7aa7c81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lbListener.LbListenerDefaultActionForwardTargetGroup",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn", "weight": "weight"},
)
class LbListenerDefaultActionForwardTargetGroup:
    def __init__(
        self,
        *,
        arn: builtins.str,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#arn LbListener#arn}.
        :param weight: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#weight LbListener#weight}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__746b191bae9894d69db0d526f5bb2a22204850f22f64683a2922a4adc89dd13d)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "arn": arn,
        }
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#arn LbListener#arn}.'''
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#weight LbListener#weight}.'''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbListenerDefaultActionForwardTargetGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LbListenerDefaultActionForwardTargetGroupList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lbListener.LbListenerDefaultActionForwardTargetGroupList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e90a3a636bd9e698ab6d8e70c5fd7aa1f46ec398586ab3df39e433f2b0f2e063)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LbListenerDefaultActionForwardTargetGroupOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c00045b0c7833f79f91e90e7839ebd1f320c5e6f71ab14e9b7d539375ceec50)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LbListenerDefaultActionForwardTargetGroupOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5ef9798066e87612508bda25e52b573de3ca020a261a4c4aecd09e7d673a326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff6ca41cc2670bec140e8a5a178fa167ce9e540449d688b32f8dae5e1c50c630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__804482496c697c965248e8c4d4631a1a49e32cd3f67060169ff1ec88e020516e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LbListenerDefaultActionForwardTargetGroup]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LbListenerDefaultActionForwardTargetGroup]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LbListenerDefaultActionForwardTargetGroup]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba40c02f2263aeedb267e449a64589ccaff533ac8c45e8dfe699180ddb5ef0f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LbListenerDefaultActionForwardTargetGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lbListener.LbListenerDefaultActionForwardTargetGroupOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8de3b800210b7ea37a2374091244698123b59fc2da58c1489e2dc002c75cb1d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetWeight")
    def reset_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeight", []))

    @builtins.property
    @jsii.member(jsii_name="arnInput")
    def arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arnInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @arn.setter
    def arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__354f710c3b8bee4edaef7871e5d780b9a1839baa98877e66fef2d7e2b9b14bd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arn", value)

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88777bbdb2bf19aab742a5d712006f91a32c5d6f361bf93cc92c326d8e00fa21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbListenerDefaultActionForwardTargetGroup]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbListenerDefaultActionForwardTargetGroup]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbListenerDefaultActionForwardTargetGroup]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf7479ef0d5bfa7326a13004972ddc1daa8c6310182a1ca57dbf6bc5f3046770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LbListenerDefaultActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lbListener.LbListenerDefaultActionList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30bfc954ab47761857d72e06c19e6ef4cb795bd2c310f514d678b260d05822e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LbListenerDefaultActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa9807060efe1fd681be8201e5c4ef47becdfe941135db2de7230e2d70edbe3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LbListenerDefaultActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3f0f2873aa59a36ddee30e10239a1309828ee718d3138c1f9a6fcd344db7846)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b300c6760756bfbf9ba3b346287c1e47a7489036ad2e535dbdef99486aad664)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26819d0a1d30ffc87fe631a3e4f63db595e170edb8205e1f5064753529fe252e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LbListenerDefaultAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LbListenerDefaultAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LbListenerDefaultAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__655a25045561980a6d7506bdaf4977c9b9dff297d65c29f8e741c636117fa5f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LbListenerDefaultActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lbListener.LbListenerDefaultActionOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ea4b1160e423600ffb7b030d7eb46bbca8b8ae6708ef506ee638050f4f65afa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAuthenticateCognito")
    def put_authenticate_cognito(
        self,
        *,
        user_pool_arn: builtins.str,
        user_pool_client_id: builtins.str,
        user_pool_domain: builtins.str,
        authentication_request_extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        on_unauthenticated_request: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        session_cookie_name: typing.Optional[builtins.str] = None,
        session_timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param user_pool_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#user_pool_arn LbListener#user_pool_arn}.
        :param user_pool_client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#user_pool_client_id LbListener#user_pool_client_id}.
        :param user_pool_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#user_pool_domain LbListener#user_pool_domain}.
        :param authentication_request_extra_params: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#authentication_request_extra_params LbListener#authentication_request_extra_params}.
        :param on_unauthenticated_request: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#on_unauthenticated_request LbListener#on_unauthenticated_request}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#scope LbListener#scope}.
        :param session_cookie_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#session_cookie_name LbListener#session_cookie_name}.
        :param session_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#session_timeout LbListener#session_timeout}.
        '''
        value = LbListenerDefaultActionAuthenticateCognito(
            user_pool_arn=user_pool_arn,
            user_pool_client_id=user_pool_client_id,
            user_pool_domain=user_pool_domain,
            authentication_request_extra_params=authentication_request_extra_params,
            on_unauthenticated_request=on_unauthenticated_request,
            scope=scope,
            session_cookie_name=session_cookie_name,
            session_timeout=session_timeout,
        )

        return typing.cast(None, jsii.invoke(self, "putAuthenticateCognito", [value]))

    @jsii.member(jsii_name="putAuthenticateOidc")
    def put_authenticate_oidc(
        self,
        *,
        authorization_endpoint: builtins.str,
        client_id: builtins.str,
        client_secret: builtins.str,
        issuer: builtins.str,
        token_endpoint: builtins.str,
        user_info_endpoint: builtins.str,
        authentication_request_extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        on_unauthenticated_request: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        session_cookie_name: typing.Optional[builtins.str] = None,
        session_timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param authorization_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#authorization_endpoint LbListener#authorization_endpoint}.
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#client_id LbListener#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#client_secret LbListener#client_secret}.
        :param issuer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#issuer LbListener#issuer}.
        :param token_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#token_endpoint LbListener#token_endpoint}.
        :param user_info_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#user_info_endpoint LbListener#user_info_endpoint}.
        :param authentication_request_extra_params: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#authentication_request_extra_params LbListener#authentication_request_extra_params}.
        :param on_unauthenticated_request: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#on_unauthenticated_request LbListener#on_unauthenticated_request}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#scope LbListener#scope}.
        :param session_cookie_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#session_cookie_name LbListener#session_cookie_name}.
        :param session_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#session_timeout LbListener#session_timeout}.
        '''
        value = LbListenerDefaultActionAuthenticateOidc(
            authorization_endpoint=authorization_endpoint,
            client_id=client_id,
            client_secret=client_secret,
            issuer=issuer,
            token_endpoint=token_endpoint,
            user_info_endpoint=user_info_endpoint,
            authentication_request_extra_params=authentication_request_extra_params,
            on_unauthenticated_request=on_unauthenticated_request,
            scope=scope,
            session_cookie_name=session_cookie_name,
            session_timeout=session_timeout,
        )

        return typing.cast(None, jsii.invoke(self, "putAuthenticateOidc", [value]))

    @jsii.member(jsii_name="putFixedResponse")
    def put_fixed_response(
        self,
        *,
        content_type: builtins.str,
        message_body: typing.Optional[builtins.str] = None,
        status_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#content_type LbListener#content_type}.
        :param message_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#message_body LbListener#message_body}.
        :param status_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#status_code LbListener#status_code}.
        '''
        value = LbListenerDefaultActionFixedResponse(
            content_type=content_type,
            message_body=message_body,
            status_code=status_code,
        )

        return typing.cast(None, jsii.invoke(self, "putFixedResponse", [value]))

    @jsii.member(jsii_name="putForward")
    def put_forward(
        self,
        *,
        target_group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LbListenerDefaultActionForwardTargetGroup, typing.Dict[builtins.str, typing.Any]]]],
        stickiness: typing.Optional[typing.Union[LbListenerDefaultActionForwardStickiness, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param target_group: target_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#target_group LbListener#target_group}
        :param stickiness: stickiness block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#stickiness LbListener#stickiness}
        '''
        value = LbListenerDefaultActionForward(
            target_group=target_group, stickiness=stickiness
        )

        return typing.cast(None, jsii.invoke(self, "putForward", [value]))

    @jsii.member(jsii_name="putRedirect")
    def put_redirect(
        self,
        *,
        status_code: builtins.str,
        host: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        query: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param status_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#status_code LbListener#status_code}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#host LbListener#host}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#path LbListener#path}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#port LbListener#port}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#protocol LbListener#protocol}.
        :param query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#query LbListener#query}.
        '''
        value = LbListenerDefaultActionRedirect(
            status_code=status_code,
            host=host,
            path=path,
            port=port,
            protocol=protocol,
            query=query,
        )

        return typing.cast(None, jsii.invoke(self, "putRedirect", [value]))

    @jsii.member(jsii_name="resetAuthenticateCognito")
    def reset_authenticate_cognito(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticateCognito", []))

    @jsii.member(jsii_name="resetAuthenticateOidc")
    def reset_authenticate_oidc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticateOidc", []))

    @jsii.member(jsii_name="resetFixedResponse")
    def reset_fixed_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedResponse", []))

    @jsii.member(jsii_name="resetForward")
    def reset_forward(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForward", []))

    @jsii.member(jsii_name="resetOrder")
    def reset_order(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrder", []))

    @jsii.member(jsii_name="resetRedirect")
    def reset_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirect", []))

    @jsii.member(jsii_name="resetTargetGroupArn")
    def reset_target_group_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetGroupArn", []))

    @builtins.property
    @jsii.member(jsii_name="authenticateCognito")
    def authenticate_cognito(
        self,
    ) -> LbListenerDefaultActionAuthenticateCognitoOutputReference:
        return typing.cast(LbListenerDefaultActionAuthenticateCognitoOutputReference, jsii.get(self, "authenticateCognito"))

    @builtins.property
    @jsii.member(jsii_name="authenticateOidc")
    def authenticate_oidc(
        self,
    ) -> LbListenerDefaultActionAuthenticateOidcOutputReference:
        return typing.cast(LbListenerDefaultActionAuthenticateOidcOutputReference, jsii.get(self, "authenticateOidc"))

    @builtins.property
    @jsii.member(jsii_name="fixedResponse")
    def fixed_response(self) -> LbListenerDefaultActionFixedResponseOutputReference:
        return typing.cast(LbListenerDefaultActionFixedResponseOutputReference, jsii.get(self, "fixedResponse"))

    @builtins.property
    @jsii.member(jsii_name="forward")
    def forward(self) -> LbListenerDefaultActionForwardOutputReference:
        return typing.cast(LbListenerDefaultActionForwardOutputReference, jsii.get(self, "forward"))

    @builtins.property
    @jsii.member(jsii_name="redirect")
    def redirect(self) -> "LbListenerDefaultActionRedirectOutputReference":
        return typing.cast("LbListenerDefaultActionRedirectOutputReference", jsii.get(self, "redirect"))

    @builtins.property
    @jsii.member(jsii_name="authenticateCognitoInput")
    def authenticate_cognito_input(
        self,
    ) -> typing.Optional[LbListenerDefaultActionAuthenticateCognito]:
        return typing.cast(typing.Optional[LbListenerDefaultActionAuthenticateCognito], jsii.get(self, "authenticateCognitoInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticateOidcInput")
    def authenticate_oidc_input(
        self,
    ) -> typing.Optional[LbListenerDefaultActionAuthenticateOidc]:
        return typing.cast(typing.Optional[LbListenerDefaultActionAuthenticateOidc], jsii.get(self, "authenticateOidcInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedResponseInput")
    def fixed_response_input(
        self,
    ) -> typing.Optional[LbListenerDefaultActionFixedResponse]:
        return typing.cast(typing.Optional[LbListenerDefaultActionFixedResponse], jsii.get(self, "fixedResponseInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardInput")
    def forward_input(self) -> typing.Optional[LbListenerDefaultActionForward]:
        return typing.cast(typing.Optional[LbListenerDefaultActionForward], jsii.get(self, "forwardInput"))

    @builtins.property
    @jsii.member(jsii_name="orderInput")
    def order_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "orderInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectInput")
    def redirect_input(self) -> typing.Optional["LbListenerDefaultActionRedirect"]:
        return typing.cast(typing.Optional["LbListenerDefaultActionRedirect"], jsii.get(self, "redirectInput"))

    @builtins.property
    @jsii.member(jsii_name="targetGroupArnInput")
    def target_group_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetGroupArnInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "order"))

    @order.setter
    def order(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4b4f7363287133dee5834c1511147324fb4c060c1992425d78416fdea732932)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "order", value)

    @builtins.property
    @jsii.member(jsii_name="targetGroupArn")
    def target_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetGroupArn"))

    @target_group_arn.setter
    def target_group_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d7322476533dd8a5b7c4c059304ba39acdd86a6815b55ff6ca113bec5e5beb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetGroupArn", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5ffd3c9529226c85baa44633382c1ab159765924ad8dfa1812433e08b21f4e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbListenerDefaultAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbListenerDefaultAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbListenerDefaultAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc092da75f78f118a79e70a2f9256ca743bef52a755cc29d95bd58a3ef956ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lbListener.LbListenerDefaultActionRedirect",
    jsii_struct_bases=[],
    name_mapping={
        "status_code": "statusCode",
        "host": "host",
        "path": "path",
        "port": "port",
        "protocol": "protocol",
        "query": "query",
    },
)
class LbListenerDefaultActionRedirect:
    def __init__(
        self,
        *,
        status_code: builtins.str,
        host: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        query: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param status_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#status_code LbListener#status_code}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#host LbListener#host}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#path LbListener#path}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#port LbListener#port}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#protocol LbListener#protocol}.
        :param query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#query LbListener#query}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__200a42881013ce46de3ddb5f07b3d068ca90a4bf5e9e897f2dda98f7bc880eb9)
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "status_code": status_code,
        }
        if host is not None:
            self._values["host"] = host
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if query is not None:
            self._values["query"] = query

    @builtins.property
    def status_code(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#status_code LbListener#status_code}.'''
        result = self._values.get("status_code")
        assert result is not None, "Required property 'status_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#host LbListener#host}.'''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#path LbListener#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#port LbListener#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#protocol LbListener#protocol}.'''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#query LbListener#query}.'''
        result = self._values.get("query")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbListenerDefaultActionRedirect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LbListenerDefaultActionRedirectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lbListener.LbListenerDefaultActionRedirectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e113505b6d7dc21f3953e8ec21784fcab02ced92610aaa7eec161013d5dc117d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="statusCodeInput")
    def status_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ccdc5dabb72a0219a062e9513f4bc00162ea4f795815528f5792785e95ca440)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b43540ce3b12a67524845485e9bc29a329612ce8d77ad4878fd1dede85101a38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f9aa8b3efeda063255fdcadd48d5f4ecc01762cf38da9887cdd666f03b62139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d04d87fad6d6b7f4c9b573c2de5cd9a6cc4a430ebb28ba72e7610ceafbfd25b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__938f39a0a76a2337360bbbe10874ed98e344610fda639d9f752c018193c10f6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusCode"))

    @status_code.setter
    def status_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__778f026eff5c62c07080e7c4085b698f4d1ae455d1b446e7be6eb014bb0b18aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusCode", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LbListenerDefaultActionRedirect]:
        return typing.cast(typing.Optional[LbListenerDefaultActionRedirect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LbListenerDefaultActionRedirect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e6615817dc29f5114c48134b4c445ca38d9438e2d6b3fa5744c42aeea5b5d0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lbListener.LbListenerTimeouts",
    jsii_struct_bases=[],
    name_mapping={"read": "read"},
)
class LbListenerTimeouts:
    def __init__(self, *, read: typing.Optional[builtins.str] = None) -> None:
        '''
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#read LbListener#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e127855131eadac348a35123dbc67199a4a762070cad23132af1bd596a3089d)
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if read is not None:
            self._values["read"] = read

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/lb_listener#read LbListener#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbListenerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LbListenerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lbListener.LbListenerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60f5b5349ab4a16c5f409dfd379429fdff725633cc785f3126ad77039ec4f77c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75dca95c9f673a2140e85b84ffa6c5bcb37203941bcbd9305898611a93f7049e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbListenerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbListenerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbListenerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a07423686205b8ddce667a68562fd6aac75cf6604a363656539ed49274eae7c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "LbListener",
    "LbListenerConfig",
    "LbListenerDefaultAction",
    "LbListenerDefaultActionAuthenticateCognito",
    "LbListenerDefaultActionAuthenticateCognitoOutputReference",
    "LbListenerDefaultActionAuthenticateOidc",
    "LbListenerDefaultActionAuthenticateOidcOutputReference",
    "LbListenerDefaultActionFixedResponse",
    "LbListenerDefaultActionFixedResponseOutputReference",
    "LbListenerDefaultActionForward",
    "LbListenerDefaultActionForwardOutputReference",
    "LbListenerDefaultActionForwardStickiness",
    "LbListenerDefaultActionForwardStickinessOutputReference",
    "LbListenerDefaultActionForwardTargetGroup",
    "LbListenerDefaultActionForwardTargetGroupList",
    "LbListenerDefaultActionForwardTargetGroupOutputReference",
    "LbListenerDefaultActionList",
    "LbListenerDefaultActionOutputReference",
    "LbListenerDefaultActionRedirect",
    "LbListenerDefaultActionRedirectOutputReference",
    "LbListenerTimeouts",
    "LbListenerTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0e05f9c031e1db2706dcfe3b4556e44f5c3e75642d2ab0be31c5f0e4273bad93(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    default_action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LbListenerDefaultAction, typing.Dict[builtins.str, typing.Any]]]],
    load_balancer_arn: builtins.str,
    alpn_policy: typing.Optional[builtins.str] = None,
    certificate_arn: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
    ssl_policy: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[LbListenerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__07952a1a8fb697491ad46974796b0f5db51120cdb230f5265b9a047588242e50(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LbListenerDefaultAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2342b47a81580b4b42811f77f8cb0922118259bec9c23c495b20e832daf5f7bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be09bbacab395102713596a51a4f4f230188bb3f18194596dacd5892cfda25ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4961ea0372c39fbc5d8a6c295bd5d8a94e9c3f20c1aa62b009a30d3bb5cce8e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1e464cc333c8727720158eb312a7abc0aff4a07cc2331ede0a2d6661b93081f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938fecbd77628b8318619b71bef7aed9f775c38d25058078cb5a89179ebaa5ee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be1335717b4a1c12d11f296111a26fa2b556af88fd82b6d1aa57802d1e251b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60537b1272b8503fbf708018a7b23fb5a018487579a0ad41756f20133f9f7b13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce5caed2d49e715e74cd8eaaaf79b1922b386518366ccc2c26fcd74d53bb2d21(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af321ceb45b673a68c5a16584cc67e079ba03a404930ab679d4f5de827d3ef3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a9cb2ead8a3e1523913faf81dedc14718a024fb9e7458cf0efc1b06ac86fd77(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LbListenerDefaultAction, typing.Dict[builtins.str, typing.Any]]]],
    load_balancer_arn: builtins.str,
    alpn_policy: typing.Optional[builtins.str] = None,
    certificate_arn: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
    ssl_policy: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[LbListenerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3face0812180d37cd8274fe0b875786d8e41acab2f0fc57ce5925adf9384829(
    *,
    type: builtins.str,
    authenticate_cognito: typing.Optional[typing.Union[LbListenerDefaultActionAuthenticateCognito, typing.Dict[builtins.str, typing.Any]]] = None,
    authenticate_oidc: typing.Optional[typing.Union[LbListenerDefaultActionAuthenticateOidc, typing.Dict[builtins.str, typing.Any]]] = None,
    fixed_response: typing.Optional[typing.Union[LbListenerDefaultActionFixedResponse, typing.Dict[builtins.str, typing.Any]]] = None,
    forward: typing.Optional[typing.Union[LbListenerDefaultActionForward, typing.Dict[builtins.str, typing.Any]]] = None,
    order: typing.Optional[jsii.Number] = None,
    redirect: typing.Optional[typing.Union[LbListenerDefaultActionRedirect, typing.Dict[builtins.str, typing.Any]]] = None,
    target_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__095766fa2e6f31689406b03429dcfaac15c3983d65d5d565c230b5899ef2d6e2(
    *,
    user_pool_arn: builtins.str,
    user_pool_client_id: builtins.str,
    user_pool_domain: builtins.str,
    authentication_request_extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    on_unauthenticated_request: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    session_cookie_name: typing.Optional[builtins.str] = None,
    session_timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36427a8405cd0e22e20a8ec220dc3aa2a2cde29bc8d86fa638b8c4c8d7aa3974(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0e9b12f6b8eca4686871d620f3392f216c3688903b733c37faf302082a330a7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f893d90b51e9151426e4fe723c7cff028eeb207282ca1e352445365c7c3787eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6845de12a3f3427c83d62021eea28bc86ee571eecfd3d9ef03122f5852be66d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d4b7f3c289d1ea4db7ea885388407422a9db279229b7a729632e1c863a4108(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cadf625aebff884fb2e16306eacb7247b8f5307af052390c27962f91b02636c9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f33b6993992f07fe55b66be2980fb8210418f3d4939229486cc2a70c0dc75ec9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90bd4271bf62bac602c3d438511894f9658672463ed2aa156bf3855948444f76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dd39c7cad48cc6aeef95f48a93e459cac17a22d8cb5b052293b181cff4ce866(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3756598e296bd1b1fd3c0160cc221217ba9d5afb873e368ef9231035a0cb07(
    value: typing.Optional[LbListenerDefaultActionAuthenticateCognito],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f03f7b8b895017730827726386876781f0bc83cd89af750517ff6e8a47fbd91(
    *,
    authorization_endpoint: builtins.str,
    client_id: builtins.str,
    client_secret: builtins.str,
    issuer: builtins.str,
    token_endpoint: builtins.str,
    user_info_endpoint: builtins.str,
    authentication_request_extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    on_unauthenticated_request: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    session_cookie_name: typing.Optional[builtins.str] = None,
    session_timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b492e094ad4f10f8519827362a3aaa77bba8cf2458d5242758dadbeb71846df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceb155cfe8f0b586c356c7d406678e7df645b8ca41bd1514924389ac044883d1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e83dd5171f43a544d6298baaea5ddd5c50be890e4206c6cf6b6e682e880beba4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe795009eb0676ae6c333ffd6c55d354a4b6ec77201bd5a3b16d0722755dedc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__212e1f828616515320f313026d440ce3126fdbfa6bc5ce5cd8e17dfabbff6f6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c099af595a427c0996199f4341e2db993505f30dc549a3d9ca814a6b8be74d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a043d0012c9ba9ef1d5ade6509aab3fbdaae94bec7f68be1f74d70e1b39466a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472e173443c892f47073ae197cc2759d47bbd5045c620621137d5b3e799d8846(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d1ca2635ddf7cd7a0b64b89ee4c952ccec9f1b9a90a8f7003e009ba1b522efc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d2b4f603ab0c9f8f750b80131ae8e6566918ffd168e2c757e9bd3c72a4ce87(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86fa58911889e072edcb5acd16ab5c420a300325d66426fe6be9c4e3430c2193(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e96845f3c354429cb5548d006ba2815b72c6a63ad848f68cbbcf143631d37d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6833fe9fc4a284f3e46f247b73a8428580c9da8ebc311b2b6a88f57cb10eafe(
    value: typing.Optional[LbListenerDefaultActionAuthenticateOidc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23014c7a7f68dcabada65bee01e0f37ca8a0d62132d5abf68c7b335f6e3e745f(
    *,
    content_type: builtins.str,
    message_body: typing.Optional[builtins.str] = None,
    status_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d8b3b4e4fb1cd87c73d3a360c1458b8411f24c9beb4cc2b1db35defe3028c46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286c2a654f4f12ef143ca0087c463e4dd15c8c61d78d8c3fc8a4c2cf2900f109(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e83b975cbaa5628ead906a47e3e7bf555eef3a3b1b9ff71c2cff489db3de791(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dfb7020a477167cd50e2d3f935a694ae639024a360343942eceb286da12e0e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa82b680b9ef16cd128f64c6099351727e287a8cecd438b9ffcb8fae1bd04595(
    value: typing.Optional[LbListenerDefaultActionFixedResponse],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316fd60f78368b0f63f89a55f4c066026e4602de7ea4a9e09f3c270561e5e60c(
    *,
    target_group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LbListenerDefaultActionForwardTargetGroup, typing.Dict[builtins.str, typing.Any]]]],
    stickiness: typing.Optional[typing.Union[LbListenerDefaultActionForwardStickiness, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7739b11ea260cc0839609a56f1e189a0fcfa8af8080c2d271c3252985c15a19b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0d1472b70a9488a4eb36359477f939c755c991ac844e63933f94385d949df3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LbListenerDefaultActionForwardTargetGroup, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a75d4b53471f504ebc99b2a476e3ff436e9bf1ab4b12f74f4c83cdde34aa1dd(
    value: typing.Optional[LbListenerDefaultActionForward],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77251f30e372ffd2caa7a88894d135805a58587ba447a5c780aee9b14d98e5f9(
    *,
    duration: jsii.Number,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1394a64052b7e1860f9711039e25157622d0f7b66358f92f8d600ba50701996b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85903ed1970818c162df1ca7aca1ec71557fd865f94a6ac29aaa55debf6af9a2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b528e55f81c511b2a698701794454d891478daf25161ad8769f071c45f5e2b5e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__478f8e1278405bdd1cb8753883c1e4b234d98526f0bc2c1ebaebe72af7aa7c81(
    value: typing.Optional[LbListenerDefaultActionForwardStickiness],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__746b191bae9894d69db0d526f5bb2a22204850f22f64683a2922a4adc89dd13d(
    *,
    arn: builtins.str,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e90a3a636bd9e698ab6d8e70c5fd7aa1f46ec398586ab3df39e433f2b0f2e063(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c00045b0c7833f79f91e90e7839ebd1f320c5e6f71ab14e9b7d539375ceec50(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5ef9798066e87612508bda25e52b573de3ca020a261a4c4aecd09e7d673a326(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff6ca41cc2670bec140e8a5a178fa167ce9e540449d688b32f8dae5e1c50c630(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__804482496c697c965248e8c4d4631a1a49e32cd3f67060169ff1ec88e020516e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba40c02f2263aeedb267e449a64589ccaff533ac8c45e8dfe699180ddb5ef0f0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LbListenerDefaultActionForwardTargetGroup]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8de3b800210b7ea37a2374091244698123b59fc2da58c1489e2dc002c75cb1d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354f710c3b8bee4edaef7871e5d780b9a1839baa98877e66fef2d7e2b9b14bd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88777bbdb2bf19aab742a5d712006f91a32c5d6f361bf93cc92c326d8e00fa21(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7479ef0d5bfa7326a13004972ddc1daa8c6310182a1ca57dbf6bc5f3046770(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbListenerDefaultActionForwardTargetGroup]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30bfc954ab47761857d72e06c19e6ef4cb795bd2c310f514d678b260d05822e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa9807060efe1fd681be8201e5c4ef47becdfe941135db2de7230e2d70edbe3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f0f2873aa59a36ddee30e10239a1309828ee718d3138c1f9a6fcd344db7846(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b300c6760756bfbf9ba3b346287c1e47a7489036ad2e535dbdef99486aad664(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26819d0a1d30ffc87fe631a3e4f63db595e170edb8205e1f5064753529fe252e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__655a25045561980a6d7506bdaf4977c9b9dff297d65c29f8e741c636117fa5f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LbListenerDefaultAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ea4b1160e423600ffb7b030d7eb46bbca8b8ae6708ef506ee638050f4f65afa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4b4f7363287133dee5834c1511147324fb4c060c1992425d78416fdea732932(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d7322476533dd8a5b7c4c059304ba39acdd86a6815b55ff6ca113bec5e5beb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5ffd3c9529226c85baa44633382c1ab159765924ad8dfa1812433e08b21f4e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc092da75f78f118a79e70a2f9256ca743bef52a755cc29d95bd58a3ef956ec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbListenerDefaultAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__200a42881013ce46de3ddb5f07b3d068ca90a4bf5e9e897f2dda98f7bc880eb9(
    *,
    status_code: builtins.str,
    host: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    query: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e113505b6d7dc21f3953e8ec21784fcab02ced92610aaa7eec161013d5dc117d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ccdc5dabb72a0219a062e9513f4bc00162ea4f795815528f5792785e95ca440(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43540ce3b12a67524845485e9bc29a329612ce8d77ad4878fd1dede85101a38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f9aa8b3efeda063255fdcadd48d5f4ecc01762cf38da9887cdd666f03b62139(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04d87fad6d6b7f4c9b573c2de5cd9a6cc4a430ebb28ba72e7610ceafbfd25b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938f39a0a76a2337360bbbe10874ed98e344610fda639d9f752c018193c10f6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__778f026eff5c62c07080e7c4085b698f4d1ae455d1b446e7be6eb014bb0b18aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e6615817dc29f5114c48134b4c445ca38d9438e2d6b3fa5744c42aeea5b5d0c(
    value: typing.Optional[LbListenerDefaultActionRedirect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e127855131eadac348a35123dbc67199a4a762070cad23132af1bd596a3089d(
    *,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f5b5349ab4a16c5f409dfd379429fdff725633cc785f3126ad77039ec4f77c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75dca95c9f673a2140e85b84ffa6c5bcb37203941bcbd9305898611a93f7049e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a07423686205b8ddce667a68562fd6aac75cf6604a363656539ed49274eae7c8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbListenerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
