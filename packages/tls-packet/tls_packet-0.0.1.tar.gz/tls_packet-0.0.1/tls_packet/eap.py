# -------------------------------------------------------------------------
# Copyright 2023-2023, Boling Consulting Solutions, bcsw.net
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License
# -------------------------------------------------------------------------

# pylint: disable=missing-docstring, line-too-long, too-many-statements, too-many-arguments, too-many-locals, too-many-nested-blocks, too-many-branches, broad-except, invalid-name, no-self-use


from enum import Enum
from typing import Union

import struct

EAP_HDR_LEN = 1 + 1 + 2
EAP_TYPE_LEN = 1

# Used to map an EapType with their respective parser
PARSERS = {}
PARSERS_TYPES = {}


class EapCode(Enum):
    REQUEST = 1
    RESPONSE = 2
    SUCCESS = 3
    FAILURE = 4
    INITIALIZE = 5
    FINISH = 6


_eap_code_dict = {
    EapCode.REQUEST:    "Request",
    EapCode.RESPONSE:   "Response",
    EapCode.SUCCESS:    "Success",
    EapCode.FAILURE:    "Failure",
    EapCode.INITIALIZE: "Initiate",
    EapCode.FINISH:     "Finish"
}


class EapType(Enum):
    IDENTITY = 1
    LEGACY_NAK = 3
    MD5_CHALLENGE = 4
    TLS = 13
    TTLS = 21
    PEAP = 25


eap_type_dict = {
    0:                     "Reserved",
    EapType.IDENTITY:      "Identity",
    2:                     "Notification",
    EapType.LEGACY_NAK:    "Legacy Nak",
    4:                     "MD5-Challenge",
    EapType.MD5_CHALLENGE: "One-Time Password (OTP)",
    6:                     "Generic Token Card (GTC)",
    7:                     "Allocated - RFC3748",
    8:                     "Allocated - RFC3748",
    9:                     "RSA Public Key Authentication",
    10:                    "DSS Unilateral",
    11:                    "KEA",
    12:                    "KEA-VALIDATE",
    EapType.TLS:           "EAP-TLS",
    14:                    "Defender Token (AXENT)",
    15:                    "RSA Security SecurID EAP",
    16:                    "Arcot Systems EAP",
    17:                    "EAP-Cisco Wireless",
    18:                    "GSM Subscriber Identity Modules (EAP-SIM)",
    19:                    "SRP-SHA1",
    20:                    "Unassigned",
    EapType.TTLS:          "EAP-TTLS",
    22:                    "Remote Access Service",
    23:                    "EAP-AKA Authentication",
    24:                    "EAP-3Com Wireless",
    EapType.PEAP:          "PEAP",
    26:                    "MS-EAP-Authentication",
    27:                    "Mutual Authentication w/Key Exchange (MAKE)",
    28:                    "CRYPTOCard",
    29:                    "EAP-MSCHAP-V2",
    30:                    "DynamID",
    31:                    "Rob EAP",
    32:                    "Protected One-Time Password",
    33:                    "MS-Authentication-TLV",
    34:                    "SentriNET",
    35:                    "EAP-Actiontec Wireless",
    36:                    "Cogent Systems Biometrics Authentication EAP",
    37:                    "AirFortress EAP",
    38:                    "EAP-HTTP Digest",
    39:                    "SecureSuite EAP",
    40:                    "DeviceConnect EAP",
    41:                    "EAP-SPEKE",
    42:                    "EAP-MOBAC",
    43:                    "EAP-FAST",
    44:                    "ZoneLabs EAP (ZLXEAP)",
    45:                    "EAP-Link",
    46:                    "EAP-PAX",
    47:                    "EAP-PSK",
    48:                    "EAP-SAKE",
    49:                    "EAP-IKEv2",
    50:                    "EAP-AKA",
    51:                    "EAP-GPSK",
    52:                    "EAP-pwd",
    53:                    "EAP-EKE Version 1",
    54:                    "EAP Method Type for PT-EAP",
    55:                    "TEAP",
    254:                   "Reserved for the Expanded Type",
    255:                   "Experimental",
}


