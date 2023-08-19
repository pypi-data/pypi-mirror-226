'''
# `aws_s3_object_copy`

Refer to the Terraform Registory for docs: [`aws_s3_object_copy`](https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy).
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


class S3ObjectCopy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.s3ObjectCopy.S3ObjectCopy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy aws_s3_object_copy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        bucket: builtins.str,
        key: builtins.str,
        source: builtins.str,
        acl: typing.Optional[builtins.str] = None,
        bucket_key_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cache_control: typing.Optional[builtins.str] = None,
        content_disposition: typing.Optional[builtins.str] = None,
        content_encoding: typing.Optional[builtins.str] = None,
        content_language: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
        copy_if_match: typing.Optional[builtins.str] = None,
        copy_if_modified_since: typing.Optional[builtins.str] = None,
        copy_if_none_match: typing.Optional[builtins.str] = None,
        copy_if_unmodified_since: typing.Optional[builtins.str] = None,
        customer_algorithm: typing.Optional[builtins.str] = None,
        customer_key: typing.Optional[builtins.str] = None,
        customer_key_md5: typing.Optional[builtins.str] = None,
        expected_bucket_owner: typing.Optional[builtins.str] = None,
        expected_source_bucket_owner: typing.Optional[builtins.str] = None,
        expires: typing.Optional[builtins.str] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        grant: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3ObjectCopyGrant", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_encryption_context: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_directive: typing.Optional[builtins.str] = None,
        object_lock_legal_hold_status: typing.Optional[builtins.str] = None,
        object_lock_mode: typing.Optional[builtins.str] = None,
        object_lock_retain_until_date: typing.Optional[builtins.str] = None,
        request_payer: typing.Optional[builtins.str] = None,
        server_side_encryption: typing.Optional[builtins.str] = None,
        source_customer_algorithm: typing.Optional[builtins.str] = None,
        source_customer_key: typing.Optional[builtins.str] = None,
        source_customer_key_md5: typing.Optional[builtins.str] = None,
        storage_class: typing.Optional[builtins.str] = None,
        tagging_directive: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        website_redirect: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy aws_s3_object_copy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#bucket S3ObjectCopy#bucket}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#key S3ObjectCopy#key}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#source S3ObjectCopy#source}.
        :param acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#acl S3ObjectCopy#acl}.
        :param bucket_key_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#bucket_key_enabled S3ObjectCopy#bucket_key_enabled}.
        :param cache_control: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#cache_control S3ObjectCopy#cache_control}.
        :param content_disposition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#content_disposition S3ObjectCopy#content_disposition}.
        :param content_encoding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#content_encoding S3ObjectCopy#content_encoding}.
        :param content_language: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#content_language S3ObjectCopy#content_language}.
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#content_type S3ObjectCopy#content_type}.
        :param copy_if_match: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#copy_if_match S3ObjectCopy#copy_if_match}.
        :param copy_if_modified_since: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#copy_if_modified_since S3ObjectCopy#copy_if_modified_since}.
        :param copy_if_none_match: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#copy_if_none_match S3ObjectCopy#copy_if_none_match}.
        :param copy_if_unmodified_since: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#copy_if_unmodified_since S3ObjectCopy#copy_if_unmodified_since}.
        :param customer_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#customer_algorithm S3ObjectCopy#customer_algorithm}.
        :param customer_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#customer_key S3ObjectCopy#customer_key}.
        :param customer_key_md5: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#customer_key_md5 S3ObjectCopy#customer_key_md5}.
        :param expected_bucket_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#expected_bucket_owner S3ObjectCopy#expected_bucket_owner}.
        :param expected_source_bucket_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#expected_source_bucket_owner S3ObjectCopy#expected_source_bucket_owner}.
        :param expires: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#expires S3ObjectCopy#expires}.
        :param force_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#force_destroy S3ObjectCopy#force_destroy}.
        :param grant: grant block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#grant S3ObjectCopy#grant}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#id S3ObjectCopy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_encryption_context: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#kms_encryption_context S3ObjectCopy#kms_encryption_context}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#kms_key_id S3ObjectCopy#kms_key_id}.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#metadata S3ObjectCopy#metadata}.
        :param metadata_directive: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#metadata_directive S3ObjectCopy#metadata_directive}.
        :param object_lock_legal_hold_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#object_lock_legal_hold_status S3ObjectCopy#object_lock_legal_hold_status}.
        :param object_lock_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#object_lock_mode S3ObjectCopy#object_lock_mode}.
        :param object_lock_retain_until_date: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#object_lock_retain_until_date S3ObjectCopy#object_lock_retain_until_date}.
        :param request_payer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#request_payer S3ObjectCopy#request_payer}.
        :param server_side_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#server_side_encryption S3ObjectCopy#server_side_encryption}.
        :param source_customer_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#source_customer_algorithm S3ObjectCopy#source_customer_algorithm}.
        :param source_customer_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#source_customer_key S3ObjectCopy#source_customer_key}.
        :param source_customer_key_md5: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#source_customer_key_md5 S3ObjectCopy#source_customer_key_md5}.
        :param storage_class: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#storage_class S3ObjectCopy#storage_class}.
        :param tagging_directive: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#tagging_directive S3ObjectCopy#tagging_directive}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#tags S3ObjectCopy#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#tags_all S3ObjectCopy#tags_all}.
        :param website_redirect: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#website_redirect S3ObjectCopy#website_redirect}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__127d837d295517d79c8522d5c41412cf3f3898adbe8aa8e89bb5cc6371a5bbf1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = S3ObjectCopyConfig(
            bucket=bucket,
            key=key,
            source=source,
            acl=acl,
            bucket_key_enabled=bucket_key_enabled,
            cache_control=cache_control,
            content_disposition=content_disposition,
            content_encoding=content_encoding,
            content_language=content_language,
            content_type=content_type,
            copy_if_match=copy_if_match,
            copy_if_modified_since=copy_if_modified_since,
            copy_if_none_match=copy_if_none_match,
            copy_if_unmodified_since=copy_if_unmodified_since,
            customer_algorithm=customer_algorithm,
            customer_key=customer_key,
            customer_key_md5=customer_key_md5,
            expected_bucket_owner=expected_bucket_owner,
            expected_source_bucket_owner=expected_source_bucket_owner,
            expires=expires,
            force_destroy=force_destroy,
            grant=grant,
            id=id,
            kms_encryption_context=kms_encryption_context,
            kms_key_id=kms_key_id,
            metadata=metadata,
            metadata_directive=metadata_directive,
            object_lock_legal_hold_status=object_lock_legal_hold_status,
            object_lock_mode=object_lock_mode,
            object_lock_retain_until_date=object_lock_retain_until_date,
            request_payer=request_payer,
            server_side_encryption=server_side_encryption,
            source_customer_algorithm=source_customer_algorithm,
            source_customer_key=source_customer_key,
            source_customer_key_md5=source_customer_key_md5,
            storage_class=storage_class,
            tagging_directive=tagging_directive,
            tags=tags,
            tags_all=tags_all,
            website_redirect=website_redirect,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putGrant")
    def put_grant(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3ObjectCopyGrant", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea4790450fd3bccb9313c9577a68141b3852635abcabbb96e97b56d06fbb9df1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGrant", [value]))

    @jsii.member(jsii_name="resetAcl")
    def reset_acl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcl", []))

    @jsii.member(jsii_name="resetBucketKeyEnabled")
    def reset_bucket_key_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketKeyEnabled", []))

    @jsii.member(jsii_name="resetCacheControl")
    def reset_cache_control(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheControl", []))

    @jsii.member(jsii_name="resetContentDisposition")
    def reset_content_disposition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentDisposition", []))

    @jsii.member(jsii_name="resetContentEncoding")
    def reset_content_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentEncoding", []))

    @jsii.member(jsii_name="resetContentLanguage")
    def reset_content_language(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentLanguage", []))

    @jsii.member(jsii_name="resetContentType")
    def reset_content_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentType", []))

    @jsii.member(jsii_name="resetCopyIfMatch")
    def reset_copy_if_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyIfMatch", []))

    @jsii.member(jsii_name="resetCopyIfModifiedSince")
    def reset_copy_if_modified_since(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyIfModifiedSince", []))

    @jsii.member(jsii_name="resetCopyIfNoneMatch")
    def reset_copy_if_none_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyIfNoneMatch", []))

    @jsii.member(jsii_name="resetCopyIfUnmodifiedSince")
    def reset_copy_if_unmodified_since(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyIfUnmodifiedSince", []))

    @jsii.member(jsii_name="resetCustomerAlgorithm")
    def reset_customer_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerAlgorithm", []))

    @jsii.member(jsii_name="resetCustomerKey")
    def reset_customer_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerKey", []))

    @jsii.member(jsii_name="resetCustomerKeyMd5")
    def reset_customer_key_md5(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerKeyMd5", []))

    @jsii.member(jsii_name="resetExpectedBucketOwner")
    def reset_expected_bucket_owner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpectedBucketOwner", []))

    @jsii.member(jsii_name="resetExpectedSourceBucketOwner")
    def reset_expected_source_bucket_owner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpectedSourceBucketOwner", []))

    @jsii.member(jsii_name="resetExpires")
    def reset_expires(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpires", []))

    @jsii.member(jsii_name="resetForceDestroy")
    def reset_force_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceDestroy", []))

    @jsii.member(jsii_name="resetGrant")
    def reset_grant(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrant", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsEncryptionContext")
    def reset_kms_encryption_context(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsEncryptionContext", []))

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetMetadataDirective")
    def reset_metadata_directive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataDirective", []))

    @jsii.member(jsii_name="resetObjectLockLegalHoldStatus")
    def reset_object_lock_legal_hold_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectLockLegalHoldStatus", []))

    @jsii.member(jsii_name="resetObjectLockMode")
    def reset_object_lock_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectLockMode", []))

    @jsii.member(jsii_name="resetObjectLockRetainUntilDate")
    def reset_object_lock_retain_until_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectLockRetainUntilDate", []))

    @jsii.member(jsii_name="resetRequestPayer")
    def reset_request_payer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestPayer", []))

    @jsii.member(jsii_name="resetServerSideEncryption")
    def reset_server_side_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerSideEncryption", []))

    @jsii.member(jsii_name="resetSourceCustomerAlgorithm")
    def reset_source_customer_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceCustomerAlgorithm", []))

    @jsii.member(jsii_name="resetSourceCustomerKey")
    def reset_source_customer_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceCustomerKey", []))

    @jsii.member(jsii_name="resetSourceCustomerKeyMd5")
    def reset_source_customer_key_md5(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceCustomerKeyMd5", []))

    @jsii.member(jsii_name="resetStorageClass")
    def reset_storage_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageClass", []))

    @jsii.member(jsii_name="resetTaggingDirective")
    def reset_tagging_directive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaggingDirective", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetWebsiteRedirect")
    def reset_website_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebsiteRedirect", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="expiration")
    def expiration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiration"))

    @builtins.property
    @jsii.member(jsii_name="grant")
    def grant(self) -> "S3ObjectCopyGrantList":
        return typing.cast("S3ObjectCopyGrantList", jsii.get(self, "grant"))

    @builtins.property
    @jsii.member(jsii_name="lastModified")
    def last_modified(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModified"))

    @builtins.property
    @jsii.member(jsii_name="requestCharged")
    def request_charged(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "requestCharged"))

    @builtins.property
    @jsii.member(jsii_name="sourceVersionId")
    def source_version_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceVersionId"))

    @builtins.property
    @jsii.member(jsii_name="versionId")
    def version_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionId"))

    @builtins.property
    @jsii.member(jsii_name="aclInput")
    def acl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aclInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketKeyEnabledInput")
    def bucket_key_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bucketKeyEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheControlInput")
    def cache_control_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheControlInput"))

    @builtins.property
    @jsii.member(jsii_name="contentDispositionInput")
    def content_disposition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentDispositionInput"))

    @builtins.property
    @jsii.member(jsii_name="contentEncodingInput")
    def content_encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentEncodingInput"))

    @builtins.property
    @jsii.member(jsii_name="contentLanguageInput")
    def content_language_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentLanguageInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="copyIfMatchInput")
    def copy_if_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "copyIfMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="copyIfModifiedSinceInput")
    def copy_if_modified_since_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "copyIfModifiedSinceInput"))

    @builtins.property
    @jsii.member(jsii_name="copyIfNoneMatchInput")
    def copy_if_none_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "copyIfNoneMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="copyIfUnmodifiedSinceInput")
    def copy_if_unmodified_since_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "copyIfUnmodifiedSinceInput"))

    @builtins.property
    @jsii.member(jsii_name="customerAlgorithmInput")
    def customer_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customerAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="customerKeyInput")
    def customer_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customerKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="customerKeyMd5Input")
    def customer_key_md5_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customerKeyMd5Input"))

    @builtins.property
    @jsii.member(jsii_name="expectedBucketOwnerInput")
    def expected_bucket_owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expectedBucketOwnerInput"))

    @builtins.property
    @jsii.member(jsii_name="expectedSourceBucketOwnerInput")
    def expected_source_bucket_owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expectedSourceBucketOwnerInput"))

    @builtins.property
    @jsii.member(jsii_name="expiresInput")
    def expires_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expiresInput"))

    @builtins.property
    @jsii.member(jsii_name="forceDestroyInput")
    def force_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="grantInput")
    def grant_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3ObjectCopyGrant"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3ObjectCopyGrant"]]], jsii.get(self, "grantInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsEncryptionContextInput")
    def kms_encryption_context_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsEncryptionContextInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataDirectiveInput")
    def metadata_directive_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataDirectiveInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="objectLockLegalHoldStatusInput")
    def object_lock_legal_hold_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectLockLegalHoldStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="objectLockModeInput")
    def object_lock_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectLockModeInput"))

    @builtins.property
    @jsii.member(jsii_name="objectLockRetainUntilDateInput")
    def object_lock_retain_until_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectLockRetainUntilDateInput"))

    @builtins.property
    @jsii.member(jsii_name="requestPayerInput")
    def request_payer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestPayerInput"))

    @builtins.property
    @jsii.member(jsii_name="serverSideEncryptionInput")
    def server_side_encryption_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverSideEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceCustomerAlgorithmInput")
    def source_customer_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceCustomerAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceCustomerKeyInput")
    def source_customer_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceCustomerKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceCustomerKeyMd5Input")
    def source_customer_key_md5_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceCustomerKeyMd5Input"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="storageClassInput")
    def storage_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageClassInput"))

    @builtins.property
    @jsii.member(jsii_name="taggingDirectiveInput")
    def tagging_directive_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "taggingDirectiveInput"))

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
    @jsii.member(jsii_name="websiteRedirectInput")
    def website_redirect_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "websiteRedirectInput"))

    @builtins.property
    @jsii.member(jsii_name="acl")
    def acl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acl"))

    @acl.setter
    def acl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05788da5549ad403f5e81fa032f31df31177ca877b6bb4264fe481a4a671a1c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acl", value)

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac72d4a5ed19aeb330bd26ef49fa2ddf9476d64d00db367bd3287e1bed848275)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value)

    @builtins.property
    @jsii.member(jsii_name="bucketKeyEnabled")
    def bucket_key_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bucketKeyEnabled"))

    @bucket_key_enabled.setter
    def bucket_key_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4fe79bd714df9b8e5984d6518c364f98be9535682cdf48153319ed712e6f58f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketKeyEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="cacheControl")
    def cache_control(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheControl"))

    @cache_control.setter
    def cache_control(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a41761ad23a387240eb352ba131cbf8f2f44af9ba92cbe6537d2c89d8785151e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheControl", value)

    @builtins.property
    @jsii.member(jsii_name="contentDisposition")
    def content_disposition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentDisposition"))

    @content_disposition.setter
    def content_disposition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e78229dddea3c0571b2cdbc7f6c95e718fa097605c733e47ff50428c22d16d0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentDisposition", value)

    @builtins.property
    @jsii.member(jsii_name="contentEncoding")
    def content_encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentEncoding"))

    @content_encoding.setter
    def content_encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__104cdcf7f5d517cc9ff153f39c2db993af4c8f260942f22305c93b4d8f7d2ae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentEncoding", value)

    @builtins.property
    @jsii.member(jsii_name="contentLanguage")
    def content_language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentLanguage"))

    @content_language.setter
    def content_language(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c6bab4db7e7071002b1cb15e408f242579bb7beddf6d057a1a169056f1dd149)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentLanguage", value)

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66fecac34a59b569966274a2ad7f08b8b644c736d1f09f01ed6b91138cc2c1ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value)

    @builtins.property
    @jsii.member(jsii_name="copyIfMatch")
    def copy_if_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "copyIfMatch"))

    @copy_if_match.setter
    def copy_if_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57dc38314a02f8a3af35ce0453ed94e69e0b508c59a265fafb89890b561cf2ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyIfMatch", value)

    @builtins.property
    @jsii.member(jsii_name="copyIfModifiedSince")
    def copy_if_modified_since(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "copyIfModifiedSince"))

    @copy_if_modified_since.setter
    def copy_if_modified_since(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d5b6af2d05853c952e8a9312aec0c91cb28017d09cc96939934bd15ccfb321f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyIfModifiedSince", value)

    @builtins.property
    @jsii.member(jsii_name="copyIfNoneMatch")
    def copy_if_none_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "copyIfNoneMatch"))

    @copy_if_none_match.setter
    def copy_if_none_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f64302eb57b504d460cb68ba7d169c687b895a99dbf0b41051573a60a2872a3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyIfNoneMatch", value)

    @builtins.property
    @jsii.member(jsii_name="copyIfUnmodifiedSince")
    def copy_if_unmodified_since(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "copyIfUnmodifiedSince"))

    @copy_if_unmodified_since.setter
    def copy_if_unmodified_since(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac2004dd014da9e46c9ff649a5411c49c8fffce9cb64169ec17bcfdf3ad2943f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyIfUnmodifiedSince", value)

    @builtins.property
    @jsii.member(jsii_name="customerAlgorithm")
    def customer_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerAlgorithm"))

    @customer_algorithm.setter
    def customer_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6b854feba0b26ba83596acc5fcbfe29e833053e85d9d705fedd604469bd4eaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerAlgorithm", value)

    @builtins.property
    @jsii.member(jsii_name="customerKey")
    def customer_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerKey"))

    @customer_key.setter
    def customer_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3e653d22e9ed9d40294c4575c54f7a78f21f18c0f9c8d9c758d8b0d1d4781b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerKey", value)

    @builtins.property
    @jsii.member(jsii_name="customerKeyMd5")
    def customer_key_md5(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerKeyMd5"))

    @customer_key_md5.setter
    def customer_key_md5(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1c1c487bc0d3266b8d2b3f9802104fe153ed1f9cc070353623f81f370761630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerKeyMd5", value)

    @builtins.property
    @jsii.member(jsii_name="expectedBucketOwner")
    def expected_bucket_owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expectedBucketOwner"))

    @expected_bucket_owner.setter
    def expected_bucket_owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eb343a585bbb2272928acd507a5667d8c3c7e3f430db96733a082987337bdae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expectedBucketOwner", value)

    @builtins.property
    @jsii.member(jsii_name="expectedSourceBucketOwner")
    def expected_source_bucket_owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expectedSourceBucketOwner"))

    @expected_source_bucket_owner.setter
    def expected_source_bucket_owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4179977248f1ccf33f63f1bb696160f17919d31866a0c17331d33acafc031194)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expectedSourceBucketOwner", value)

    @builtins.property
    @jsii.member(jsii_name="expires")
    def expires(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expires"))

    @expires.setter
    def expires(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23eff1a7ea1846caab2d93b3c0ce2c9b6969261b63355c871ea42dd6f78ea6c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expires", value)

    @builtins.property
    @jsii.member(jsii_name="forceDestroy")
    def force_destroy(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceDestroy"))

    @force_destroy.setter
    def force_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__146dbb236e8738ecb426d5e09b7d04ba5659dcd631edad62581275a48d676924)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDestroy", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b55e17aacfb3456c2dcb6dc8d55cd7adef85c83cb49714ffaa6e33de156aa75f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6ed81982319104a5e9c2ed412bd974b9988055469bd377f991a127bb54ba7a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="kmsEncryptionContext")
    def kms_encryption_context(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsEncryptionContext"))

    @kms_encryption_context.setter
    def kms_encryption_context(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ab0d01aaeca16398e2b0366fcf817f771f993c2feb9eec34996eb361897286)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsEncryptionContext", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dbc9038812ac748eb69d3395b3a567ab2237b8a888744cda37488ad965c7c62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56de5d75a4d2f558b08cfebec9e10d4673a58da04f32d43266d86394fd3f0077)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value)

    @builtins.property
    @jsii.member(jsii_name="metadataDirective")
    def metadata_directive(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataDirective"))

    @metadata_directive.setter
    def metadata_directive(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ac617d81bb103d696f2e968439a351e9129e6dad486aee4ab3dfac26e24534)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataDirective", value)

    @builtins.property
    @jsii.member(jsii_name="objectLockLegalHoldStatus")
    def object_lock_legal_hold_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectLockLegalHoldStatus"))

    @object_lock_legal_hold_status.setter
    def object_lock_legal_hold_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f18b3cff964464e4ce5ccf39edc867785e3834c3745c276e87d2537cbe1d9eec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectLockLegalHoldStatus", value)

    @builtins.property
    @jsii.member(jsii_name="objectLockMode")
    def object_lock_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectLockMode"))

    @object_lock_mode.setter
    def object_lock_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6e3a7456afa4662bc8e4e9e4b12c02c0d28b9ab3718963eb8eb89250f92277c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectLockMode", value)

    @builtins.property
    @jsii.member(jsii_name="objectLockRetainUntilDate")
    def object_lock_retain_until_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectLockRetainUntilDate"))

    @object_lock_retain_until_date.setter
    def object_lock_retain_until_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__385519a6a92e7b5cf1c24a956d75be7df530cc50b49648919f51cc0f2c1b50f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectLockRetainUntilDate", value)

    @builtins.property
    @jsii.member(jsii_name="requestPayer")
    def request_payer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestPayer"))

    @request_payer.setter
    def request_payer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a236b28ca0b50943990d4cc1a5422bf8dc9c8c40261d145dedf640a03091d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestPayer", value)

    @builtins.property
    @jsii.member(jsii_name="serverSideEncryption")
    def server_side_encryption(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverSideEncryption"))

    @server_side_encryption.setter
    def server_side_encryption(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb9552cfa69b3ffbeb985880c43520d410f2c3d538424b131dfc759f2ea30335)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverSideEncryption", value)

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1bbc672d222361b020724c86b33a2edc6915dd7ff6a145970ee13a8b6753976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value)

    @builtins.property
    @jsii.member(jsii_name="sourceCustomerAlgorithm")
    def source_customer_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceCustomerAlgorithm"))

    @source_customer_algorithm.setter
    def source_customer_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8d04b473ee3e8d8782ddb9574dc9afb09b1208380cc9a5497c80fc730ce6f4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceCustomerAlgorithm", value)

    @builtins.property
    @jsii.member(jsii_name="sourceCustomerKey")
    def source_customer_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceCustomerKey"))

    @source_customer_key.setter
    def source_customer_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f379197b76c8c86c9830103706b427a417eb426bb1783edb41f2b4260b62433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceCustomerKey", value)

    @builtins.property
    @jsii.member(jsii_name="sourceCustomerKeyMd5")
    def source_customer_key_md5(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceCustomerKeyMd5"))

    @source_customer_key_md5.setter
    def source_customer_key_md5(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1ca783dff3511d21264b58fe90f65cee8b9c15d748695734fe48021e0afe657)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceCustomerKeyMd5", value)

    @builtins.property
    @jsii.member(jsii_name="storageClass")
    def storage_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageClass"))

    @storage_class.setter
    def storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eba5eeb30de6ddd679c42b4fcb20a9f2708ad0acf053fc1f05fbb6331b58486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClass", value)

    @builtins.property
    @jsii.member(jsii_name="taggingDirective")
    def tagging_directive(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taggingDirective"))

    @tagging_directive.setter
    def tagging_directive(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e5a87fb95ca9e3be0da6219d75dea3bddc8d5548e46e1f972d1530ce10b0f6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taggingDirective", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dbd4d61432cc3d5123829777b490d7eba238311ae9e4c8547ff34755b5d8c42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6b0971d2cca172d74279f636f2053df0af338ea6828577014175c2bd6c6864e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)

    @builtins.property
    @jsii.member(jsii_name="websiteRedirect")
    def website_redirect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "websiteRedirect"))

    @website_redirect.setter
    def website_redirect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed601269e61cacdc6c9e51a311b511afad03cc2aeafbeb75c22c9600a1ec628)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "websiteRedirect", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.s3ObjectCopy.S3ObjectCopyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bucket": "bucket",
        "key": "key",
        "source": "source",
        "acl": "acl",
        "bucket_key_enabled": "bucketKeyEnabled",
        "cache_control": "cacheControl",
        "content_disposition": "contentDisposition",
        "content_encoding": "contentEncoding",
        "content_language": "contentLanguage",
        "content_type": "contentType",
        "copy_if_match": "copyIfMatch",
        "copy_if_modified_since": "copyIfModifiedSince",
        "copy_if_none_match": "copyIfNoneMatch",
        "copy_if_unmodified_since": "copyIfUnmodifiedSince",
        "customer_algorithm": "customerAlgorithm",
        "customer_key": "customerKey",
        "customer_key_md5": "customerKeyMd5",
        "expected_bucket_owner": "expectedBucketOwner",
        "expected_source_bucket_owner": "expectedSourceBucketOwner",
        "expires": "expires",
        "force_destroy": "forceDestroy",
        "grant": "grant",
        "id": "id",
        "kms_encryption_context": "kmsEncryptionContext",
        "kms_key_id": "kmsKeyId",
        "metadata": "metadata",
        "metadata_directive": "metadataDirective",
        "object_lock_legal_hold_status": "objectLockLegalHoldStatus",
        "object_lock_mode": "objectLockMode",
        "object_lock_retain_until_date": "objectLockRetainUntilDate",
        "request_payer": "requestPayer",
        "server_side_encryption": "serverSideEncryption",
        "source_customer_algorithm": "sourceCustomerAlgorithm",
        "source_customer_key": "sourceCustomerKey",
        "source_customer_key_md5": "sourceCustomerKeyMd5",
        "storage_class": "storageClass",
        "tagging_directive": "taggingDirective",
        "tags": "tags",
        "tags_all": "tagsAll",
        "website_redirect": "websiteRedirect",
    },
)
class S3ObjectCopyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bucket: builtins.str,
        key: builtins.str,
        source: builtins.str,
        acl: typing.Optional[builtins.str] = None,
        bucket_key_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cache_control: typing.Optional[builtins.str] = None,
        content_disposition: typing.Optional[builtins.str] = None,
        content_encoding: typing.Optional[builtins.str] = None,
        content_language: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
        copy_if_match: typing.Optional[builtins.str] = None,
        copy_if_modified_since: typing.Optional[builtins.str] = None,
        copy_if_none_match: typing.Optional[builtins.str] = None,
        copy_if_unmodified_since: typing.Optional[builtins.str] = None,
        customer_algorithm: typing.Optional[builtins.str] = None,
        customer_key: typing.Optional[builtins.str] = None,
        customer_key_md5: typing.Optional[builtins.str] = None,
        expected_bucket_owner: typing.Optional[builtins.str] = None,
        expected_source_bucket_owner: typing.Optional[builtins.str] = None,
        expires: typing.Optional[builtins.str] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        grant: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3ObjectCopyGrant", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_encryption_context: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_directive: typing.Optional[builtins.str] = None,
        object_lock_legal_hold_status: typing.Optional[builtins.str] = None,
        object_lock_mode: typing.Optional[builtins.str] = None,
        object_lock_retain_until_date: typing.Optional[builtins.str] = None,
        request_payer: typing.Optional[builtins.str] = None,
        server_side_encryption: typing.Optional[builtins.str] = None,
        source_customer_algorithm: typing.Optional[builtins.str] = None,
        source_customer_key: typing.Optional[builtins.str] = None,
        source_customer_key_md5: typing.Optional[builtins.str] = None,
        storage_class: typing.Optional[builtins.str] = None,
        tagging_directive: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        website_redirect: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#bucket S3ObjectCopy#bucket}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#key S3ObjectCopy#key}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#source S3ObjectCopy#source}.
        :param acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#acl S3ObjectCopy#acl}.
        :param bucket_key_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#bucket_key_enabled S3ObjectCopy#bucket_key_enabled}.
        :param cache_control: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#cache_control S3ObjectCopy#cache_control}.
        :param content_disposition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#content_disposition S3ObjectCopy#content_disposition}.
        :param content_encoding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#content_encoding S3ObjectCopy#content_encoding}.
        :param content_language: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#content_language S3ObjectCopy#content_language}.
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#content_type S3ObjectCopy#content_type}.
        :param copy_if_match: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#copy_if_match S3ObjectCopy#copy_if_match}.
        :param copy_if_modified_since: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#copy_if_modified_since S3ObjectCopy#copy_if_modified_since}.
        :param copy_if_none_match: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#copy_if_none_match S3ObjectCopy#copy_if_none_match}.
        :param copy_if_unmodified_since: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#copy_if_unmodified_since S3ObjectCopy#copy_if_unmodified_since}.
        :param customer_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#customer_algorithm S3ObjectCopy#customer_algorithm}.
        :param customer_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#customer_key S3ObjectCopy#customer_key}.
        :param customer_key_md5: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#customer_key_md5 S3ObjectCopy#customer_key_md5}.
        :param expected_bucket_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#expected_bucket_owner S3ObjectCopy#expected_bucket_owner}.
        :param expected_source_bucket_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#expected_source_bucket_owner S3ObjectCopy#expected_source_bucket_owner}.
        :param expires: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#expires S3ObjectCopy#expires}.
        :param force_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#force_destroy S3ObjectCopy#force_destroy}.
        :param grant: grant block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#grant S3ObjectCopy#grant}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#id S3ObjectCopy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_encryption_context: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#kms_encryption_context S3ObjectCopy#kms_encryption_context}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#kms_key_id S3ObjectCopy#kms_key_id}.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#metadata S3ObjectCopy#metadata}.
        :param metadata_directive: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#metadata_directive S3ObjectCopy#metadata_directive}.
        :param object_lock_legal_hold_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#object_lock_legal_hold_status S3ObjectCopy#object_lock_legal_hold_status}.
        :param object_lock_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#object_lock_mode S3ObjectCopy#object_lock_mode}.
        :param object_lock_retain_until_date: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#object_lock_retain_until_date S3ObjectCopy#object_lock_retain_until_date}.
        :param request_payer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#request_payer S3ObjectCopy#request_payer}.
        :param server_side_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#server_side_encryption S3ObjectCopy#server_side_encryption}.
        :param source_customer_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#source_customer_algorithm S3ObjectCopy#source_customer_algorithm}.
        :param source_customer_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#source_customer_key S3ObjectCopy#source_customer_key}.
        :param source_customer_key_md5: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#source_customer_key_md5 S3ObjectCopy#source_customer_key_md5}.
        :param storage_class: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#storage_class S3ObjectCopy#storage_class}.
        :param tagging_directive: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#tagging_directive S3ObjectCopy#tagging_directive}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#tags S3ObjectCopy#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#tags_all S3ObjectCopy#tags_all}.
        :param website_redirect: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#website_redirect S3ObjectCopy#website_redirect}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75becea80c469798e566dc4f4c8a787d59f30b8b49e600d12e86a661f28c2639)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument acl", value=acl, expected_type=type_hints["acl"])
            check_type(argname="argument bucket_key_enabled", value=bucket_key_enabled, expected_type=type_hints["bucket_key_enabled"])
            check_type(argname="argument cache_control", value=cache_control, expected_type=type_hints["cache_control"])
            check_type(argname="argument content_disposition", value=content_disposition, expected_type=type_hints["content_disposition"])
            check_type(argname="argument content_encoding", value=content_encoding, expected_type=type_hints["content_encoding"])
            check_type(argname="argument content_language", value=content_language, expected_type=type_hints["content_language"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument copy_if_match", value=copy_if_match, expected_type=type_hints["copy_if_match"])
            check_type(argname="argument copy_if_modified_since", value=copy_if_modified_since, expected_type=type_hints["copy_if_modified_since"])
            check_type(argname="argument copy_if_none_match", value=copy_if_none_match, expected_type=type_hints["copy_if_none_match"])
            check_type(argname="argument copy_if_unmodified_since", value=copy_if_unmodified_since, expected_type=type_hints["copy_if_unmodified_since"])
            check_type(argname="argument customer_algorithm", value=customer_algorithm, expected_type=type_hints["customer_algorithm"])
            check_type(argname="argument customer_key", value=customer_key, expected_type=type_hints["customer_key"])
            check_type(argname="argument customer_key_md5", value=customer_key_md5, expected_type=type_hints["customer_key_md5"])
            check_type(argname="argument expected_bucket_owner", value=expected_bucket_owner, expected_type=type_hints["expected_bucket_owner"])
            check_type(argname="argument expected_source_bucket_owner", value=expected_source_bucket_owner, expected_type=type_hints["expected_source_bucket_owner"])
            check_type(argname="argument expires", value=expires, expected_type=type_hints["expires"])
            check_type(argname="argument force_destroy", value=force_destroy, expected_type=type_hints["force_destroy"])
            check_type(argname="argument grant", value=grant, expected_type=type_hints["grant"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_encryption_context", value=kms_encryption_context, expected_type=type_hints["kms_encryption_context"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument metadata_directive", value=metadata_directive, expected_type=type_hints["metadata_directive"])
            check_type(argname="argument object_lock_legal_hold_status", value=object_lock_legal_hold_status, expected_type=type_hints["object_lock_legal_hold_status"])
            check_type(argname="argument object_lock_mode", value=object_lock_mode, expected_type=type_hints["object_lock_mode"])
            check_type(argname="argument object_lock_retain_until_date", value=object_lock_retain_until_date, expected_type=type_hints["object_lock_retain_until_date"])
            check_type(argname="argument request_payer", value=request_payer, expected_type=type_hints["request_payer"])
            check_type(argname="argument server_side_encryption", value=server_side_encryption, expected_type=type_hints["server_side_encryption"])
            check_type(argname="argument source_customer_algorithm", value=source_customer_algorithm, expected_type=type_hints["source_customer_algorithm"])
            check_type(argname="argument source_customer_key", value=source_customer_key, expected_type=type_hints["source_customer_key"])
            check_type(argname="argument source_customer_key_md5", value=source_customer_key_md5, expected_type=type_hints["source_customer_key_md5"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
            check_type(argname="argument tagging_directive", value=tagging_directive, expected_type=type_hints["tagging_directive"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument website_redirect", value=website_redirect, expected_type=type_hints["website_redirect"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "key": key,
            "source": source,
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
        if acl is not None:
            self._values["acl"] = acl
        if bucket_key_enabled is not None:
            self._values["bucket_key_enabled"] = bucket_key_enabled
        if cache_control is not None:
            self._values["cache_control"] = cache_control
        if content_disposition is not None:
            self._values["content_disposition"] = content_disposition
        if content_encoding is not None:
            self._values["content_encoding"] = content_encoding
        if content_language is not None:
            self._values["content_language"] = content_language
        if content_type is not None:
            self._values["content_type"] = content_type
        if copy_if_match is not None:
            self._values["copy_if_match"] = copy_if_match
        if copy_if_modified_since is not None:
            self._values["copy_if_modified_since"] = copy_if_modified_since
        if copy_if_none_match is not None:
            self._values["copy_if_none_match"] = copy_if_none_match
        if copy_if_unmodified_since is not None:
            self._values["copy_if_unmodified_since"] = copy_if_unmodified_since
        if customer_algorithm is not None:
            self._values["customer_algorithm"] = customer_algorithm
        if customer_key is not None:
            self._values["customer_key"] = customer_key
        if customer_key_md5 is not None:
            self._values["customer_key_md5"] = customer_key_md5
        if expected_bucket_owner is not None:
            self._values["expected_bucket_owner"] = expected_bucket_owner
        if expected_source_bucket_owner is not None:
            self._values["expected_source_bucket_owner"] = expected_source_bucket_owner
        if expires is not None:
            self._values["expires"] = expires
        if force_destroy is not None:
            self._values["force_destroy"] = force_destroy
        if grant is not None:
            self._values["grant"] = grant
        if id is not None:
            self._values["id"] = id
        if kms_encryption_context is not None:
            self._values["kms_encryption_context"] = kms_encryption_context
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if metadata is not None:
            self._values["metadata"] = metadata
        if metadata_directive is not None:
            self._values["metadata_directive"] = metadata_directive
        if object_lock_legal_hold_status is not None:
            self._values["object_lock_legal_hold_status"] = object_lock_legal_hold_status
        if object_lock_mode is not None:
            self._values["object_lock_mode"] = object_lock_mode
        if object_lock_retain_until_date is not None:
            self._values["object_lock_retain_until_date"] = object_lock_retain_until_date
        if request_payer is not None:
            self._values["request_payer"] = request_payer
        if server_side_encryption is not None:
            self._values["server_side_encryption"] = server_side_encryption
        if source_customer_algorithm is not None:
            self._values["source_customer_algorithm"] = source_customer_algorithm
        if source_customer_key is not None:
            self._values["source_customer_key"] = source_customer_key
        if source_customer_key_md5 is not None:
            self._values["source_customer_key_md5"] = source_customer_key_md5
        if storage_class is not None:
            self._values["storage_class"] = storage_class
        if tagging_directive is not None:
            self._values["tagging_directive"] = tagging_directive
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if website_redirect is not None:
            self._values["website_redirect"] = website_redirect

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
    def bucket(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#bucket S3ObjectCopy#bucket}.'''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#key S3ObjectCopy#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#source S3ObjectCopy#source}.'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def acl(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#acl S3ObjectCopy#acl}.'''
        result = self._values.get("acl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_key_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#bucket_key_enabled S3ObjectCopy#bucket_key_enabled}.'''
        result = self._values.get("bucket_key_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cache_control(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#cache_control S3ObjectCopy#cache_control}.'''
        result = self._values.get("cache_control")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_disposition(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#content_disposition S3ObjectCopy#content_disposition}.'''
        result = self._values.get("content_disposition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_encoding(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#content_encoding S3ObjectCopy#content_encoding}.'''
        result = self._values.get("content_encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_language(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#content_language S3ObjectCopy#content_language}.'''
        result = self._values.get("content_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#content_type S3ObjectCopy#content_type}.'''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def copy_if_match(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#copy_if_match S3ObjectCopy#copy_if_match}.'''
        result = self._values.get("copy_if_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def copy_if_modified_since(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#copy_if_modified_since S3ObjectCopy#copy_if_modified_since}.'''
        result = self._values.get("copy_if_modified_since")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def copy_if_none_match(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#copy_if_none_match S3ObjectCopy#copy_if_none_match}.'''
        result = self._values.get("copy_if_none_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def copy_if_unmodified_since(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#copy_if_unmodified_since S3ObjectCopy#copy_if_unmodified_since}.'''
        result = self._values.get("copy_if_unmodified_since")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def customer_algorithm(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#customer_algorithm S3ObjectCopy#customer_algorithm}.'''
        result = self._values.get("customer_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def customer_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#customer_key S3ObjectCopy#customer_key}.'''
        result = self._values.get("customer_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def customer_key_md5(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#customer_key_md5 S3ObjectCopy#customer_key_md5}.'''
        result = self._values.get("customer_key_md5")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expected_bucket_owner(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#expected_bucket_owner S3ObjectCopy#expected_bucket_owner}.'''
        result = self._values.get("expected_bucket_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expected_source_bucket_owner(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#expected_source_bucket_owner S3ObjectCopy#expected_source_bucket_owner}.'''
        result = self._values.get("expected_source_bucket_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expires(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#expires S3ObjectCopy#expires}.'''
        result = self._values.get("expires")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#force_destroy S3ObjectCopy#force_destroy}.'''
        result = self._values.get("force_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def grant(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3ObjectCopyGrant"]]]:
        '''grant block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#grant S3ObjectCopy#grant}
        '''
        result = self._values.get("grant")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3ObjectCopyGrant"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#id S3ObjectCopy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_encryption_context(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#kms_encryption_context S3ObjectCopy#kms_encryption_context}.'''
        result = self._values.get("kms_encryption_context")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#kms_key_id S3ObjectCopy#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#metadata S3ObjectCopy#metadata}.'''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata_directive(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#metadata_directive S3ObjectCopy#metadata_directive}.'''
        result = self._values.get("metadata_directive")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_lock_legal_hold_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#object_lock_legal_hold_status S3ObjectCopy#object_lock_legal_hold_status}.'''
        result = self._values.get("object_lock_legal_hold_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_lock_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#object_lock_mode S3ObjectCopy#object_lock_mode}.'''
        result = self._values.get("object_lock_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_lock_retain_until_date(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#object_lock_retain_until_date S3ObjectCopy#object_lock_retain_until_date}.'''
        result = self._values.get("object_lock_retain_until_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_payer(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#request_payer S3ObjectCopy#request_payer}.'''
        result = self._values.get("request_payer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_side_encryption(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#server_side_encryption S3ObjectCopy#server_side_encryption}.'''
        result = self._values.get("server_side_encryption")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_customer_algorithm(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#source_customer_algorithm S3ObjectCopy#source_customer_algorithm}.'''
        result = self._values.get("source_customer_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_customer_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#source_customer_key S3ObjectCopy#source_customer_key}.'''
        result = self._values.get("source_customer_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_customer_key_md5(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#source_customer_key_md5 S3ObjectCopy#source_customer_key_md5}.'''
        result = self._values.get("source_customer_key_md5")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_class(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#storage_class S3ObjectCopy#storage_class}.'''
        result = self._values.get("storage_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tagging_directive(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#tagging_directive S3ObjectCopy#tagging_directive}.'''
        result = self._values.get("tagging_directive")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#tags S3ObjectCopy#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#tags_all S3ObjectCopy#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def website_redirect(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#website_redirect S3ObjectCopy#website_redirect}.'''
        result = self._values.get("website_redirect")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ObjectCopyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.s3ObjectCopy.S3ObjectCopyGrant",
    jsii_struct_bases=[],
    name_mapping={
        "permissions": "permissions",
        "type": "type",
        "email": "email",
        "id": "id",
        "uri": "uri",
    },
)
class S3ObjectCopyGrant:
    def __init__(
        self,
        *,
        permissions: typing.Sequence[builtins.str],
        type: builtins.str,
        email: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param permissions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#permissions S3ObjectCopy#permissions}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#type S3ObjectCopy#type}.
        :param email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#email S3ObjectCopy#email}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#id S3ObjectCopy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#uri S3ObjectCopy#uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6374f9b133b821990a8a71454d83ec71f8c26d276f9329784c008ee8c3d1f0b)
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "permissions": permissions,
            "type": type,
        }
        if email is not None:
            self._values["email"] = email
        if id is not None:
            self._values["id"] = id
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def permissions(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#permissions S3ObjectCopy#permissions}.'''
        result = self._values.get("permissions")
        assert result is not None, "Required property 'permissions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#type S3ObjectCopy#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#email S3ObjectCopy#email}.'''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#id S3ObjectCopy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.13.1/docs/resources/s3_object_copy#uri S3ObjectCopy#uri}.'''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ObjectCopyGrant(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3ObjectCopyGrantList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.s3ObjectCopy.S3ObjectCopyGrantList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__674ec00d9b59ea0c69aea399d360cf6d926aa36bc178acfe4bc9c1337873a8ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "S3ObjectCopyGrantOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9591f6eb0ab1d9a850752194c9e4dbf6e8da426cac6513f4067f2ec2a1ca07d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("S3ObjectCopyGrantOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3700e941529f8623436a5eaacb0f8c4f4b409c1125d3af8eeec6e59ddf19c9db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2f3b681a73f9ec4f36c1fb95fd6174f248afd2f59a5cef36aa6508c1c042ee0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d0165b37e374a3d72157bee65c50b0a0ee050a37ddc842d2ab81d58d119cfbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3ObjectCopyGrant]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3ObjectCopyGrant]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3ObjectCopyGrant]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__972d932bd5f8b9b9f0df7f1a72fc524ed0a0374c34ed7c7f3fcc20652f9c8fb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class S3ObjectCopyGrantOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.s3ObjectCopy.S3ObjectCopyGrantOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b446338a3df842371c123901984b3ed6c20d93e714d9aa51110db9f032b6c0b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetUri")
    def reset_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUri", []))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionsInput")
    def permissions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "permissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d685f6f5a0c669079dd35280cfec22d5ad7566783b038cc60d6fc8314125343b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ec1e919f4486e28a9320ed9d83abeefd6829a1a463708adb31cdb3e59ae8904)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permissions"))

    @permissions.setter
    def permissions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77744385a9121f73260bc291fab0ac295afe9bde1b4c7a2fff59132873cccec0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissions", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fabdbf0821a0167c1e5cd494ebc715bed740ab7a107e40a6471e586cedf7e029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45a86819e1148858ab00f03b06678b02c3a88c0dcb7b9f833f91f29c16530b27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3ObjectCopyGrant]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3ObjectCopyGrant]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3ObjectCopyGrant]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca51a2f403ab3bb2ff7a942d40841389b3de2d7c3f962a727262f34ffcc35186)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "S3ObjectCopy",
    "S3ObjectCopyConfig",
    "S3ObjectCopyGrant",
    "S3ObjectCopyGrantList",
    "S3ObjectCopyGrantOutputReference",
]

publication.publish()

def _typecheckingstub__127d837d295517d79c8522d5c41412cf3f3898adbe8aa8e89bb5cc6371a5bbf1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    bucket: builtins.str,
    key: builtins.str,
    source: builtins.str,
    acl: typing.Optional[builtins.str] = None,
    bucket_key_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cache_control: typing.Optional[builtins.str] = None,
    content_disposition: typing.Optional[builtins.str] = None,
    content_encoding: typing.Optional[builtins.str] = None,
    content_language: typing.Optional[builtins.str] = None,
    content_type: typing.Optional[builtins.str] = None,
    copy_if_match: typing.Optional[builtins.str] = None,
    copy_if_modified_since: typing.Optional[builtins.str] = None,
    copy_if_none_match: typing.Optional[builtins.str] = None,
    copy_if_unmodified_since: typing.Optional[builtins.str] = None,
    customer_algorithm: typing.Optional[builtins.str] = None,
    customer_key: typing.Optional[builtins.str] = None,
    customer_key_md5: typing.Optional[builtins.str] = None,
    expected_bucket_owner: typing.Optional[builtins.str] = None,
    expected_source_bucket_owner: typing.Optional[builtins.str] = None,
    expires: typing.Optional[builtins.str] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    grant: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3ObjectCopyGrant, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_encryption_context: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_directive: typing.Optional[builtins.str] = None,
    object_lock_legal_hold_status: typing.Optional[builtins.str] = None,
    object_lock_mode: typing.Optional[builtins.str] = None,
    object_lock_retain_until_date: typing.Optional[builtins.str] = None,
    request_payer: typing.Optional[builtins.str] = None,
    server_side_encryption: typing.Optional[builtins.str] = None,
    source_customer_algorithm: typing.Optional[builtins.str] = None,
    source_customer_key: typing.Optional[builtins.str] = None,
    source_customer_key_md5: typing.Optional[builtins.str] = None,
    storage_class: typing.Optional[builtins.str] = None,
    tagging_directive: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    website_redirect: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__ea4790450fd3bccb9313c9577a68141b3852635abcabbb96e97b56d06fbb9df1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3ObjectCopyGrant, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05788da5549ad403f5e81fa032f31df31177ca877b6bb4264fe481a4a671a1c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac72d4a5ed19aeb330bd26ef49fa2ddf9476d64d00db367bd3287e1bed848275(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4fe79bd714df9b8e5984d6518c364f98be9535682cdf48153319ed712e6f58f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41761ad23a387240eb352ba131cbf8f2f44af9ba92cbe6537d2c89d8785151e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e78229dddea3c0571b2cdbc7f6c95e718fa097605c733e47ff50428c22d16d0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__104cdcf7f5d517cc9ff153f39c2db993af4c8f260942f22305c93b4d8f7d2ae0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c6bab4db7e7071002b1cb15e408f242579bb7beddf6d057a1a169056f1dd149(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66fecac34a59b569966274a2ad7f08b8b644c736d1f09f01ed6b91138cc2c1ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57dc38314a02f8a3af35ce0453ed94e69e0b508c59a265fafb89890b561cf2ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d5b6af2d05853c952e8a9312aec0c91cb28017d09cc96939934bd15ccfb321f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64302eb57b504d460cb68ba7d169c687b895a99dbf0b41051573a60a2872a3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac2004dd014da9e46c9ff649a5411c49c8fffce9cb64169ec17bcfdf3ad2943f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6b854feba0b26ba83596acc5fcbfe29e833053e85d9d705fedd604469bd4eaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e653d22e9ed9d40294c4575c54f7a78f21f18c0f9c8d9c758d8b0d1d4781b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c1c487bc0d3266b8d2b3f9802104fe153ed1f9cc070353623f81f370761630(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb343a585bbb2272928acd507a5667d8c3c7e3f430db96733a082987337bdae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4179977248f1ccf33f63f1bb696160f17919d31866a0c17331d33acafc031194(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23eff1a7ea1846caab2d93b3c0ce2c9b6969261b63355c871ea42dd6f78ea6c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__146dbb236e8738ecb426d5e09b7d04ba5659dcd631edad62581275a48d676924(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b55e17aacfb3456c2dcb6dc8d55cd7adef85c83cb49714ffaa6e33de156aa75f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6ed81982319104a5e9c2ed412bd974b9988055469bd377f991a127bb54ba7a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ab0d01aaeca16398e2b0366fcf817f771f993c2feb9eec34996eb361897286(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dbc9038812ac748eb69d3395b3a567ab2237b8a888744cda37488ad965c7c62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56de5d75a4d2f558b08cfebec9e10d4673a58da04f32d43266d86394fd3f0077(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ac617d81bb103d696f2e968439a351e9129e6dad486aee4ab3dfac26e24534(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f18b3cff964464e4ce5ccf39edc867785e3834c3745c276e87d2537cbe1d9eec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6e3a7456afa4662bc8e4e9e4b12c02c0d28b9ab3718963eb8eb89250f92277c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__385519a6a92e7b5cf1c24a956d75be7df530cc50b49648919f51cc0f2c1b50f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a236b28ca0b50943990d4cc1a5422bf8dc9c8c40261d145dedf640a03091d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb9552cfa69b3ffbeb985880c43520d410f2c3d538424b131dfc759f2ea30335(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1bbc672d222361b020724c86b33a2edc6915dd7ff6a145970ee13a8b6753976(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d04b473ee3e8d8782ddb9574dc9afb09b1208380cc9a5497c80fc730ce6f4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f379197b76c8c86c9830103706b427a417eb426bb1783edb41f2b4260b62433(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ca783dff3511d21264b58fe90f65cee8b9c15d748695734fe48021e0afe657(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eba5eeb30de6ddd679c42b4fcb20a9f2708ad0acf053fc1f05fbb6331b58486(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e5a87fb95ca9e3be0da6219d75dea3bddc8d5548e46e1f972d1530ce10b0f6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dbd4d61432cc3d5123829777b490d7eba238311ae9e4c8547ff34755b5d8c42(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b0971d2cca172d74279f636f2053df0af338ea6828577014175c2bd6c6864e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed601269e61cacdc6c9e51a311b511afad03cc2aeafbeb75c22c9600a1ec628(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75becea80c469798e566dc4f4c8a787d59f30b8b49e600d12e86a661f28c2639(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bucket: builtins.str,
    key: builtins.str,
    source: builtins.str,
    acl: typing.Optional[builtins.str] = None,
    bucket_key_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cache_control: typing.Optional[builtins.str] = None,
    content_disposition: typing.Optional[builtins.str] = None,
    content_encoding: typing.Optional[builtins.str] = None,
    content_language: typing.Optional[builtins.str] = None,
    content_type: typing.Optional[builtins.str] = None,
    copy_if_match: typing.Optional[builtins.str] = None,
    copy_if_modified_since: typing.Optional[builtins.str] = None,
    copy_if_none_match: typing.Optional[builtins.str] = None,
    copy_if_unmodified_since: typing.Optional[builtins.str] = None,
    customer_algorithm: typing.Optional[builtins.str] = None,
    customer_key: typing.Optional[builtins.str] = None,
    customer_key_md5: typing.Optional[builtins.str] = None,
    expected_bucket_owner: typing.Optional[builtins.str] = None,
    expected_source_bucket_owner: typing.Optional[builtins.str] = None,
    expires: typing.Optional[builtins.str] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    grant: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3ObjectCopyGrant, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_encryption_context: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_directive: typing.Optional[builtins.str] = None,
    object_lock_legal_hold_status: typing.Optional[builtins.str] = None,
    object_lock_mode: typing.Optional[builtins.str] = None,
    object_lock_retain_until_date: typing.Optional[builtins.str] = None,
    request_payer: typing.Optional[builtins.str] = None,
    server_side_encryption: typing.Optional[builtins.str] = None,
    source_customer_algorithm: typing.Optional[builtins.str] = None,
    source_customer_key: typing.Optional[builtins.str] = None,
    source_customer_key_md5: typing.Optional[builtins.str] = None,
    storage_class: typing.Optional[builtins.str] = None,
    tagging_directive: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    website_redirect: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6374f9b133b821990a8a71454d83ec71f8c26d276f9329784c008ee8c3d1f0b(
    *,
    permissions: typing.Sequence[builtins.str],
    type: builtins.str,
    email: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__674ec00d9b59ea0c69aea399d360cf6d926aa36bc178acfe4bc9c1337873a8ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9591f6eb0ab1d9a850752194c9e4dbf6e8da426cac6513f4067f2ec2a1ca07d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3700e941529f8623436a5eaacb0f8c4f4b409c1125d3af8eeec6e59ddf19c9db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f3b681a73f9ec4f36c1fb95fd6174f248afd2f59a5cef36aa6508c1c042ee0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0165b37e374a3d72157bee65c50b0a0ee050a37ddc842d2ab81d58d119cfbd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__972d932bd5f8b9b9f0df7f1a72fc524ed0a0374c34ed7c7f3fcc20652f9c8fb5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3ObjectCopyGrant]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b446338a3df842371c123901984b3ed6c20d93e714d9aa51110db9f032b6c0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d685f6f5a0c669079dd35280cfec22d5ad7566783b038cc60d6fc8314125343b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec1e919f4486e28a9320ed9d83abeefd6829a1a463708adb31cdb3e59ae8904(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77744385a9121f73260bc291fab0ac295afe9bde1b4c7a2fff59132873cccec0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fabdbf0821a0167c1e5cd494ebc715bed740ab7a107e40a6471e586cedf7e029(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a86819e1148858ab00f03b06678b02c3a88c0dcb7b9f833f91f29c16530b27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca51a2f403ab3bb2ff7a942d40841389b3de2d7c3f962a727262f34ffcc35186(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3ObjectCopyGrant]],
) -> None:
    """Type checking stubs"""
    pass
