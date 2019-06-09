import pytest

import asyncio
from asynctest import mock_open, patch
from asynctest.mock import call
from scripts.AccessUrl import AccessUrl

@pytest.yield_fixture
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

#With test data file_content:
# _fetch is called 3 times
# _fetch function is called with parameters f1, f2, f3
#With return value of mock object:
# _write is called with parameters "cannot connect\n", "cannot connect\n", "cannot connect\n" 	
def test_fetch_write(event_loop):
    file_content = (
        'f1 1\n'
        'f2 2\n'
        'f3 3\n'
    )
    m = mock_open(read_data = file_content)    
    m.return_value.__iter__ = lambda self : iter(self.readline, '')
    with patch("builtins.open", m) as mock_file1, patch.object(AccessUrl, '_fetch',return_value=("cannot connect",[])) as MockHelper:
        access = AccessUrl(event_loop,'path1','path2')
        event_loop.run_until_complete(access())

        assert MockHelper.call_count == 3
        calls = [call('f1'), call('f2'), call('f3')]
        MockHelper.assert_has_calls(calls, any_order=True)

        calls2 = [call("cannot connect\n"), call("cannot connect\n"), call("cannot connect\n")]
        mock_file1().write.assert_has_calls(calls2, any_order=True)
 
 
  
 
