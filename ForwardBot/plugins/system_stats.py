

import psutil
import platform
from datetime import datetime

from ForwardBot import CMD_HELP, bot
from ForwardBot.events import register

modules = CMD_HELP


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["Dtk", "Mnt", "Jam", "Hari"]

    while count < 4:
        count += 1
        remainder, result = divmod(
            seconds, 60) if count < 3 else divmod(
            seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
       time_list[x] = str(time_list[x]) + time_suffix_list[x]

    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


@register(incoming=True, pattern=r"^\.systeminfo")
async def psu(event):
    uname = platform.uname()
    softw = "**SYSTEM RELATED INFO**\n"
    softw += f"`OS         : {uname.system}`\n"
    softw += f"`RELEASE    : {uname.release}`\n"
    softw += f"`VERSION    : {uname.version}`\n"

    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    softw += f"`**LAST BOOT**: {bt.day}/{bt.month}/{bt.year}  {bt.hour}:{bt.minute}:{bt.second}`\n"
    cpuu = "**CPU INFO**\n"
    cpuu += "`PHYSICAL CORES  : " + \
        str(psutil.cpu_count(logical=False)) + "`\n"
    cpuu += "`TOTAL CORES     : " + \
        str(psutil.cpu_count(logical=True)) + "`\n"
    cpufreq = psutil.cpu_freq()
    cpuu += f"`Max Frequency    : {cpufreq.max:.2f}Mhz`\n"
    cpuu += f"`Min Frequency    : {cpufreq.min:.2f}Mhz`\n"
    cpuu += f"`Current Frequency: {cpufreq.current:.2f}Mhz`\n\n"

    cpuu += "**CPU Usage Per Core**\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpuu += f"`Core {i}  : {percentage}%`\n"
    cpuu += "**CPU USAGE**\n"
    cpuu += f"`CPU : {psutil.cpu_percent()}%`\n"

    svmem = psutil.virtual_memory()
    memm = "**RAM INFO**\n"
    memm += f"`Total     : {get_size(svmem.total)}`\n"
    memm += f"`Available : {get_size(svmem.available)}`\n"
    memm += f"`Used      : {get_size(svmem.used)}`\n"
    memm += f"`Percentage: {svmem.percent}%`\n"
    bw = "**Bandwidth USAGE**\n"
    bw += f"`UPLOAD  : {get_size(psutil.net_io_counters().bytes_sent)}`\n"
    bw += f"`DOWNLOAD: {get_size(psutil.net_io_counters().bytes_recv)}`\n"
    help_string = f"{str(softw)}\n"
    help_string += f"{str(cpuu)}\n"
    help_string += f"{str(memm)}\n"
    help_string += f"{str(bw)}\n"
    await bot.send_message(message=help_string, entity=event.chat_id)


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor



CMD_HELP.update({
    "system": "✘ Pʟᴜɢɪɴ : System Stats"
"\n\n⚡𝘾𝙈𝘿⚡: `.systeminfo`"
"\n↳ : Shows system informations such as RAM USAGE, CPU FREQ and so on."
})
