import subprocess

from langchain.tools import tool


def shell(cmd):
    output = subprocess.check_output(cmd, shell=True)
    return output


@tool
def iostat():
    """iostat - Report Central Processing Unit (CPU) statistics and input/output statistics for devices and partitions."""
    return shell("iostat -dxsm 1 3 | grep -v loop")


@tool
def vmstat():
    """vmstat - Report virtual memory statistics."""
    return shell("vmstat -S m 1 3")


@tool
def mpstat():
    """mpstat - Report processors related statistics."""
    return shell("mpstat 1 3")


@tool
def loadavg():
    """uptime - Gives average load on system."""
    return shell("uptime")
