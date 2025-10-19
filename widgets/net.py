import re, subprocess
from gi.repository import GLib
from fabric.widgets.label import Label

IPV4_RE = re.compile(r"\binet (\d+\.\d+\.\d+\.\d+)/\d+")

def _read_ip_addrs():
    """Devuelve {iface: [ips...]} leyendo 'ip -4 addr show'."""
    out = subprocess.check_output(["ip", "-4", "addr", "show"], text=True)
    addrs, iface = {}, None
    for line in out.splitlines():
        m = re.match(r"^\d+:\s+([^:]+):", line)
        if m:
            iface = m.group(1)
            continue
        if "inet " in line and iface:
            ip = IPV4_RE.search(line).group(1)
            addrs.setdefault(iface, []).append(ip)
    return addrs

def get_local_ip():
    addrs = _read_ip_addrs()
    # Prioriza ethernet/wifi comunes
    prefs = ("eth", "enp", "eno", "enx", "wlan", "wlp")
    for iface, ips in addrs.items():
        if iface.startswith(prefs) and ips:
            return ips[0]
    # Si nada, muestra "-"
    return "-"

def get_vpn_ip():
    addrs = _read_ip_addrs()
    for iface, ips in addrs.items():
        if iface.startswith(("tun", "tap", "vpn")) and ips:
            return ips[0]
    return "Disconnected"

class LocalIP(Label):
    def __init__(self, every=5, **kwargs):
        super().__init__(text="…", css_classes=["ip", "local"], **kwargs)
        self.every = every
        self.refresh()
        GLib.timeout_add_seconds(self.every, self._tick)

    def _tick(self):
        self.refresh()
        return True  # repetir

    def refresh(self):
        self.text = get_local_ip()

class VpnIP(Label):
    def __init__(self, every=5, **kwargs):
        super().__init__(text="…", css_classes=["ip", "vpn"], **kwargs)
        self.every = every
        self.refresh()
        GLib.timeout_add_seconds(self.every, self._tick)

    def _tick(self):
        self.refresh()
        return True

    def refresh(self):
        self.text = get_vpn_ip()

