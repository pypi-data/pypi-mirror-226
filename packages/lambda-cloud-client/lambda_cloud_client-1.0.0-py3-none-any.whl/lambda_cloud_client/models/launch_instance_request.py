# coding: utf-8

"""
    Lambda Cloud API

    API for interacting with the Lambda GPU Cloud  # noqa: E501

    The version of the OpenAPI document: 1.4.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import List, Optional
from pydantic import BaseModel, Field, StrictStr, conint, conlist, constr

class LaunchInstanceRequest(BaseModel):
    """
    LaunchInstanceRequest
    """
    region_name: StrictStr = Field(..., description="Short name of a region")
    instance_type_name: StrictStr = Field(..., description="Name of an instance type")
    ssh_key_names: conlist(constr(strict=True, max_length=64), max_items=1, min_items=1) = Field(..., description="Names of the SSH keys to allow access to the instances. Currently, exactly one SSH key must be specified.")
    file_system_names: Optional[conlist(StrictStr, max_items=1)] = Field(None, description="Names of the file systems to attach to the instances. Currently, only one (if any) file system may be specified.")
    quantity: Optional[conint(strict=True, le=1, ge=1)] = Field(1, description="Number of instances to launch")
    name: Optional[constr(strict=True, max_length=64, min_length=1)] = Field(None, description="User-provided name for the instance")
    __properties = ["region_name", "instance_type_name", "ssh_key_names", "file_system_names", "quantity", "name"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LaunchInstanceRequest:
        """Create an instance of LaunchInstanceRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if name (nullable) is None
        # and __fields_set__ contains the field
        if self.name is None and "name" in self.__fields_set__:
            _dict['name'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> LaunchInstanceRequest:
        """Create an instance of LaunchInstanceRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return LaunchInstanceRequest.parse_obj(obj)

        _obj = LaunchInstanceRequest.parse_obj({
            "region_name": obj.get("region_name"),
            "instance_type_name": obj.get("instance_type_name"),
            "ssh_key_names": obj.get("ssh_key_names"),
            "file_system_names": obj.get("file_system_names"),
            "quantity": obj.get("quantity") if obj.get("quantity") is not None else 1,
            "name": obj.get("name")
        })
        return _obj