def register_parser(cls):
    """Register a packet type to the parser"""
    PARSERS[cls.PACKET_TYPE] = cls.parse
    PARSERS_TYPES[cls.PACKET_TYPE] = cls
    return cls


class Eap:
    """ Packet/parser for Eap messages """
    code = None
    packet_id = None
    PACKET_TYPE = None

    @staticmethod
    def parse(packed_message: bytes) -> Union['Eap', None]:
        try:
            code, packet_id, length = struct.unpack("!BBH", packed_message[:EAP_HDR_LEN])
        except struct.error as exception:
            raise exception  # Provided for breakpoint purposes

        if code in (EapCode.REQUEST.value, EapCode.RESPONSE.value):
            try:
                packet_type, = struct.unpack("!B", packed_message[EAP_HDR_LEN: EAP_HDR_LEN + EAP_TYPE_LEN])
            except struct.error as exception:
                raise exception  # Provided for breakpoint purposes

            data = packed_message[EAP_HDR_LEN + EAP_TYPE_LEN:length]
            try:
                return PARSERS[EapType(packet_type)](code, packet_id, data)

            except KeyError as exception:
                raise exception  # Provided for breakpoint purposes

        elif code == EapCode.SUCCESS.value:
            return EapSuccess(packet_id)

        elif code == EapCode.FAILURE.value:
            return EapFailure(packet_id)

        else:
            raise NotImplementedError(f"EAP: Code point {code} is not yet supported")

    def pack(self, packed_body: bytes) -> bytes:
        """Pack an EAP Message"""
        header = struct.pack("!BBHB", self.code, self.packet_id,
                             EAP_HDR_LEN + EAP_TYPE_LEN + len(packed_body),
                             self.PACKET_TYPE.value)
        return header + packed_body


class EapSuccess(Eap):
    """EAP Success Packet"""

    def __init__(self, packet_id: int):
        self.packet_id = packet_id

    @classmethod
    def parse(cls, packet_id: int) -> 'EapSuccess':
        return cls(packet_id)

    def pack(self) -> bytes:
        return struct.pack("!BBH", EapCode.SUCCESS.value, self.packet_id, EAP_HDR_LEN)

    def __repr__(self):
        return f"{self.__class__.__name__}(packet_id={self.packet_id}"


class EapFailure(Eap):
    """EAP Failure Packet"""

    def __init__(self, packet_id: int):
        self.packet_id = packet_id

    @classmethod
    def parse(cls, packet_id: int) -> 'EapFailure':
        return cls(packet_id)

    def pack(self) -> bytes:
        return struct.pack("!BBH", EapCode.FAILURE.value, self.packet_id, EAP_HDR_LEN)

    def __repr__(self):
        return f"{self.__class__.__name__}(packet_id={self.packet_id})"


@register_parser
class EapIdentity(Eap):
    """ EAP Identity packet """
    PACKET_TYPE = EapType.IDENTITY

    def __init__(self, code: int, packet_id: int, identity: str = None):
        self.code = code
        self.packet_id = packet_id
        self.identity = identity

    @classmethod
    def parse(cls, code: int, packet_id: int, packed_message: bytes) -> 'EapIdentity':
        try:
            identity = packed_message.decode()
        except UnicodeDecodeError as exception:
            # raise MessageParseError("%s unable to decode identity" % cls.__name__) from exception
            raise exception
        return cls(code, packet_id, identity)

    def pack(self) -> bytes:
        if self.identity:
            packed_identity = self.identity.encode()
            return super().pack(packed_identity)
        return super().pack(b'')

    def __repr__(self):
        return f"{self.__class__.__name__}(identity={self.identity}, code={self.code}, packet_id={self.packet_id})"


