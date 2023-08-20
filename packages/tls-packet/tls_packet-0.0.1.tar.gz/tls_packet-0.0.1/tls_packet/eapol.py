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


import ipaddress
import struct
from datetime import datetime, timedelta

from enum import Enum
from dpkt import dhcp
from dpkt import udp
from dpkt import ip6
from dpkt import ethernet


class EapolType(Enum):
    EAP_PACKET = 0
    EAPOL_START = 1
    EAPOL_LOGOFF = 2
    EAPOL_KEY = 3
    EAPOL_ENCAPSULATED_ASF_ALERT = 4
    EAPOL_MKA = 5
    EAPOL_ANNOUNCEMENT_GENERIC = 6
    EAPOL_ANNOUNCEMENT_SPECIFIC = 7
    EAPOL_ANNOUNCEMENT_REQ = 8

    @classmethod
    def has_value(cls, val: int) -> bool:
        return val in cls._value2member_map_


##################################################################################
#
# UMT Defines

ETH_TYPE_802DOT1X = 0x888E
ETH_TYPE_802DOT1Q = 0x8100
ETH_TYPE_802DOT1AD = 0x88a8

##################################################################################
#
# EAPOL Defines

EAPOL_HDR_MIN_SIZE = 4
EAPOL_HDR_EAP_TYPE = 0
EAPOL_HDR_VER_POSITION = 0
EAPOL_HDR_TYPE_POSITION = 1
EAPOL_HDR_LEN_POSITION = 2
EAPOL_START_TYPE = 1
EAPOL_LOGOFF_TYPE = 2

EAPOL_TYPE_DICT = {
    0x0: "EAP-Packet",
    0x1: "EAPOL-Start",
    0x2: "EAPOL-Logoff",
    0x3: "EAPOL-Key",
    0x4: "EAPOL-Encapsulated-ASF-Alert",
    0x5: "EAPOL-MKA",
    0x6: "EAPOL-Announcement (Generic)",
    0x7: "EAPOL-Announcement (Specific)",
    0x8: "EAPOL-Announcement-Req"
}

EAPOL_HDR_LEN = 1 + 1 + 2


class Eapol:
    """Packet/parsers for 802.1x frames"""

    def __init__(self, version: int, packet_type: int, data: bytes):
        self.version = version
        self.packet_type = packet_type
        self.data = data

    @classmethod
    def parse(cls, packed_message: bytes):
        try:
            version, packet_type, length = struct.unpack("!BBH",
                                                         packed_message[:EAPOL_HDR_LEN])
        except struct.error as _ex:
            # TODO: log Error, might want to silently discard malformed packets without raising an exception
            return None
        data = packed_message[EAPOL_HDR_LEN:EAPOL_HDR_LEN + length]
        return cls(version, packet_type, data)

    def pack(self) -> bytes:
        header = struct.pack("!BBH", self.version, self.packet_type, len(self.data))
        return header

    def __repr__(self):
        return f"{self.__class__.__name__,}(version={self.version}, packet_type={self.packet_type}, data={self.data})"

    def __str__(self):
        return f"{self.__class__.__name__}<packet_type={self.packet_type}, data={self.data}>"


