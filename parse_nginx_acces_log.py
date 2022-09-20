import re
re_search_pattern = re.compile(r'(?P<ipAddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - (?P<DateTime>\[\d\d\/\w{3}\/\d{4}:\d\d:\d\d:\d\d \+\d{4}]) (?P<Request>\"\w{1,6} /.+HTTP\/\d\.\d\") (?P<StatusCode>\d{3}) (?P<ByteSent>\d{1,100}) (?P<ReferHttp>\"\S+\") (?P<UserAgent>\".+\")')
uniq_ip_set = set()
user_agent_match_list = (
    'Windows NT 10.0', 
    'Linux x86_64', 
    'Mac OS',)
clients_d = {
    'Windows NT 10.0' : 0,
    'Linux x86_64' : 0,
    'Mac OS': 0,
}
status_code_d = {
    '200' : 0,
    '304' : 0,
    '404' : 0,
    '405' : 0,
}

def load_log(path_log):
    with open(path_log, mode="r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            line_match = re_search_pattern.match(line)
            parse_user_agent(line_match.group('UserAgent'))
            parse_status_code(line_match.group('StatusCode'))
            parse_ip(line_match.group('ipAddress'))

def parse_status_code(line_log_code):
    if '200' in line_log_code:
        status_code_d['200'] += 1
    if '304' in line_log_code:
        status_code_d['304'] += 1
    if '404' in line_log_code:
        status_code_d['404'] += 1
    if '405' in line_log_code:
        status_code_d['405'] += 1

def parse_ip(line_log_ip):
    if line_log_ip != None:
        uniq_ip_set.add(line_log_ip)

def parse_user_agent(line_log_ua):
    if user_agent_match_list[0] in line_log_ua:
        clients_d['Windows NT 10.0'] += 1
    if user_agent_match_list[1] in line_log_ua:
        clients_d['Linux x86_64'] += 1
    if user_agent_match_list[2] in line_log_ua:
        clients_d['Mac OS'] += 1
    else:
        return False

load_log('nginx.access.log')
print('Список уникальных IP адресов:')
for i in uniq_ip_set:
    print(i)
print(f'Количество уникальных IP адресов: {len(uniq_ip_set)}')
print('Клиенты по типу ОС:')
for key,value in clients_d.items():
    print(f'Клиенты: {key} - Количество: {value}')

print(f'Количество запросов с ошибками: {status_code_d.get("404") + status_code_d.get("405")}')
print(f'Количество запросов без ошибок: {status_code_d.get("200") + status_code_d.get("304")}')