@register_parser
class EapMd5Challenge(Eap):
    """EAP MD5-Challenge Packet"""
    PACKET_TYPE = EapType.MD5_CHALLENGE

    def __init__(self, code: int, packet_id: int, challenge: bytes, extra_data: bytes = b""):
        self.code = code
        self.packet_id = packet_id
        self.challenge = challenge
        self.extra_data = extra_data

    @classmethod
    def parse(cls, code: int, packet_id: int, packed_message: bytes) -> 'EapMd5Challenge':
        try:
            value_length, = struct.unpack("!B", packed_message[:1])
        except struct.error as exception:
            raise exception
        challenge = packed_message[1:1 + value_length]
        extra_data = packed_message[1 + value_length:]
        return cls(code, packet_id, challenge, extra_data)

    def pack(self) -> bytes:
        value_length = struct.pack("!B", len(self.challenge))
        packed_md5_challenge = value_length + self.challenge + self.extra_data
        return super().pack(packed_md5_challenge)

    def __repr__(self):
        return f"{self.__class__.__name__}(challenge={self.challenge}, extra_data='{self.extra_data.hex()}')"


@register_parser
class EapLegacyNak(Eap):
    """EAP Legacy-NAK Packet"""
    PACKET_TYPE = EapType.LEGACY_NAK

    def __init__(self, code: int, packet_id: int, desired_auth_types):
        self.code = code
        self.packet_id = packet_id
        self.desired_auth_types = desired_auth_types

    @classmethod
    def parse(cls, code, packet_id, packed_msg) -> 'EapLegacyNak':
        value_len = len(packed_msg)
        try:
            desired_auth_types = struct.unpack("!%ds" % value_len, packed_msg)
        except struct.error as exception:
            raise exception
        return cls(code, packet_id, desired_auth_types)

    def pack(self) -> bytes:
        packed_legacy_nak = struct.pack("!%ds" % len(self.desired_auth_types),
                                        *self.desired_auth_types)  # pytype: disable=wrong-arg-types
        return super().pack(packed_legacy_nak)

    def __repr__(self):
        return f"{self.__class__.__name__}(packet_id={self.packet_id}, desired_auth_types={self.desired_auth_types})"


class EapTLSBase(Eap):
    """EAPTLS & EAPTTLS have the same packet format."""

    def __init__(self, code: int, packet_id: int, flags, extra_data):
        self.code = code
        self.packet_id = packet_id
        self.flags = flags
        self.extra_data = extra_data

    def __str__(self):
        data_len = len(self.extra_data)
        # Note: Hex dump is 2 octets per bytre of data...
        hex_limit = 128
        return f"{self.__class__.__name__}: packet_id: {self.packet_id}, flags: {self.flags}/0x{self.flags:02x}, " + \
            f"extra_data: {data_len} : '{self.extra_data.hex()[:(hex_limit * 2)]}{'...' if data_len > hex_limit else ''}'"

    @classmethod
    def parse(cls, code: int, packet_id: int, packed_msg: bytes) -> 'EapTLSBase':
        value_len = len(packed_msg)
        fmt_str = "!B"
        if value_len > 1:
            fmt_str += "%ds" % (value_len - 1)
        try:
            unpacked = struct.unpack(fmt_str, packed_msg)
        except struct.error as exception:
            raise exception
        extra_data = b""
        if value_len > 1:
            flags, extra_data = unpacked
        else:
            flags = unpacked[0]

        return cls(code, packet_id, flags, extra_data)

    def pack(self) -> bytes:
        if self.extra_data:
            packed = struct.pack("!B%ds" % len(self.extra_data), self.flags, self.extra_data)
        else:
            packed = struct.pack("!B", self.flags)
        return super().pack(packed)

    def __repr__(self):
        return f"{self.__class__.__name__}(packet_id={self.packet_id}, flags={self.flags}, extra_data='{self.extra_data.hex()}')"


@register_parser
class EapTLS(EapTLSBase):
    """EAP TLS Packet"""
    PACKET_TYPE = EapType.TLS


@register_parser
class EapTTLS(EapTLSBase):
    """EAP TTLS Packet"""
    PACKET_TYPE = EapType.TTLS


@register_parser
class EapPEAP(EapTLSBase):
    """PEAP Packet"""
    PACKET_TYPE = EapType.PEAP