class SidecarPacketUtility(object):
    def __init__(self, umt_mongodb=None):
        self.umt_mongodb = umt_mongodb  # Mongodb information

    def eth_does_frame_have_eapol_layer(self, eth_frame):
        _eapol_frame = None

        _len_eth_frame = len(eth_frame)

        # Check that the frame is long enough for src(6), dst(6), type(2) and EAPOL header (4) = 18
        if eth_frame and _len_eth_frame >= 18:
            # Check that the Ethernet frame contains an EAPOL frame
            _tag_frame = eth_frame[12:]

            while _tag_frame:
                # Loop through while there is an 802.1Q or 802.1AD tag to process
                _tag_tpid = struct.unpack_from('>H', _tag_frame, 0)[0]
                _tag_tci = struct.unpack_from('>H', _tag_frame, 2)[0]

                if _tag_tpid == ETH_TYPE_802DOT1Q or _tag_tpid == ETH_TYPE_802DOT1AD:
                    # Move to the next tag
                    _tag_frame = _tag_frame[4:]
                elif _tag_tpid == ETH_TYPE_802DOT1X:
                    # skip past EAPoL ether type (0x888e) to get the EAPOL Frame
                    _eapol_frame = _tag_frame[2:]
                    break
                else:
                    # Invalid tags or frame, stop processing
                    break
        else:
            self.umt_mongodb.umt_log('CNTL', 'DEBUG', self.umt_mongodb.cntl_dev_id, \
                                     f"eth_does_frame_have_eapol_layer - Called with invalid parameter, eth_frame: {eth_frame}, length: {_len_eth_frame}")

        return _eapol_frame

    def from_eth_frame_get_eapol_fields(self, eth_frame):

        _eapol_frame = None
        _eapol_ver = None
        _eapol_type = None
        _eapol_len = None

        # Check that the Ethernet frame contains an EAPOL frame
        _eapol_frame = self.eth_does_frame_have_eapol_layer(eth_frame)

        if _eapol_frame:
            _eapol_ver, _eapol_type, _eapol_len = self.eapol_decode_hdr(_eapol_frame)
        else:
            self.umt_mongodb.umt_log('CNTL', 'DEBUG', self.umt_mongodb.cntl_dev_id, \
                                     f'from_eth_frame_get_eapol_fields - Ethernet frame did not contain any data: {eth_frame}')

        return (_eapol_ver, _eapol_type, _eapol_len)

    ##################################################################################
    #
    # 802.1X EAPOL Packet Utilities

    def eapol_decode_hdr(self, eapol_frame):
        _eapol_ver = None
        _eapol_type = None
        _eapol_len = None

        _eapol_len = len(eapol_frame)

        if eapol_frame is None or len(eapol_frame) >= EAPOL_HDR_MIN_SIZE:
            _eapol_ver = struct.unpack_from('>B', eapol_frame, EAPOL_HDR_VER_POSITION)[0]
            _eapol_type = struct.unpack_from('>B', eapol_frame, EAPOL_HDR_TYPE_POSITION)[0]
            _eapol_len = struct.unpack_from('>H', eapol_frame, EAPOL_HDR_LEN_POSITION)[0]
        else:
            self.umt_mongodb.umt_log('CNTL', 'DEBUG', self.umt_mongodb.cntl_dev_id,
                                     f'eapol_decode_hdr - invalid parameters eapol_frame: {eapol_frame}, eapol length {_eapol_len}')

        return _eapol_ver, _eapol_type, _eapol_len

    def eapol_does_frame_have_eap_layer(self, eapol_frame):
        _haslayer = False

        if eapol_frame:
            # Decode the EAPOL HDR to check type
            _eapol_type = self.eapol_decode_hdr(eapol_frame)[1]

            # Check that the EAPOL HDR contains EAP based on type
            if _eapol_type == EAPOL_HDR_EAP_TYPE:
                _haslayer = True

        return _haslayer

    def eapol_frame_get_eap_fields(self, eapol_frame):
        _eap_code = None
        _eap_id = None
        _eap_len = None
        _eap_type = None

        if eapol_frame:
            # Check that the EAPOL frame contains an EAP frame
            if self.eapol_does_frame_have_eap_layer(eapol_frame):
                _eap_frame = eapol_frame[4:]
                _eap_code, _eap_id, _eap_len = self.decode_eap_hdr(_eap_frame)
        else:
            self.umt_mongodb.umt_log('CNTL', 'DEBUG', self.umt_mongodb.cntl_dev_id, f'eapol_frame_get_eap_fields - invalid parameters, frame: {eapol_frame}')

        return (_eap_code, _eap_id, _eap_len)
