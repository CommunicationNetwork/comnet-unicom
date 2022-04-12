from scapy.all import * # TODO: remove * import

class UnicomReceiver:
    def __init__(self, mon_interface, receiver_name, receive_callback):
        self.mon_interface = mon_interface
        self.receiver_id = self.generate_id(receiver_name)
        self.receive_callback = receive_callback

    def internal_callback(self, frame):
        if frame.haslayer(Dot11) and frame.type == 2 and frame.subtype == 5:
            if frame.addr2.replace(":", "").startswith(self.receiver_id):
                data = bytes(frame[Dot11].payload)
                self.receive_callback(data)
            

    def start(self):
        sniff(iface=self.mon_interface, prn=self.internal_callback)

    # https://gist.github.com/mengzhuo/180cd6be8ba9e2743753
    def generate_id(self, s):                                                                                                                                
        hash = 5381
        for x in s:
            hash = (( hash << 5) + hash) + ord(x)
        return hex(hash & 0xFFFFFFFF)[2:8]