import camelot

CamelotServerIp = "10.38.228.239"
CamelotServerPort = 5000

CcmIp = "10.38.228.28"

ep1Mac = "SEP000000581026"

serv = camelot.create_camelot_server(CamelotServerIp, CamelotServerPort)
serv.log_mask(moduleid="*",level="debug_5",device="file")
serv.log_mask(moduleid="*",level="error",device="console")

ep1 = serv.create_new_endpoint('sk',ep1Mac)
ep1.config('skinny.phone.phoneip',CamelotServerIp)
ep1.config('skinny.phone.tftpip',CcmIp)
ep1.config('skinny.phone.devicetype','585')
ep1.config('skinny.phone.protocolver','0x00000014')
ep1.config('skinny.timeouts.setup','60000')
ep1.init()
ep1.inservice()

ep1.get_lines()
ep1.get_info()
ep1.get_info()['state']