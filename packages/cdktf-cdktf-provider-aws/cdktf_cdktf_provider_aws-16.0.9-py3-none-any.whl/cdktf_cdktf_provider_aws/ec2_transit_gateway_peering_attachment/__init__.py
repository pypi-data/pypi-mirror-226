'''
# `aws_ec2_transit_gateway_peering_attachment`

Refer to the Terraform Registory for docs: [`aws_ec2_transit_gateway_peering_attachment`](https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment).
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


class Ec2TransitGatewayPeeringAttachment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ec2TransitGatewayPeeringAttachment.Ec2TransitGatewayPeeringAttachment",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment aws_ec2_transit_gateway_peering_attachment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        peer_region: builtins.str,
        peer_transit_gateway_id: builtins.str,
        transit_gateway_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        peer_account_id: typing.Optional[builtins.str] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment aws_ec2_transit_gateway_peering_attachment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param peer_region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment#peer_region Ec2TransitGatewayPeeringAttachment#peer_region}.
        :param peer_transit_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment#peer_transit_gateway_id Ec2TransitGatewayPeeringAttachment#peer_transit_gateway_id}.
        :param transit_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment#transit_gateway_id Ec2TransitGatewayPeeringAttachment#transit_gateway_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment#id Ec2TransitGatewayPeeringAttachment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param peer_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment#peer_account_id Ec2TransitGatewayPeeringAttachment#peer_account_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment#tags Ec2TransitGatewayPeeringAttachment#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment#tags_all Ec2TransitGatewayPeeringAttachment#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4af17e737b1c71f92d4bca8ec7b8f77cc0fdb7a0652e75e032dbe6aacefafab)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = Ec2TransitGatewayPeeringAttachmentConfig(
            peer_region=peer_region,
            peer_transit_gateway_id=peer_transit_gateway_id,
            transit_gateway_id=transit_gateway_id,
            id=id,
            peer_account_id=peer_account_id,
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

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPeerAccountId")
    def reset_peer_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerAccountId", []))

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
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="peerAccountIdInput")
    def peer_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="peerRegionInput")
    def peer_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="peerTransitGatewayIdInput")
    def peer_transit_gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerTransitGatewayIdInput"))

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
    @jsii.member(jsii_name="transitGatewayIdInput")
    def transit_gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transitGatewayIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80974d38b6f8ed77db8d0f63f4de9c0959832bbd6b74e63ca354c02c5499a566)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="peerAccountId")
    def peer_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerAccountId"))

    @peer_account_id.setter
    def peer_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__353fdf2e7ba0d43dc2adfaab7ecf6931639fd011f88603113328a4fe6ea42713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerAccountId", value)

    @builtins.property
    @jsii.member(jsii_name="peerRegion")
    def peer_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerRegion"))

    @peer_region.setter
    def peer_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83a8164edd7ca40e5ccb327a066f77146800d58970923980c152199914fe3ba4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerRegion", value)

    @builtins.property
    @jsii.member(jsii_name="peerTransitGatewayId")
    def peer_transit_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerTransitGatewayId"))

    @peer_transit_gateway_id.setter
    def peer_transit_gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86a71973540dff9c599a0dad61221c4c60f173e8ef134b54d1676ef4151b75f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerTransitGatewayId", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__748cfa5bd25f6dbea59890386a6e46f6c512448dd63ca1999d13cc701da7387b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15710a797d3c921ccdb532fbd3df0092c68228ee9d99ac656b7ee40e84610936)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)

    @builtins.property
    @jsii.member(jsii_name="transitGatewayId")
    def transit_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayId"))

    @transit_gateway_id.setter
    def transit_gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0048b5ebdaccf02797b0b7fb28477ca790d2e0ee0d01d7bc09d08100517d97d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transitGatewayId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ec2TransitGatewayPeeringAttachment.Ec2TransitGatewayPeeringAttachmentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "peer_region": "peerRegion",
        "peer_transit_gateway_id": "peerTransitGatewayId",
        "transit_gateway_id": "transitGatewayId",
        "id": "id",
        "peer_account_id": "peerAccountId",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class Ec2TransitGatewayPeeringAttachmentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        peer_region: builtins.str,
        peer_transit_gateway_id: builtins.str,
        transit_gateway_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        peer_account_id: typing.Optional[builtins.str] = None,
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
        :param peer_region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment#peer_region Ec2TransitGatewayPeeringAttachment#peer_region}.
        :param peer_transit_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment#peer_transit_gateway_id Ec2TransitGatewayPeeringAttachment#peer_transit_gateway_id}.
        :param transit_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment#transit_gateway_id Ec2TransitGatewayPeeringAttachment#transit_gateway_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment#id Ec2TransitGatewayPeeringAttachment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param peer_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment#peer_account_id Ec2TransitGatewayPeeringAttachment#peer_account_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment#tags Ec2TransitGatewayPeeringAttachment#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment#tags_all Ec2TransitGatewayPeeringAttachment#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9075059820ac4c524a7188159ed7a962bb2cff3db4943bdd3ca76d55fb52ebb9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument peer_region", value=peer_region, expected_type=type_hints["peer_region"])
            check_type(argname="argument peer_transit_gateway_id", value=peer_transit_gateway_id, expected_type=type_hints["peer_transit_gateway_id"])
            check_type(argname="argument transit_gateway_id", value=transit_gateway_id, expected_type=type_hints["transit_gateway_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument peer_account_id", value=peer_account_id, expected_type=type_hints["peer_account_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "peer_region": peer_region,
            "peer_transit_gateway_id": peer_transit_gateway_id,
            "transit_gateway_id": transit_gateway_id,
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
        if peer_account_id is not None:
            self._values["peer_account_id"] = peer_account_id
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
    def peer_region(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment#peer_region Ec2TransitGatewayPeeringAttachment#peer_region}.'''
        result = self._values.get("peer_region")
        assert result is not None, "Required property 'peer_region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peer_transit_gateway_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment#peer_transit_gateway_id Ec2TransitGatewayPeeringAttachment#peer_transit_gateway_id}.'''
        result = self._values.get("peer_transit_gateway_id")
        assert result is not None, "Required property 'peer_transit_gateway_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def transit_gateway_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment#transit_gateway_id Ec2TransitGatewayPeeringAttachment#transit_gateway_id}.'''
        result = self._values.get("transit_gateway_id")
        assert result is not None, "Required property 'transit_gateway_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment#id Ec2TransitGatewayPeeringAttachment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment#peer_account_id Ec2TransitGatewayPeeringAttachment#peer_account_id}.'''
        result = self._values.get("peer_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment#tags Ec2TransitGatewayPeeringAttachment#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/ec2_transit_gateway_peering_attachment#tags_all Ec2TransitGatewayPeeringAttachment#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2TransitGatewayPeeringAttachmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Ec2TransitGatewayPeeringAttachment",
    "Ec2TransitGatewayPeeringAttachmentConfig",
]

publication.publish()

def _typecheckingstub__a4af17e737b1c71f92d4bca8ec7b8f77cc0fdb7a0652e75e032dbe6aacefafab(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    peer_region: builtins.str,
    peer_transit_gateway_id: builtins.str,
    transit_gateway_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    peer_account_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__80974d38b6f8ed77db8d0f63f4de9c0959832bbd6b74e63ca354c02c5499a566(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__353fdf2e7ba0d43dc2adfaab7ecf6931639fd011f88603113328a4fe6ea42713(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a8164edd7ca40e5ccb327a066f77146800d58970923980c152199914fe3ba4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86a71973540dff9c599a0dad61221c4c60f173e8ef134b54d1676ef4151b75f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__748cfa5bd25f6dbea59890386a6e46f6c512448dd63ca1999d13cc701da7387b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15710a797d3c921ccdb532fbd3df0092c68228ee9d99ac656b7ee40e84610936(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0048b5ebdaccf02797b0b7fb28477ca790d2e0ee0d01d7bc09d08100517d97d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9075059820ac4c524a7188159ed7a962bb2cff3db4943bdd3ca76d55fb52ebb9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    peer_region: builtins.str,
    peer_transit_gateway_id: builtins.str,
    transit_gateway_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    peer_account_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
