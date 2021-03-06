#! /usr/bin/env python
from __future__ import absolute_import
'''test configure module.'''

import pytest
from jmclient import (load_program_config, jm_single, get_irc_mchannels,
                      BTC_P2PK_VBYTE, BTC_P2SH_VBYTE, validate_address,
                      JsonRpcConnectionError)
from jmclient.configure import (get_config_irc_channel, get_p2sh_vbyte,
                                get_p2pk_vbyte, get_blockchain_interface_instance)
import jmbitcoin as bitcoin
import copy
import os

def test_attribute_dict():
    from jmclient.configure import AttributeDict
    ad = AttributeDict(foo=1, bar=2, baz={"x":3, "y":4})
    assert ad.foo == 1
    assert ad.bar == 2
    assert ad.baz.x == 3
    assert ad["foo"] == 1

def test_load_config():
    load_program_config(bs="regtest")
    os.makedirs("dummydirforconfig")
    ncp = os.path.join(os.getcwd(), "dummydirforconfig")
    jm_single().config_location = "joinmarket.cfg"
    #TODO hack: load from default implies a connection error unless
    #actually mainnet, but tests cannot; for now catch the connection error
    with pytest.raises(JsonRpcConnectionError) as e_info:
        load_program_config(config_path=ncp, bs="regtest")
    assert str(e_info.value) in ["authentication for JSON-RPC failed",
                                 "JSON-RPC connection failed. Err:error(111, 'Connection refused')"]
    os.remove("dummydirforconfig/joinmarket.cfg")
    os.removedirs("dummydirforconfig")
    jm_single().config_location = "joinmarket.cfg"
    load_program_config()

def test_config_get_irc_channel():
    load_program_config()
    channel = "dummy"
    assert get_config_irc_channel(channel) == "#dummy-test"
    jm_single().config.set("BLOCKCHAIN", "network", "mainnet")
    assert get_config_irc_channel(channel) == "#dummy"
    get_irc_mchannels()
    load_program_config()

def test_net_byte():
    load_program_config()
    assert get_p2pk_vbyte() == 0x6f
    assert get_p2sh_vbyte() == 196

def test_blockchain_sources():
    load_program_config()
    for src in ["electrum", "dummy"]:
        jm_single().config.set("BLOCKCHAIN", "blockchain_source", src)
        if src=="electrum":
            jm_single().config.set("BLOCKCHAIN", "network", "mainnet")
        if src == "dummy":
            with pytest.raises(ValueError) as e_info:
                get_blockchain_interface_instance(jm_single().config)
        else:
            get_blockchain_interface_instance(jm_single().config)
    load_program_config()

        

        
    