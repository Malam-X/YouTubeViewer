from selenium import webdriver
import time
import threading

url = input("[+] URL: ")
proxy_path = input("[*] Proxies: ")
threads_num = input("[+] Threads: ")
threads_num = int(threads_num)
with open(proxy_path) as f:
    content = f.readlines()
    f.close()
proxies = 0
with open(proxy_path) as infp:
    for line in infp:
       if line.strip():proxies += 1
print('Loaded %d proxies \n' %proxies)

def worker(num):
    run_through = num
    run_through = int(run_through)
    print('[*] Worker: %s \n' % num)
    print("[=] Running: %s \n" %run_through)
    while True:
        print(run_through)
        try:use_proxy = content[run_through]
        except IndexError:
            print("[!] Out of proxies")
            break
        print(use_proxy)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' %use_proxy)
        browser = webdriver.Chrome(chrome_options=chrome_options)
        try:
           browser.get(url)
           time.sleep(10)
           browser.quit()
        except Exception as e:
            browser.quit()
            run_through += threads_num
            continue
        run_through += threads_num
        if run_through >= proxies:
            print("[-] No more proxies \n")
            browser.quit()
            break

threads = []
for i in range(threads_num):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()
