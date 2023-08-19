'''
# `aws_route53_health_check`

Refer to the Terraform Registory for docs: [`aws_route53_health_check`](https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check).
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


class Route53HealthCheck(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.route53HealthCheck.Route53HealthCheck",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check aws_route53_health_check}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        type: builtins.str,
        child_healthchecks: typing.Optional[typing.Sequence[builtins.str]] = None,
        child_health_threshold: typing.Optional[jsii.Number] = None,
        cloudwatch_alarm_name: typing.Optional[builtins.str] = None,
        cloudwatch_alarm_region: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_sni: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        failure_threshold: typing.Optional[jsii.Number] = None,
        fqdn: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        insufficient_data_health_status: typing.Optional[builtins.str] = None,
        invert_healthcheck: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_address: typing.Optional[builtins.str] = None,
        measure_latency: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        port: typing.Optional[jsii.Number] = None,
        reference_name: typing.Optional[builtins.str] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_interval: typing.Optional[jsii.Number] = None,
        resource_path: typing.Optional[builtins.str] = None,
        routing_control_arn: typing.Optional[builtins.str] = None,
        search_string: typing.Optional[builtins.str] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check aws_route53_health_check} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#type Route53HealthCheck#type}.
        :param child_healthchecks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#child_healthchecks Route53HealthCheck#child_healthchecks}.
        :param child_health_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#child_health_threshold Route53HealthCheck#child_health_threshold}.
        :param cloudwatch_alarm_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#cloudwatch_alarm_name Route53HealthCheck#cloudwatch_alarm_name}.
        :param cloudwatch_alarm_region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#cloudwatch_alarm_region Route53HealthCheck#cloudwatch_alarm_region}.
        :param disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#disabled Route53HealthCheck#disabled}.
        :param enable_sni: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#enable_sni Route53HealthCheck#enable_sni}.
        :param failure_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#failure_threshold Route53HealthCheck#failure_threshold}.
        :param fqdn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#fqdn Route53HealthCheck#fqdn}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#id Route53HealthCheck#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param insufficient_data_health_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#insufficient_data_health_status Route53HealthCheck#insufficient_data_health_status}.
        :param invert_healthcheck: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#invert_healthcheck Route53HealthCheck#invert_healthcheck}.
        :param ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#ip_address Route53HealthCheck#ip_address}.
        :param measure_latency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#measure_latency Route53HealthCheck#measure_latency}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#port Route53HealthCheck#port}.
        :param reference_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#reference_name Route53HealthCheck#reference_name}.
        :param regions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#regions Route53HealthCheck#regions}.
        :param request_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#request_interval Route53HealthCheck#request_interval}.
        :param resource_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#resource_path Route53HealthCheck#resource_path}.
        :param routing_control_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#routing_control_arn Route53HealthCheck#routing_control_arn}.
        :param search_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#search_string Route53HealthCheck#search_string}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#tags Route53HealthCheck#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#tags_all Route53HealthCheck#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9552a76b0db10a01bed3d1a6691c7eed74ba27ecb921dbf79c83c010f08dbfd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = Route53HealthCheckConfig(
            type=type,
            child_healthchecks=child_healthchecks,
            child_health_threshold=child_health_threshold,
            cloudwatch_alarm_name=cloudwatch_alarm_name,
            cloudwatch_alarm_region=cloudwatch_alarm_region,
            disabled=disabled,
            enable_sni=enable_sni,
            failure_threshold=failure_threshold,
            fqdn=fqdn,
            id=id,
            insufficient_data_health_status=insufficient_data_health_status,
            invert_healthcheck=invert_healthcheck,
            ip_address=ip_address,
            measure_latency=measure_latency,
            port=port,
            reference_name=reference_name,
            regions=regions,
            request_interval=request_interval,
            resource_path=resource_path,
            routing_control_arn=routing_control_arn,
            search_string=search_string,
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

    @jsii.member(jsii_name="resetChildHealthchecks")
    def reset_child_healthchecks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChildHealthchecks", []))

    @jsii.member(jsii_name="resetChildHealthThreshold")
    def reset_child_health_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChildHealthThreshold", []))

    @jsii.member(jsii_name="resetCloudwatchAlarmName")
    def reset_cloudwatch_alarm_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchAlarmName", []))

    @jsii.member(jsii_name="resetCloudwatchAlarmRegion")
    def reset_cloudwatch_alarm_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchAlarmRegion", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetEnableSni")
    def reset_enable_sni(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSni", []))

    @jsii.member(jsii_name="resetFailureThreshold")
    def reset_failure_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureThreshold", []))

    @jsii.member(jsii_name="resetFqdn")
    def reset_fqdn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFqdn", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInsufficientDataHealthStatus")
    def reset_insufficient_data_health_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsufficientDataHealthStatus", []))

    @jsii.member(jsii_name="resetInvertHealthcheck")
    def reset_invert_healthcheck(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvertHealthcheck", []))

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @jsii.member(jsii_name="resetMeasureLatency")
    def reset_measure_latency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMeasureLatency", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetReferenceName")
    def reset_reference_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReferenceName", []))

    @jsii.member(jsii_name="resetRegions")
    def reset_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegions", []))

    @jsii.member(jsii_name="resetRequestInterval")
    def reset_request_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestInterval", []))

    @jsii.member(jsii_name="resetResourcePath")
    def reset_resource_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourcePath", []))

    @jsii.member(jsii_name="resetRoutingControlArn")
    def reset_routing_control_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingControlArn", []))

    @jsii.member(jsii_name="resetSearchString")
    def reset_search_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearchString", []))

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
    @jsii.member(jsii_name="childHealthchecksInput")
    def child_healthchecks_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "childHealthchecksInput"))

    @builtins.property
    @jsii.member(jsii_name="childHealthThresholdInput")
    def child_health_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "childHealthThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchAlarmNameInput")
    def cloudwatch_alarm_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudwatchAlarmNameInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchAlarmRegionInput")
    def cloudwatch_alarm_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudwatchAlarmRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSniInput")
    def enable_sni_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSniInput"))

    @builtins.property
    @jsii.member(jsii_name="failureThresholdInput")
    def failure_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="fqdnInput")
    def fqdn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fqdnInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="insufficientDataHealthStatusInput")
    def insufficient_data_health_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "insufficientDataHealthStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="invertHealthcheckInput")
    def invert_healthcheck_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "invertHealthcheckInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="measureLatencyInput")
    def measure_latency_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "measureLatencyInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="referenceNameInput")
    def reference_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "referenceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionsInput")
    def regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "regionsInput"))

    @builtins.property
    @jsii.member(jsii_name="requestIntervalInput")
    def request_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "requestIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcePathInput")
    def resource_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourcePathInput"))

    @builtins.property
    @jsii.member(jsii_name="routingControlArnInput")
    def routing_control_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingControlArnInput"))

    @builtins.property
    @jsii.member(jsii_name="searchStringInput")
    def search_string_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "searchStringInput"))

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
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="childHealthchecks")
    def child_healthchecks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "childHealthchecks"))

    @child_healthchecks.setter
    def child_healthchecks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45788cc35dc7d57c7caac31d818dc38b4d66d1e8589e53f08985528419d44a5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "childHealthchecks", value)

    @builtins.property
    @jsii.member(jsii_name="childHealthThreshold")
    def child_health_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "childHealthThreshold"))

    @child_health_threshold.setter
    def child_health_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffb45ea7384da4fe762b26273d6598e6fb1d9e7562b2b05db1143bc52a2cda40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "childHealthThreshold", value)

    @builtins.property
    @jsii.member(jsii_name="cloudwatchAlarmName")
    def cloudwatch_alarm_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudwatchAlarmName"))

    @cloudwatch_alarm_name.setter
    def cloudwatch_alarm_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86fbe73f164bfd858edaf8cdaf7d61ed6a3429e285a6f8305f8527c0c8d83d46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudwatchAlarmName", value)

    @builtins.property
    @jsii.member(jsii_name="cloudwatchAlarmRegion")
    def cloudwatch_alarm_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudwatchAlarmRegion"))

    @cloudwatch_alarm_region.setter
    def cloudwatch_alarm_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a0f5cad60d3e767a8666638a878432ade3ed9c865f33a63bb03eef96075c9ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudwatchAlarmRegion", value)

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f700c6012441fb9d24874833fb7ed98535e6f942c34273de8aa3ff99ee9a078e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value)

    @builtins.property
    @jsii.member(jsii_name="enableSni")
    def enable_sni(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSni"))

    @enable_sni.setter
    def enable_sni(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79127f181d32b775eb3ba6e86bd135d36891b57c45eb844f7fc0078fb4babef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSni", value)

    @builtins.property
    @jsii.member(jsii_name="failureThreshold")
    def failure_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failureThreshold"))

    @failure_threshold.setter
    def failure_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad669aa8f427b85e94cf27b82c932332ac364bcd89e45c905e04ed03302c7b7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureThreshold", value)

    @builtins.property
    @jsii.member(jsii_name="fqdn")
    def fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fqdn"))

    @fqdn.setter
    def fqdn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5beaf3fc239ed7296de5dce4501e45eaf1510183afb295e421756c8e1bd720a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fqdn", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e715d0f8c1972396460a19231b2a7b4554b7a25b1db50bd9df740bdc0ccfceed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="insufficientDataHealthStatus")
    def insufficient_data_health_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "insufficientDataHealthStatus"))

    @insufficient_data_health_status.setter
    def insufficient_data_health_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d43b6f448a086064ce0275d956e07b79e1131ec415134dd05a881d0964ac926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insufficientDataHealthStatus", value)

    @builtins.property
    @jsii.member(jsii_name="invertHealthcheck")
    def invert_healthcheck(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "invertHealthcheck"))

    @invert_healthcheck.setter
    def invert_healthcheck(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c06f30a1604341424f4005ea3ca3e52a73e4559749c281d4683c9f5cba865ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertHealthcheck", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__201bb8ac18f77f7786543be573df7de66e77b53b7e50d5fbc11aae057dfd0df4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value)

    @builtins.property
    @jsii.member(jsii_name="measureLatency")
    def measure_latency(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "measureLatency"))

    @measure_latency.setter
    def measure_latency(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__687ec1992f70e4fc0f30c7041bdb1ef2f9aaa07fd0ac6a1c60a94144ce7411e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "measureLatency", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6296f25e611ace8448c519628dc58ef926cda0d30555bb7c3ab8b1c00522d0e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="referenceName")
    def reference_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "referenceName"))

    @reference_name.setter
    def reference_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a927fa5c9432134a95f96c1b7190068fc2ea37665faaf4d1b4c00a7011c0ae2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referenceName", value)

    @builtins.property
    @jsii.member(jsii_name="regions")
    def regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "regions"))

    @regions.setter
    def regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f8417064226f5e55a73d887152942fb7ba410c8e19e10c2ad234c6a3ef8781e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regions", value)

    @builtins.property
    @jsii.member(jsii_name="requestInterval")
    def request_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "requestInterval"))

    @request_interval.setter
    def request_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__394e5831d97f438651f53f3c6a40bc225f8e4e86353a9fde2a7fb278451f235c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestInterval", value)

    @builtins.property
    @jsii.member(jsii_name="resourcePath")
    def resource_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourcePath"))

    @resource_path.setter
    def resource_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86983409107aebcbe0f571bc7213b15286e074e3f803cdf0f2d2570ceb5af951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePath", value)

    @builtins.property
    @jsii.member(jsii_name="routingControlArn")
    def routing_control_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingControlArn"))

    @routing_control_arn.setter
    def routing_control_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d510a50a8b0db3c8dc7324e6b7a8712f5505e4b57ecad0756634058a4a46e85a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingControlArn", value)

    @builtins.property
    @jsii.member(jsii_name="searchString")
    def search_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "searchString"))

    @search_string.setter
    def search_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__353b3fc6b187aa43e8ce85e3f3f7c1cff34c556db5a7af77b443d1a132d487db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "searchString", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f629ff55e9222a5e84271036b86555b6249ee682adb459cef044d15416c0c3be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b486f3f3e8aa3de133dd57c7a6db0796ea51820d824394fd313e501b661f0840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77df144940aeda9710c870760f5dc4b14bfcef460e8d8655c351350f2ac65cee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.route53HealthCheck.Route53HealthCheckConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "type": "type",
        "child_healthchecks": "childHealthchecks",
        "child_health_threshold": "childHealthThreshold",
        "cloudwatch_alarm_name": "cloudwatchAlarmName",
        "cloudwatch_alarm_region": "cloudwatchAlarmRegion",
        "disabled": "disabled",
        "enable_sni": "enableSni",
        "failure_threshold": "failureThreshold",
        "fqdn": "fqdn",
        "id": "id",
        "insufficient_data_health_status": "insufficientDataHealthStatus",
        "invert_healthcheck": "invertHealthcheck",
        "ip_address": "ipAddress",
        "measure_latency": "measureLatency",
        "port": "port",
        "reference_name": "referenceName",
        "regions": "regions",
        "request_interval": "requestInterval",
        "resource_path": "resourcePath",
        "routing_control_arn": "routingControlArn",
        "search_string": "searchString",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class Route53HealthCheckConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        type: builtins.str,
        child_healthchecks: typing.Optional[typing.Sequence[builtins.str]] = None,
        child_health_threshold: typing.Optional[jsii.Number] = None,
        cloudwatch_alarm_name: typing.Optional[builtins.str] = None,
        cloudwatch_alarm_region: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_sni: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        failure_threshold: typing.Optional[jsii.Number] = None,
        fqdn: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        insufficient_data_health_status: typing.Optional[builtins.str] = None,
        invert_healthcheck: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_address: typing.Optional[builtins.str] = None,
        measure_latency: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        port: typing.Optional[jsii.Number] = None,
        reference_name: typing.Optional[builtins.str] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_interval: typing.Optional[jsii.Number] = None,
        resource_path: typing.Optional[builtins.str] = None,
        routing_control_arn: typing.Optional[builtins.str] = None,
        search_string: typing.Optional[builtins.str] = None,
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
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#type Route53HealthCheck#type}.
        :param child_healthchecks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#child_healthchecks Route53HealthCheck#child_healthchecks}.
        :param child_health_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#child_health_threshold Route53HealthCheck#child_health_threshold}.
        :param cloudwatch_alarm_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#cloudwatch_alarm_name Route53HealthCheck#cloudwatch_alarm_name}.
        :param cloudwatch_alarm_region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#cloudwatch_alarm_region Route53HealthCheck#cloudwatch_alarm_region}.
        :param disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#disabled Route53HealthCheck#disabled}.
        :param enable_sni: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#enable_sni Route53HealthCheck#enable_sni}.
        :param failure_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#failure_threshold Route53HealthCheck#failure_threshold}.
        :param fqdn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#fqdn Route53HealthCheck#fqdn}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#id Route53HealthCheck#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param insufficient_data_health_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#insufficient_data_health_status Route53HealthCheck#insufficient_data_health_status}.
        :param invert_healthcheck: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#invert_healthcheck Route53HealthCheck#invert_healthcheck}.
        :param ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#ip_address Route53HealthCheck#ip_address}.
        :param measure_latency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#measure_latency Route53HealthCheck#measure_latency}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#port Route53HealthCheck#port}.
        :param reference_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#reference_name Route53HealthCheck#reference_name}.
        :param regions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#regions Route53HealthCheck#regions}.
        :param request_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#request_interval Route53HealthCheck#request_interval}.
        :param resource_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#resource_path Route53HealthCheck#resource_path}.
        :param routing_control_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#routing_control_arn Route53HealthCheck#routing_control_arn}.
        :param search_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#search_string Route53HealthCheck#search_string}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#tags Route53HealthCheck#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#tags_all Route53HealthCheck#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10fcb8e2932f8fa3063375a5b928b9c2972d277a5f317be1d7fed889a8f2399c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument child_healthchecks", value=child_healthchecks, expected_type=type_hints["child_healthchecks"])
            check_type(argname="argument child_health_threshold", value=child_health_threshold, expected_type=type_hints["child_health_threshold"])
            check_type(argname="argument cloudwatch_alarm_name", value=cloudwatch_alarm_name, expected_type=type_hints["cloudwatch_alarm_name"])
            check_type(argname="argument cloudwatch_alarm_region", value=cloudwatch_alarm_region, expected_type=type_hints["cloudwatch_alarm_region"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument enable_sni", value=enable_sni, expected_type=type_hints["enable_sni"])
            check_type(argname="argument failure_threshold", value=failure_threshold, expected_type=type_hints["failure_threshold"])
            check_type(argname="argument fqdn", value=fqdn, expected_type=type_hints["fqdn"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument insufficient_data_health_status", value=insufficient_data_health_status, expected_type=type_hints["insufficient_data_health_status"])
            check_type(argname="argument invert_healthcheck", value=invert_healthcheck, expected_type=type_hints["invert_healthcheck"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument measure_latency", value=measure_latency, expected_type=type_hints["measure_latency"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument reference_name", value=reference_name, expected_type=type_hints["reference_name"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            check_type(argname="argument request_interval", value=request_interval, expected_type=type_hints["request_interval"])
            check_type(argname="argument resource_path", value=resource_path, expected_type=type_hints["resource_path"])
            check_type(argname="argument routing_control_arn", value=routing_control_arn, expected_type=type_hints["routing_control_arn"])
            check_type(argname="argument search_string", value=search_string, expected_type=type_hints["search_string"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
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
        if child_healthchecks is not None:
            self._values["child_healthchecks"] = child_healthchecks
        if child_health_threshold is not None:
            self._values["child_health_threshold"] = child_health_threshold
        if cloudwatch_alarm_name is not None:
            self._values["cloudwatch_alarm_name"] = cloudwatch_alarm_name
        if cloudwatch_alarm_region is not None:
            self._values["cloudwatch_alarm_region"] = cloudwatch_alarm_region
        if disabled is not None:
            self._values["disabled"] = disabled
        if enable_sni is not None:
            self._values["enable_sni"] = enable_sni
        if failure_threshold is not None:
            self._values["failure_threshold"] = failure_threshold
        if fqdn is not None:
            self._values["fqdn"] = fqdn
        if id is not None:
            self._values["id"] = id
        if insufficient_data_health_status is not None:
            self._values["insufficient_data_health_status"] = insufficient_data_health_status
        if invert_healthcheck is not None:
            self._values["invert_healthcheck"] = invert_healthcheck
        if ip_address is not None:
            self._values["ip_address"] = ip_address
        if measure_latency is not None:
            self._values["measure_latency"] = measure_latency
        if port is not None:
            self._values["port"] = port
        if reference_name is not None:
            self._values["reference_name"] = reference_name
        if regions is not None:
            self._values["regions"] = regions
        if request_interval is not None:
            self._values["request_interval"] = request_interval
        if resource_path is not None:
            self._values["resource_path"] = resource_path
        if routing_control_arn is not None:
            self._values["routing_control_arn"] = routing_control_arn
        if search_string is not None:
            self._values["search_string"] = search_string
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
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#type Route53HealthCheck#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def child_healthchecks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#child_healthchecks Route53HealthCheck#child_healthchecks}.'''
        result = self._values.get("child_healthchecks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def child_health_threshold(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#child_health_threshold Route53HealthCheck#child_health_threshold}.'''
        result = self._values.get("child_health_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cloudwatch_alarm_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#cloudwatch_alarm_name Route53HealthCheck#cloudwatch_alarm_name}.'''
        result = self._values.get("cloudwatch_alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudwatch_alarm_region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#cloudwatch_alarm_region Route53HealthCheck#cloudwatch_alarm_region}.'''
        result = self._values.get("cloudwatch_alarm_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#disabled Route53HealthCheck#disabled}.'''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_sni(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#enable_sni Route53HealthCheck#enable_sni}.'''
        result = self._values.get("enable_sni")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#failure_threshold Route53HealthCheck#failure_threshold}.'''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fqdn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#fqdn Route53HealthCheck#fqdn}.'''
        result = self._values.get("fqdn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#id Route53HealthCheck#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insufficient_data_health_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#insufficient_data_health_status Route53HealthCheck#insufficient_data_health_status}.'''
        result = self._values.get("insufficient_data_health_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_healthcheck(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#invert_healthcheck Route53HealthCheck#invert_healthcheck}.'''
        result = self._values.get("invert_healthcheck")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#ip_address Route53HealthCheck#ip_address}.'''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def measure_latency(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#measure_latency Route53HealthCheck#measure_latency}.'''
        result = self._values.get("measure_latency")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#port Route53HealthCheck#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def reference_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#reference_name Route53HealthCheck#reference_name}.'''
        result = self._values.get("reference_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#regions Route53HealthCheck#regions}.'''
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def request_interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#request_interval Route53HealthCheck#request_interval}.'''
        result = self._values.get("request_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#resource_path Route53HealthCheck#resource_path}.'''
        result = self._values.get("resource_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_control_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#routing_control_arn Route53HealthCheck#routing_control_arn}.'''
        result = self._values.get("routing_control_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def search_string(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#search_string Route53HealthCheck#search_string}.'''
        result = self._values.get("search_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#tags Route53HealthCheck#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/route53_health_check#tags_all Route53HealthCheck#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Route53HealthCheckConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Route53HealthCheck",
    "Route53HealthCheckConfig",
]

publication.publish()

def _typecheckingstub__e9552a76b0db10a01bed3d1a6691c7eed74ba27ecb921dbf79c83c010f08dbfd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    type: builtins.str,
    child_healthchecks: typing.Optional[typing.Sequence[builtins.str]] = None,
    child_health_threshold: typing.Optional[jsii.Number] = None,
    cloudwatch_alarm_name: typing.Optional[builtins.str] = None,
    cloudwatch_alarm_region: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_sni: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    failure_threshold: typing.Optional[jsii.Number] = None,
    fqdn: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    insufficient_data_health_status: typing.Optional[builtins.str] = None,
    invert_healthcheck: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ip_address: typing.Optional[builtins.str] = None,
    measure_latency: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    port: typing.Optional[jsii.Number] = None,
    reference_name: typing.Optional[builtins.str] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_interval: typing.Optional[jsii.Number] = None,
    resource_path: typing.Optional[builtins.str] = None,
    routing_control_arn: typing.Optional[builtins.str] = None,
    search_string: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__45788cc35dc7d57c7caac31d818dc38b4d66d1e8589e53f08985528419d44a5f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffb45ea7384da4fe762b26273d6598e6fb1d9e7562b2b05db1143bc52a2cda40(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86fbe73f164bfd858edaf8cdaf7d61ed6a3429e285a6f8305f8527c0c8d83d46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a0f5cad60d3e767a8666638a878432ade3ed9c865f33a63bb03eef96075c9ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f700c6012441fb9d24874833fb7ed98535e6f942c34273de8aa3ff99ee9a078e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79127f181d32b775eb3ba6e86bd135d36891b57c45eb844f7fc0078fb4babef8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad669aa8f427b85e94cf27b82c932332ac364bcd89e45c905e04ed03302c7b7f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5beaf3fc239ed7296de5dce4501e45eaf1510183afb295e421756c8e1bd720a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e715d0f8c1972396460a19231b2a7b4554b7a25b1db50bd9df740bdc0ccfceed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d43b6f448a086064ce0275d956e07b79e1131ec415134dd05a881d0964ac926(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c06f30a1604341424f4005ea3ca3e52a73e4559749c281d4683c9f5cba865ed(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__201bb8ac18f77f7786543be573df7de66e77b53b7e50d5fbc11aae057dfd0df4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__687ec1992f70e4fc0f30c7041bdb1ef2f9aaa07fd0ac6a1c60a94144ce7411e7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6296f25e611ace8448c519628dc58ef926cda0d30555bb7c3ab8b1c00522d0e7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a927fa5c9432134a95f96c1b7190068fc2ea37665faaf4d1b4c00a7011c0ae2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f8417064226f5e55a73d887152942fb7ba410c8e19e10c2ad234c6a3ef8781e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394e5831d97f438651f53f3c6a40bc225f8e4e86353a9fde2a7fb278451f235c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86983409107aebcbe0f571bc7213b15286e074e3f803cdf0f2d2570ceb5af951(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d510a50a8b0db3c8dc7324e6b7a8712f5505e4b57ecad0756634058a4a46e85a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__353b3fc6b187aa43e8ce85e3f3f7c1cff34c556db5a7af77b443d1a132d487db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f629ff55e9222a5e84271036b86555b6249ee682adb459cef044d15416c0c3be(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b486f3f3e8aa3de133dd57c7a6db0796ea51820d824394fd313e501b661f0840(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77df144940aeda9710c870760f5dc4b14bfcef460e8d8655c351350f2ac65cee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10fcb8e2932f8fa3063375a5b928b9c2972d277a5f317be1d7fed889a8f2399c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    type: builtins.str,
    child_healthchecks: typing.Optional[typing.Sequence[builtins.str]] = None,
    child_health_threshold: typing.Optional[jsii.Number] = None,
    cloudwatch_alarm_name: typing.Optional[builtins.str] = None,
    cloudwatch_alarm_region: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_sni: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    failure_threshold: typing.Optional[jsii.Number] = None,
    fqdn: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    insufficient_data_health_status: typing.Optional[builtins.str] = None,
    invert_healthcheck: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ip_address: typing.Optional[builtins.str] = None,
    measure_latency: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    port: typing.Optional[jsii.Number] = None,
    reference_name: typing.Optional[builtins.str] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_interval: typing.Optional[jsii.Number] = None,
    resource_path: typing.Optional[builtins.str] = None,
    routing_control_arn: typing.Optional[builtins.str] = None,
    search_string: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
