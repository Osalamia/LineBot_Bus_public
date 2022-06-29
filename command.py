import bus

def cmd(cmd , tdx_token):
    if cmd == "!commend":
        return "請輸入 XXX到XXX (XXX分別為公車站名)"
    if "到" in cmd:
        text = cmd
        start_stop = text.split("到")[0]
        end_stop = text.split("到")[1]
        return bus.find_bus(start_stop, end_stop, tdx_token)
    else:
        return "指令輸入錯誤，請重新輸入指令。如果要查詢指令使用方式，請輸入!command"