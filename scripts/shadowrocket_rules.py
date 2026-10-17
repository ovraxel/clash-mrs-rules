"""Convert normalized Mihomo text rules into Shadowrocket RULE-SET entries."""
import ipaddress

def convert(value, behavior):
    if behavior == 'ipcidr':
        network = ipaddress.ip_network(value, strict=False)
        return f"IP-CIDR{6 if network.version == 6 else ''},{network},no-resolve"
    if value.startswith('full:'):
        return 'DOMAIN,' + value[5:]
    if value.startswith('keyword:'):
        return 'DOMAIN-KEYWORD,' + value[8:]
    if value.startswith('+.'):
        return 'DOMAIN-SUFFIX,' + value[2:]
    if value.startswith('*.'):
        return 'DOMAIN-WILDCARD,' + value
    return 'DOMAIN-SUFFIX,' + value

def render(lines, behavior):
    return '# Shadowrocket RULE-SET; generated automatically.\\n'.replace('\\n','\n') + '\n'.join(sorted({convert(v, behavior) for v in lines})) + '\n'
