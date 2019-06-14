#-*- coding:utf8 -*-

import wmi
import os
import yaml
import sys

# IP address, subnetmask and gateway values should be unicode objects
ip = u'192.168.67.11'
subnetmask = u'255.255.240.0'
gateway = u'192.168.64.254'
#dns = u'202.96.209.5'
dns = [u'202.1.11.5', u'8.8.8.8']
mac = '123'

def changeWinIP():
    wlan_int_id = None
    for nic in wmi.WMI().Win32_NetworkAdapter():
        print(nic.NetConnectionID)
        if nic.MACAddress == mac:
            wlan_int_id = nic.Index
            print('找到需要修改的网卡:::' + nic.NetConnectionID)
            break

    if wlan_int_id != None:
        for nic in wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True):
            if nic.Index == wlan_int_id:

                #print(nic)
                print('-----------------------------------------------')
                print('当前网络信息')
                print('网卡: %s'%nic.Description)
                print('IP: %s' % nic.IPAddress[0])
                try:
                    print('子网掩码: %s' % nic.IPSubnet[0])
                except Exception:
                    print('子网掩码: 无')
                try:
                    print('网关: %s'%nic.DefaultIPGateway[0])
                except Exception:
                    print('网关: 无')
                try:
                    print('DNS: %s, %s'%(nic.DNSServerSearchOrder[0], nic.DNSServerSearchOrder[1]))
                except Exception:
                    print('DNS: 无')
                print('-----------------------------------------------')

                ret1 = nic.EnableStatic(IPAddress=[ip], SubnetMask=[subnetmask])
                ret2 = nic.SetGateways(DefaultIPGateway=[gateway])
                ret3 = nic.SetDNSServerSearchOrder(DNSServerSearchOrder=dns)
                #ret3 = nic.SetDNSServerSearchOrder(DNSServerSearchOrder=['8.8.8.8'])

                if ret1[0] == 0 and ret2[0] == 0 and ret3[0] == 0:
                    print("设置成功！")
                    print('-----------------------------------------------')
                    print('修改后网络信息')
                    print('网卡: %s'%nic.Description)
                    print('IP: %s'%ip)
                    print('子网掩码：%s'%subnetmask)
                    print('网关: %s'%gateway)
                    print('DNS: %s, %s'%(dns[0], dns[1]))
                    print('-----------------------------------------------')
                else:
                    print('设置失败!')
    else:
        print('error,id is empty!')

def parseYamlFile(filePath, fileName):
    yamlPath = os.path.join(filePath, fileName)
    f = open(yamlPath, 'r', encoding='utf-8')
    inputCont = f.read()
    cont = yaml.load(inputCont, Loader=yaml.FullLoader)
    return cont

if __name__ == '__main__':
    #curPath = os.path.dirname(os.path.realpath(__file__))
    filePath = os.path.abspath('.')
    fileName = 'ip_config.yaml'
    cont = parseYamlFile(filePath, fileName)

    print('请输入网络类型')
    ipType = input()
    print('网络类型： %s'%ipType)
    ip = cont[ipType]['IP']
    subnetmask = cont[ipType]['IPSubnet']
    gateway = cont[ipType]['Gateway']
    dnsAry = cont[ipType]['DNS'].split(',')
    dns = [dnsAry[0].strip(), dnsAry[1].strip()]
    mac=cont[ipType]['MAC']

    changeWinIP()