# name=VFXSeqAssist

"""
    Do some stuff involving the VFX Sequencer plugin
    version:0.01
    author:dustractor
    repository: https://github.com/dustractor/vfxseqassist
    tested with FL Studio version 21.2.2[build 3914]
"""

import midi,plugins,ui

RANDOMIZER_PAD = 20
PARAMINFO_PAD = 21
COPY_PAD = 22
PASTE_PAD = 23
_SEED = 0
_LOCK_D = dict()
_IGNORE_NONAMES = True
generator_is_selected = lambda:ui.getFocused(7)

def setrandomizerpad(n):
    global RANDOMIZER_PAD
    RANDOMIZER_PAD = n

def setrandomizerpad_hex(n):
    global RANDOMIZER_PAD
    RANDOMIZER_PAD = int(f"0x{n}",base=16)

def setparaminfopad(n):
    global PARAMINFO_PAD
    PARAMINFO_PAD = n

def setparaminfopad_hex(n):
    global PARAMINFO_PAD
    PARAMINFO_PAD = int(f"0x{n}",base=16)

def lock(plugname,*paramindex):
    if plugname not in _LOCK_D:
        _LOCK_D[plugname] = set()
    for p in paramindex:
        _LOCK_D[plugname].add(p)
    print(_LOCK_D)

def unlock(plugname,*paramindex):
    if plugname not in _LOCK_D:
        return
    for p in paramindex:
        if p in _LOCK_D[plugname]:
            _LOCK_D[plugname].remove(p)
    print(_LOCK_D)

def ignorenonames(ignore=True):
    global _IGNORE_NONAMES
    _IGNORE_NONAMES = ignore

def info():
    print("-"*40)
    print(f"""
INFO:
    Randomizer pad CC#:{RANDOMIZER_PAD}
    Parameter-info pad CC#:{PARAMINFO_PAD}

Use the following functions to set:
    setrandomizerpad(n)
    setrandomizerpad_hex("n")
    setparaminfopad(n)
    setparaminfopad_hex("n")
    
Locked parameters:
    {_LOCK_D}

Manage locked parameters with:
    lock(<plugin-name>,*<parameter-index>)
    unlock(<plugin-name>,*<parameter-index>)

Ignore No-name parameters:{_IGNORE_NONAMES}
    To include no-name (and generic midi) parameters in the randomize,
    use:
    ignorenonames(False)
    or to change it back, use ignorenonames(True)
    """)
    print("-"*40)

def isnoname(name):
    if any(((not len(name)),
            name.startswith("MIDI CC #"),
            name.startswith("MIDI Channel "))):
        return True
    return False

tempdict = dict()

def OnMidiMsg(event):
    global _SEED
    _M = 2**32
    _A = 1664525
    _C = 1013904223
    event.handled = False
    if event.midiId == midi.MIDI_CONTROLCHANGE:
        if event.data2 > 0:
            if event.data1 == RANDOMIZER_PAD:
                f_id = ui.getFocusedFormID()
                if generator_is_selected():
                    if plugins.isValid(f_id):
                        name = plugins.getPluginName(f_id,-1,1)
                        L = plugins.getParamCount(f_id)
                        params = set(list(range(L)))
                        if name in _LOCK_D:
                            for p in _LOCK_D[name]:
                                if p in params:
                                    params.remove(p)
                        for i in params:
                            paramname = plugins.getParamName(i,f_id)
                            if _IGNORE_NONAMES and isnoname(paramname):
                                continue
                            _SEED = (_A * _SEED + _C) % _M
                            r = _SEED / _M
                            plugins.setParamValue(r,i,f_id)
                            print("randomized:",paramname)
                event.handled = True

            elif event.data1 == PARAMINFO_PAD:
                f_id = ui.getFocusedFormID()
                if generator_is_selected():
                    if plugins.isValid(f_id):
                        name = plugins.getPluginName(f_id,-1,1)
                        print("name:",name)
                        L = plugins.getParamCount(f_id)
                        for i in range(L):
                            paramname = plugins.getParamName(i,f_id)
                            print(["","*"][isnoname(paramname)],i,paramname)
                event.handled = True

            elif event.data1 == COPY_PAD:
                print("Copy")
                f_id = ui.getFocusedFormID()
                if generator_is_selected():
                    if plugins.isValid(f_id):
                        tempdict.clear()
                        name = plugins.getPluginName(f_id,-1,1)
                        L = plugins.getParamCount(f_id)
                        params = set(list(range(L)))
                        if name in _LOCK_D:
                            for p in _LOCK_D[name]:
                                if p in params:
                                    params.remove(p)
                        for i in params:
                            paramname = plugins.getParamName(i,f_id)
                            if _IGNORE_NONAMES and isnoname(paramname):
                                continue
                            val = plugins.getParamValue(i,f_id)
                            tempdict[i] = val
                        print("tempdict:",tempdict)
                event.handled = True

            elif event.data1 == PASTE_PAD:
                print("Paste")
                f_id = ui.getFocusedFormID()
                if generator_is_selected():
                    if plugins.isValid(f_id):
                        name = plugins.getPluginName(f_id,-1,1)
                        L = plugins.getParamCount(f_id)
                        params = set(list(range(L)))
                        if name in _LOCK_D:
                            for p in _LOCK_D[name]:
                                if p in params:
                                    params.remove(p)
                        for i in params:
                            paramname = plugins.getParamName(i,f_id)
                            if _IGNORE_NONAMES and isnoname(paramname):
                                continue
                            val = tempdict.get(i,None)
                            if val == None:
                                continue
                            plugins.setParamValue(val,i,f_id)
                event.handled = True

