# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: bookstore.proto
# Protobuf Python Version: 5.28.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    3,
    '',
    'bookstore.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0f\x62ookstore.proto\x12\tbookstore\"<\n\x06\x41uthor\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0b\n\x03\x61ge\x18\x03 \x01(\x05\x12\x0b\n\x03\x62io\x18\x04 \x01(\t\"s\n\x04\x42ook\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x10\n\x08subtitle\x18\x03 \x01(\t\x12\x0c\n\x04year\x18\x04 \x01(\x05\x12!\n\x06\x61uthor\x18\x05 \x01(\x0b\x32\x11.bookstore.Author\x12\r\n\x05price\x18\x06 \x01(\x01\"+\n\tBookstore\x12\x1e\n\x05\x62ooks\x18\x01 \x03(\x0b\x32\x0f.bookstore.Bookb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'bookstore_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_AUTHOR']._serialized_start=30
  _globals['_AUTHOR']._serialized_end=90
  _globals['_BOOK']._serialized_start=92
  _globals['_BOOK']._serialized_end=207
  _globals['_BOOKSTORE']._serialized_start=209
  _globals['_BOOKSTORE']._serialized_end=252
# @@protoc_insertion_point(module_scope)