from iana_protocol_numbers.protocol_numbers import IANAProtocolNumbers

def test_load_local():
    protocol_numbers = IANAProtocolNumbers(load_local=True)
    assert len(protocol_numbers.protocol_numbers) > 0

def test_load_latest():
    protocol_numbers = IANAProtocolNumbers(load_local=False)
    assert len(protocol_numbers.protocol_numbers) > 0

def test_number_to_keyword():
    protocol_numbers = IANAProtocolNumbers(load_local=True)
    assert protocol_numbers.number_to_keyword(0) == "HOPOPT"

def test_keyword_to_number():
    protocol_numbers = IANAProtocolNumbers(load_local=True)
    assert protocol_numbers.keyword_to_number("HOPOPT") == 0

def test_number_to_keyword_not_found():
    protocol_numbers = IANAProtocolNumbers(load_local=True)
    assert protocol_numbers.number_to_keyword(444) == None

def test_keyword_to_number_not_found():
    protocol_numbers = IANAProtocolNumbers(load_local=True)
    assert protocol_numbers.keyword_to_number("NOT_FOUND") == -1
