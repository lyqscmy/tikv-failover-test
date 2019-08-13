#!/usr/bin/env python3

import subprocess
import json
import time

pd0_addr = "http://127.0.0.1:32811"

begin = time.time()
while True:
    out = subprocess.run(["./pd-ctl", "--pd", pd0_addr, "store"], stdout=subprocess.PIPE).stdout
    stores = json.loads(out.decode())
    for s in stores["stores"]:
        if "Down" == s["store"]["state_name"]:
            store_id = s["store"]["id"]
            break
    else:
        print("detecting", end="\r")
        time.sleep(10)
        continue
    print("detect store_id {} down in {}s".format(store_id, time.time()-begin))
    break

begin = time.time()
while True:
    out = subprocess.run(["./pd-ctl", "--pd", pd0_addr, "store", str(store_id)], stdout=subprocess.PIPE).stdout
    store = json.loads(out.decode())
    if "region_count" in store["status"]:
        print("left region_count {}".format(store["status"]["region_count"]), end='\r')
        time.sleep(10)
    else:
        print("region migration complete in {}".format(time.time() - begin))
        break
