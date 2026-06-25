#!/usr/bin/env python3
"""S7G CLI — command-line interface for the Sovereign 7G Network.
Usage:
  s7g call bob.eth
  s7g beam --src 37.77,-122.42 --dst 37.34,-121.89
  s7g node register --stake 1000 --location "San Francisco"
  s7g status
  s7g message bob.eth "Hello from 7G!"
"""
import argparse, json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sdk', 'py'))
from s7g import S7GClient

def cmd_call(args):
    client = S7GClient(identity=args.identity)
    call = client.call(to=args.to, call_type=args.type, quality=args.quality)
    print(f"Calling {args.to}... ({args.type}, {args.quality})")
    print(f"Session: {call.session_id}")
    call.status = "connected"
    print("Connected! Press Ctrl+C to hangup.")
    try:
        import time; time.sleep(9999)
    except KeyboardInterrupt:
        call.hangup()
        print(f"\nCall ended.")

def cmd_beam(args):
    client = S7GClient(identity=args.identity)
    src_lat, src_lon = map(float, args.src.split(','))
    dst_lat, dst_lon = map(float, args.dst.split(','))
    result = client.compute_beam(src_lat, src_lon, dst_lat, dst_lon)
    print(json.dumps(result, indent=2))

def cmd_node(args):
    client = S7GClient(identity=args.identity)
    if args.action == "register":
        lat, lon = 37.77, -122.42  # default SF
        result = client.register_node(lat, lon, args.stake)
        print(json.dumps(result, indent=2))
    elif args.action == "status":
        result = client.node_status(args.node_id)
        print(json.dumps(result, indent=2))

def cmd_status(args):
    client = S7GClient(identity=args.identity)
    health = client.query_health()
    risk = client.query_risk()
    print("=== S7G Network Status ===")
    print(f"Health: {json.dumps(health, indent=2)}")
    print(f"Risk: {json.dumps(risk, indent=2)}")

def cmd_message(args):
    client = S7GClient(identity=args.identity)
    result = client.message(to=args.to, text=args.text, priority=args.priority)
    print(json.dumps(result, indent=2))

def main():
    p = argparse.ArgumentParser(description="Sovereign 7G CLI")
    p.add_argument("--identity", default=os.getenv("S7G_IDENTITY", "user.eth"), help="7G identity")
    sub = p.add_subparsers(dest="command")

    call_p = sub.add_parser("call", help="Make a 7G call")
    call_p.add_argument("to", help="Callee identity")
    call_p.add_argument("--type", default="voice", choices=["voice", "video"])
    call_p.add_argument("--quality", default="hd", choices=["hd", "standard", "low"])

    beam_p = sub.add_parser("beam", help="Compute beamforming weights")
    beam_p.add_argument("--src", required=True, help="Source lat,lon (e.g. 37.77,-122.42)")
    beam_p.add_argument("--dst", required=True, help="Destination lat,lon")

    node_p = sub.add_parser("node", help="Node management")
    node_p.add_argument("action", choices=["register", "status"])
    node_p.add_argument("--stake", type=int, default=1000)
    node_p.add_argument("--node-id")

    status_p = sub.add_parser("status", help="Network status")

    msg_p = sub.add_parser("message", help="Send a message")
    msg_p.add_argument("to", help="Recipient")
    msg_p.add_argument("text", help="Message text")
    msg_p.add_argument("--priority", default="normal", choices=["normal", "high", "urgent"])

    args = p.parse_args()
    if args.command == "call": cmd_call(args)
    elif args.command == "beam": cmd_beam(args)
    elif args.command == "node": cmd_node(args)
    elif args.command == "status": cmd_status(args)
    elif args.command == "message": cmd_message(args)
    else: p.print_help()

if __name__ == "__main__":
    main()
