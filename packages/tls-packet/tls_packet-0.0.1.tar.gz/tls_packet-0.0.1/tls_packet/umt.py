

# pylint: disable=missing-docstring, line-too-long, too-many-statements, too-many-arguments, too-many-locals, too-many-nested-blocks, too-many-branches, broad-except, invalid-name, no-self-use


import ipaddress
import struct
from datetime import datetime, timedelta

import dpkt
from dpkt import dhcp
from dpkt import udp
from dpkt import ip
from dpkt import ethernet

##################################################################################
#
# UMT Defines

UMT_VERSION = 1
UMT_TLV_LEN = 6
UMT_VER1_HDR_LEN = 9
UMT_HEADER_START = 0
UMT_ENCAPSULATED_FRAME_START = 9

UMT_MIN_FRAME_SIZE = 9

ENCAP_CHANNEL = 0xEC
ENCAP_CHANNEL_SUBTYPE_POSITION = 0
ENCAP_CHANNEL_LEN_POSITION = 1
ENCAP_CHANNEL_VER_POSITION = 3
ENCAP_CHANNEL_CHANID_POSITION = 5
ENCAP_CHANNEL_CHANINFO_POSITION = 7

##################################################################################
#
# ETH Defines

ETH_P_UMT = 0xa8c8
ETH_TYPE_802DOT1Q = 0x8100
ETH_TYPE_802DOT1AD = 0x88a8


class UMT:
    def __init__(self):
        pass

    ##################################################################################
    #
    # UMT Packet Utilities

    def umt_remove_header(self, umt_frame):
        _ret_frame = None

        if umt_frame:
            if len(umt_frame) >= UMT_ENCAPSULATED_FRAME_START:
                # If the frame is long enough remove the header
                _ret_frame = (umt_frame[UMT_ENCAPSULATED_FRAME_START:])
            else:
                # Frame was shorter than allowed
                self.umt_mongodb.umt_log('CNTL', 'DEBUG', self.umt_mongodb.cntl_dev_id,
                                         f"umt_remove_header called with invalid UMT frame (too short): {umt_frame}")
        else:
            # UMT frame was none
            self.umt_mongodb.umt_log('CNTL', 'DEBUG', self.umt_mongodb.cntl_dev_id, f"umt_remove_header called with invalid UMT frame: {umt_frame}")

        return _ret_frame

    def umt_encode_hdr(self, hdr_len, hdr_ver, chan_id, chan_info):
        _umt_hdr = struct.pack('>B', ENCAP_CHANNEL)
        _umt_hdr += struct.pack('>H', hdr_len)
        _umt_hdr += struct.pack('>H', hdr_ver)
        _umt_hdr += struct.pack('>H', chan_id)
        _umt_hdr += struct.pack('>H', chan_info)
        return _umt_hdr

    def decode_umt_hdr(self, umt_frame):
        _sub_type = None
        _umt_len = None
        _umt_ver = None
        _umt_chan_id = None
        _umt_chan_info = None

        if umt_frame and len(umt_frame) >= UMT_MIN_FRAME_SIZE:
            _subtype, _umt_len, _umt_ver, _umt_chan_id, _umt_chan_info = struct.unpack_from('>BHHHH', umt_frame, ENCAP_CHANNEL_SUBTYPE_POSITION)

        else:
            # UMT frame was none or length was not long enough
            self.umt_mongodb.umt_log('CNTL', 'DEBUG', self.umt_mongodb.cntl_dev_id,
                                     f"decode_umt_hdr called with invalid UMT frame: {umt_frame}, length: {len(umt_frame)}")

        return _subtype, _umt_len, _umt_ver, _umt_chan_id, _umt_chan_info

    def umt_validate_header(self, umt_frame):
        _valid_umt_hdr = True

        if umt_frame:

            _umt_len = len(umt_frame)
            if _umt_len < UMT_VER1_HDR_LEN:
                self.umt_mongodb.umt_log('CNTL', 'DEBUG', self.umt_mongodb.cntl_dev_id, \
                                         f"umt_validate_header - UMT frame is not long enough for header, length: {_umt_len}")

                # The frame length is shorter than the required header size, stop processing and return
                return False

            _subtype, _umt_len, _umt_ver, _umt_chan_id, _umt_chan_info = self.decode_umt_hdr(umt_frame)

            # Check for a valid UMT SubType
            if _subtype != ENCAP_CHANNEL:
                _valid_umt_hdr = False
                # Do not log invalid UMT SubTypes, since this can happen with the other host applications running
                # on the same interface

            # Check for a valid UMT header len
            elif _umt_len != UMT_TLV_LEN:
                _valid_umt_hdr = False
                self.umt_mongodb.umt_log('CNTL', 'DEBUG', self.umt_mongodb.cntl_dev_id, \
                                         f"umt_validate_header - UMT header has an invalid length: {_umt_len}")

            # Check for a valid UMT version
            elif _umt_ver != 1:
                _valid_umt_hdr = False
                self.umt_mongodb.umt_log('CNTL', 'DEBUG', self.umt_mongodb.cntl_dev_id, \
                                         f"umt_validate_header - UMT header has an invalid version: {_umt_ver}")

        else:
            self.umt_mongodb.umt_log('CNTL', 'DEBUG', self.umt_mongodb.cntl_dev_id, \
                                     f"umt_validate_header - Called with invalid umt_frame parameter, umt_frame: {umt_frame}")

        return _valid_umt_hdr

    def umt_add_hdr_to_frame(self, frame, fdb_entry, direction):
        _ret_frame = None

        if frame and fdb_entry:
            # Create the UMT Header
            _umt_hdr = self.umt_encode_hdr(fdb_entry.dict['ec_tlv_length'],
                                           fdb_entry.dict['ec_version'],
                                           direction,
                                           fdb_entry.dict['ec_tx_chan_info'])
            # Add the UMT header to the frame
            _ret_frame = _umt_hdr + frame
        else:
            # There was an error with the parameters
            self.umt_mongodb.umt_log('CNTL', 'DEBUG', self.umt_mongodb.cntl_dev_id, \
                                     f"umt_add_hdr_to_frame called with invalid parameters UMT frame: {frame}, fdb_entry: {fdb_entry}")

        return _ret_frame
