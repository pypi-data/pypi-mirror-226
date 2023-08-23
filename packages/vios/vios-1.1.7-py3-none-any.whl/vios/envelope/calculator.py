"""所有指令都会由此模块进行预处理，如采样、失真、串扰等，
并送入设备执行(见device模块)
"""

import numpy as np
from qlisp.kernel_utils import sample_waveform
from waveforms import Waveform, wave_eval


def calculate(step: str, target: str, cmd: list):
    """指令的预处理

    Args:
        step (str): 步骤名，如main/step1/...
        target (str): 设备通道，如AWG.CH1.Offset
        cmd (list): 操作指令，格式为(操作类型, 值, 单位, kwds)。其中
            操作类型包括WRITE/READ/WAIT, kwds见assembler.preprocess说明。

    Returns:
        tuple: 预处理结果
    
    >>> calculate('main', 'AWG.CH1.Waveform',('WRITE',square(100e-6),'au',{'calibration':{}}))
    """
    ctype, value, unit, kwds = cmd

    if ctype != 'WRITE':
        return (step, target, cmd)

    if isinstance(value, str):
        try:
            func = wave_eval(value)
        except SyntaxError as e:
            func = value
    else:
        func = value

    if isinstance(func, Waveform):
        if target.startswith(tuple(kwds.get('filter', ['zzzzz']))):
            support_waveform_object = True
        else:
            support_waveform_object = False
        ch = kwds['target'].split('.')[-1]
        cmd[1] = sample_waveform(func, kwds['calibration'][ch],
                                 sample_rate=kwds['srate'],
                                 start=0, stop=kwds['LEN'],
                                 support_waveform_object=support_waveform_object)
    else:
        cmd[1] = func

    cmd[-1] = {'sid': kwds['sid'],
               'autokeep': kwds['autokeep'],
               'target': kwds['target']}

    return (step, target, cmd)


def preview(instruction: dict, targets: list = [], backend=None):
    """预览进入设备的波形，可由etc.preview关闭。
    # NOTE: 耗时操作，慎用！！！

    Args:
        instruction (dict): _description_
        backend (_type_, optional): _description_. Defaults to None.
    """
    if not targets:
        return

    lines = {}
    for step, operations in instruction.items():
        for target, cmd in operations.items():
            if cmd[-1]['target'].split('.')[0] not in targets or cmd[-1]['sid'] < 0:
                continue
            if target.endswith('Waveform'):
                val = cmd[1]
                if isinstance(val, Waveform):
                    val = val.sample()
                xt = np.arange(len(val))
                lines[cmd[-1]['target']] = {'data': (xt, val)}
    if lines:
        backend.plot([[lines]])
                


if __name__ == "__main__":
    import doctest
    doctest.testmod()