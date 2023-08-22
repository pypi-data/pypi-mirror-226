'''
---


## author: haimtran
title: create a cognito userpool for web development
date: 20/08/2023

## Cognito Authorizer

When developing an web or mobile application, we usually need a identity provider. So this Construct can be used to create a Cognito UserPool

```python
new CognitoAuthorizer(stack, 'CognitoAuthorizer', {
  userPoolName: 'chatbot',
  userPoolClientName: 'chatbotapp',
});
```

## Usage Guide

There are different use cases, for example

* Use in another CDK Stack
* Create only a UserPool for a web application
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

from ._jsii import *

import constructs as _constructs_77d1e7e8


class CognitoAuthorizer(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-cognito-userpool.CognitoAuthorizer",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        user_pool_client_name: builtins.str,
        user_pool_name: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param user_pool_client_name: 
        :param user_pool_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c10196653c0f59a335e8c865828cf8453e55941023c72906b7f01ca958f75249)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CognitoAuthorizerProps(
            user_pool_client_name=user_pool_client_name, user_pool_name=user_pool_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="userPool")
    def user_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPool"))


@jsii.data_type(
    jsii_type="cdk-cognito-userpool.CognitoAuthorizerProps",
    jsii_struct_bases=[],
    name_mapping={
        "user_pool_client_name": "userPoolClientName",
        "user_pool_name": "userPoolName",
    },
)
class CognitoAuthorizerProps:
    def __init__(
        self,
        *,
        user_pool_client_name: builtins.str,
        user_pool_name: builtins.str,
    ) -> None:
        '''
        :param user_pool_client_name: 
        :param user_pool_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1195c7a621f46c62115540668995cbd0c0de05263818d60a9721059ba623b730)
            check_type(argname="argument user_pool_client_name", value=user_pool_client_name, expected_type=type_hints["user_pool_client_name"])
            check_type(argname="argument user_pool_name", value=user_pool_name, expected_type=type_hints["user_pool_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_pool_client_name": user_pool_client_name,
            "user_pool_name": user_pool_name,
        }

    @builtins.property
    def user_pool_client_name(self) -> builtins.str:
        result = self._values.get("user_pool_client_name")
        assert result is not None, "Required property 'user_pool_client_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_pool_name(self) -> builtins.str:
        result = self._values.get("user_pool_name")
        assert result is not None, "Required property 'user_pool_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoAuthorizerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CognitoAuthorizer",
    "CognitoAuthorizerProps",
]

publication.publish()

def _typecheckingstub__c10196653c0f59a335e8c865828cf8453e55941023c72906b7f01ca958f75249(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    user_pool_client_name: builtins.str,
    user_pool_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1195c7a621f46c62115540668995cbd0c0de05263818d60a9721059ba623b730(
    *,
    user_pool_client_name: builtins.str,
    user_pool_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
