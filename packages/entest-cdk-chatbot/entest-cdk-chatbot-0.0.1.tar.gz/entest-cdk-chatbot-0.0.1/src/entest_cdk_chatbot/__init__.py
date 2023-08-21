'''
---


## author: haimtran
title: deploy a next chatbot on amazon ecs
date: 20/08/2023
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


class QueueRecorder(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="entest-cdk-chatbot.QueueRecorder",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        function_name: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param function_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__889230a4f38278b33415cb6307ac3c3460668f9507732799ee45df78548656d5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = QueueRecorderProps(function_name=function_name)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="entest-cdk-chatbot.QueueRecorderProps",
    jsii_struct_bases=[],
    name_mapping={"function_name": "functionName"},
)
class QueueRecorderProps:
    def __init__(self, *, function_name: builtins.str) -> None:
        '''
        :param function_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1c5cd3be1bc900307541182c8fe2df418ff5c28cb4f2fd4f3ee419f157503b0)
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_name": function_name,
        }

    @builtins.property
    def function_name(self) -> builtins.str:
        result = self._values.get("function_name")
        assert result is not None, "Required property 'function_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QueueRecorderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "QueueRecorder",
    "QueueRecorderProps",
]

publication.publish()

def _typecheckingstub__889230a4f38278b33415cb6307ac3c3460668f9507732799ee45df78548656d5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    function_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1c5cd3be1bc900307541182c8fe2df418ff5c28cb4f2fd4f3ee419f157503b0(
    *,
    function_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
