"""API for pinging an IPv4 address."""

from flask import Flask
import os
import socket
import subprocess

app = Flask(__name__)


PACKETS = int(os.environ.get("PACKETS", "5"))


@app.route("/", methods=["GET"])
def home():
    return {"msg": "This is a ping service"}


def to_dict(ip, result, error_code):
    """Returns the service data as dict"""
    return {
        "ip": ip,
        "result": result,
        "error_code": error_code,
        "packets": PACKETS,
    }


@app.route("/ping/<string:ip>", methods=["GET"])
def ping(ip):
    """Ping service"""
    try:
        socket.inet_aton(ip)
    except OSError:
        return to_dict("na", "{} is not a valid IP address".format(ip), 0), 400
    p = subprocess.Popen(["ping", "-c", str(PACKETS), ip])
    p.wait()
    error_code = p.poll()
    if error_code == 0:
        return to_dict(ip, "alive", error_code)
    if error_code == 2:
        return to_dict(ip, "unreachable", error_code), 404
    return to_dict(ip, "na", error_code), 505


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)
