import hashlib

def do_work(cfg, in_q, out_q):
    sec_key = cfg["processing"]["stateless_tasks"]["secret_key"].encode('utf-8')
    iters = cfg["processing"]["stateless_tasks"]["iterations"]

    def check_packet(pkt):
        val_txt = f"{pkt['metric_value']:.2f}".encode('utf-8')
        
        h_bytes = hashlib.pbkdf2_hmac('sha256', sec_key, val_txt, iters)
        
        if h_bytes.hex() == pkt['security_hash']:
            out_q.put(pkt)
        else:
            print(f"SECURITY ALERT: Dropped bad packet from {pkt.get('entity_name')}")

    list(map(check_packet, iter(in_q.get, None)))
def get_avg(num_list):
    if not num_list:
        return 0
    return sum(num_list) / len(num_list)
