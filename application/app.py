"""API for pinging an IPv4 address."""

from flask import Flask
import socket
import subprocess

app = Flask(__name__)


PACKETS = 5

@app.route("/", methods=["GET"])
def home():
    return {"help": "This is a ping service"}


@app.route("/ping/<string:ip>", methods=["GET"])
def ping(ip):
    """Ping service"""
    try:
        socket.inet_aton(ip)
    except OSError:
        return {
            "ip": "na",
            "result": "{} is not a valid IP address".format(ip),
            "error_code": 0,
            "packets": PACKETS
        }
    p = subprocess.Popen(["ping", "-c", "5", ip])
    p.wait()
    error_code = p.poll()
    if error_code == 0:
        return {"ip": ip, "result": "alive", "error_code": error_code, "packets": PACKETS}
    if error_code == 2:
        return {"ip": ip, "result": "unreachable", "error_code": error_code, "packets": PACKETS}
    return {"ip": ip, "result": "na", "error_code": error_code, "packets": PACKETS}


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)
