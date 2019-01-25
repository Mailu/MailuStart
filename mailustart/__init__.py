import tenacity
from tenacity import retry
import logging as log
import socket
import jinja2
import os



@retry(
    stop=tenacity.stop_after_attempt(100),
    wait=tenacity.wait_random(min=2, max=5),
    before=tenacity.before_log(log.getLogger(__name__ + ".tenacity.retry"), log.DEBUG),
    before_sleep=tenacity.before_sleep_log(log.getLogger(__name__ + ".tenacity.retry"), log.INFO),
    after=tenacity.after_log(log.getLogger(__name__ + ".tenacity.retry"), log.DEBUG)
    )

def resolve(host):
    try:
        hostname, port = host.split(":")
    except ValueError:
        hostname = host
    logger = log.getLogger(__name__ + ".resolve()")
    logger.info(hostname) 
    ip_addr = socket.gethostbyname(hostname)
    try:
        return ip_addr + ":" + port
    except: 
        return ip_addr

def convert(src, dst, args=None):
    logger = log.getLogger("convert()")
    logger.debug("Source: %s, Destination: %s", src, dst)
    if args:
        open(dst, "w").write(jinja2.Template(open(src).read()).render(**args))
    else:
        open(dst, "w").write(jinja2.Template(open(src).read()).render(**os.environ))
