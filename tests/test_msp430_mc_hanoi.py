from angr_platforms.msp430 import *
import angr
import nose


def test_hanoi():
    p = angr.Project("../test_programs/msp430/microcorruption_hanoi/out.elf", load_options={'rebase_granularity': 8})
    p.hook_symbol('getsn', simos_msp430.MCgetsn())
    p.hook_symbol('__stop_progExec__', simos_msp430.MCstopexec())
    p.hook_symbol('puts', simos_msp430.MCputs())
    simgr = p.factory.simgr()
    simgr.explore(find=p.loader.find_symbol('unlock_door').rebased_addr)
    stdin_contents = simgr.found[0].posix.dumps(0)
    nose.tools.assert_equals(stdin_contents.encode('hex'), '00000000000000000000000000000000960000000000000000000000')

if __name__ == '__main__':
    test_hanoi()