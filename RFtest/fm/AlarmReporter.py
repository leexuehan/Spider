import datetime
import json
import uuid

from http.HttpService import HttpService


class AlarmReporter(object):
    def __init__(self):
        self.alarm_model = {'neIps': [], 'alarms': {'alarmId': '1'}}
        self.reported_alarm_dict = {}

    def raise_alarm(self, server_info_list, alarm_num, timeout):
        total_alarm = 0
        server_info_dict = self.get_sim_info_dict(server_info_list)
        begin_time = datetime.datetime.now()
        cost_time = 0
        while total_alarm < alarm_num and cost_time < timeout:
            for (sim_ip, start_net) in server_info_dict.items():
                total_alarm += self.do_raise(alarm_num, sim_ip, start_net)
                if total_alarm % 10 == 0:
                    print "already report alarm num: " + str(total_alarm)
                if total_alarm >= alarm_num:
                    break
            cost_time = (datetime.datetime.now() - begin_time).seconds
        self.persist_reported_alarm()

    def clear_reported_alarm(self, server_info_list):
        with open('report-alarms.json', 'r') as reported_alarms:
            reported_alarm_dict = json.loads(reported_alarms.read())
        clear_total_num = 0
        for sim_ip in reported_alarm_dict.keys():
            dict = reported_alarm_dict.get(sim_ip)
            for ne_ip in dict.keys():
                clear_total_num += self.clear_alarm_by_alarmId(sim_ip, ne_ip, dict.get(ne_ip))
                if clear_total_num % 100 == 0:
                    print "already clear alarm num", clear_total_num

    def clear_alarm_by_alarmId(self, sim_ip, hostIp, alarmId_list):
        clear_num = 0
        url = "http://%s:8080/am/notify" % (sim_ip)
        for alarm_id in alarmId_list:
            self.alarm_model['neIps'] = hostIp
            self.alarm_model['alarms']['alarmId'] = alarm_id
            self.alarm_model['alarms']['messageType'] = 'cleared'
            res = HttpService().post(url, json.dumps(self.alarm_model))
            if res == 200:
                clear_num += 1
            return clear_num

    def do_raise(self, alarm_num, sim_ip, start_net):
        url = "http://%s:8080/am/notify" % (sim_ip)
        reported_alarm_num = 0
        [ip_seg_1, ip_seg_2, ip_seg_3] = start_net.split('.')
        for index in range(int(ip_seg_3), int(ip_seg_3) + 4):
            ip_seg_4 = 1
            while ip_seg_4 < 251 and reported_alarm_num < alarm_num:
                hostIp = ip_seg_1 + '.' + ip_seg_2 + '.' + str(index) + '.' + str(ip_seg_4)
                self.alarm_model['neIps'] = [hostIp]
                alarm_id = str(uuid.uuid1())
                self.alarm_model['alarms']['alarmId'] = alarm_id
                res = HttpService().post(url, json.dumps(self.alarm_model))
                if res == 200:
                    reported_alarm_num += 1
                ip_seg_4 += 1
                self.create_report_alarm_dict(sim_ip, hostIp, alarm_id)
        return reported_alarm_num

    def create_report_alarm_dict(self, sim_ip, hostIp, alarm_id):
        if self.reported_alarm_dict.has_key(sim_ip):
            if self.reported_alarm_dict[sim_ip].has_key(hostIp):
                self.reported_alarm_dict[sim_ip][hostIp].append(alarm_id)
            else:
                neip_alarmId_dict = self.reported_alarm_dict.get(sim_ip)
                if neip_alarmId_dict.has_key(hostIp):
                    neip_alarmId_dict[hostIp].append(alarm_id)
                else:
                    neip_alarmId_dict[hostIp] = [alarm_id]
        else:
            dict = {}
            dict[hostIp] = [alarm_id]
            self.reported_alarm_dict[sim_ip] = dict

    def get_sim_info_dict(self, server_info_list):
        server_info_dict = {}
        for server_info in server_info_list:
            server_ip = self.get_simulator_ip(server_info)
            start_net = self.get_start_net(server_info)
            server_info_dict[server_ip] = start_net
        return server_info_dict

    def get_simulator_ip(self, server_info):
        result = server_info.split(':')
        if len(result) != 2:
            raise Exception("server info illegal:" + server_info)
        return result[0]

    def get_start_net(self, server_info):
        result = server_info.split(':')
        if len(result) != 2:
            raise Exception("server info illegal:" + server_info)
        return result[1]

    def persist_reported_alarm(self):
        with open('report-alarms.json', 'w') as alarm_file:
            alarm_file.write(json.dumps(self.reported_alarm_dict))


if __name__ == '__main__':
    server_info_list = ["10.92.250.201:192.168.231", "10.92.250.202:192.168.240", "10.92.250.203:192.168.220"]
    # AlarmReporter().raise_alarm(server_info_list, 6000, 500)
    AlarmReporter().clear_reported_alarm(server_info_list)
    # print(AlarmReporter().get_simulator_ip("10.92.250.201:192.168.231.1"))
    # ne_ip_alarm_dict = {}
    # dict = {}
    # for key in ["var1", "var2"]:
    #     if dict.has_key(key):
    #         if dict[key].has_key("value") :
    #             dict[key]["value"] = {}
    # print dict
    print uuid.uuid1()
