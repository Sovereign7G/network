// coordinator.mo — S7G Inference Coordinator Canister
// Routes requests across Akash, Render, Bittensor with fallback + immutable ledger

import Text "mo:base/Text";
import Nat "mo:base/Nat";
import Int "mo:base/Int";
import Time "mo:base/Time";
import Array "mo:base/Array";
import Iter "mo:base/Iter";
import Result "mo:base/Result";
import Debug "mo:base/Debug";
import Error "mo:base/Error";
import Cycles "mo:base/ExperimentalCycles";
import Http "mo:base/Http";
import Blob "mo:base/Blob";
import Buffer "mo:base/Buffer";

shared actor class Coordinator() {

  // ── Types ────────────────────────────────────────────────────────────

  public type Provider = { #Akash; #Render; #Bittensor; #ICP };

  public type Request = {
    model: Text;
    prompt: Text;
    max_tokens: ?Nat;
    temperature: ?Float;
  };

  public type Response = {
    result: Text;
    provider: Provider;
    timestamp: Int;
    request_id: Nat;
  };

  public type RequestLog = {
    id: Nat;
    request: Request;
    response: Response;
    timestamp: Int;
  };

  public type Proposal = {
    id: Nat;
    action: GovernanceAction;
    proposer: Text;
    votes: [Text];
    status: { #Pending; #Approved; #Rejected };
  };

  // ── State ────────────────────────────────────────────────────────────

  private stable var fallbackChain: [Provider] = [#Akash, #Render, #Bittensor, #ICP];
  private stable var requestCounter: Nat = 0;
  private stable var ledger: [RequestLog] = [];
  private stable var governors: [Text] = [];
  private stable var proposalCounter: Nat = 0;
  private stable var proposals: [Proposal] = [];

  // ── API ──────────────────────────────────────────────────────────────

  public query func health() : async Text {
    "Coordinator live. Requests: " # Nat.toText(requestCounter) # ", Governors: " # Nat.toText(governors.size())
  };

  public shared func route(model: Text, prompt: Text) : async Response {
    let request: Request = { model; prompt; max_tokens = null; temperature = null; };
    for (provider in fallbackChain.vals()) {
      let result = await callProvider(provider, model, prompt);
      if (result != "") {
        let response: Response = { result; provider; timestamp = Time.now(); request_id = requestCounter; };
        ledger := Array.append(ledger, [{ id = requestCounter; request; response; timestamp = Time.now() }]);
        requestCounter += 1;
        return response;
      };
    };
    throw Error.reject("All providers failed");
  };

  private func callProvider(p: Provider, model: Text, prompt: Text) : async Text {
    let endpoint = switch p {
      case (#Akash) { "https://s7g-committee.onrender.com/propose" };
      case (#Render) { "https://api.render.com/v1/inference" };
      case (#Bittensor) { "https://bittensor-adapter.onrender.com/v1/completions" };
      case (#ICP) { "https://llm-canister.icp0.io/v1/chat/completions" };
    };
    let body = switch p {
      case (#Akash) { "{\"request_id\":\"" # Nat.toText(requestCounter) # "\",\"payload\":{\"prompt\":\"" # prompt # "\"}}" };
      case _ { "{\"model\":\"" # model # "\",\"prompt\":\"" # prompt # "\"}" };
    };
    Cycles.add(10_000_000_000);
    let response = await Http.request({
      url = endpoint; method = #POST; headers = [("Content-Type", "application/json")];
      body = ?Text.encodeUtf8(body); max_response_bytes = ?10_000;
    });
    return Text.decodeUtf8(response.body);
  };

  // ── Ledger ───────────────────────────────────────────────────────────

  public query func get_ledger(limit: Nat) : async [RequestLog] {
    let len = ledger.size();
    let start = if (len > limit) { len - limit } else { 0 };
    return Array.subArray(ledger, start, len - start);
  };

  public query func get_request_count() : async Nat { requestCounter };

  // ── Governance ───────────────────────────────────────────────────────

  public shared(msg) func add_governor(p: Text) : async Result.Result<(), Text> {
    if (not isGovernor(msg.caller.toText())) { return #err("Unauthorized") };
    if (Array.indexOf(p, governors, Text.equal) != null) { return #err("Already governor") };
    governors := Array.append(governors, [p]); #ok(())
  };

  public query func get_governors() : async [Text] { governors };

  private func isGovernor(p: Text) : Bool {
    Array.indexOf(p, governors, Text.equal) != null
  };

  public shared(msg) func set_fallback_chain(chain: [Provider]) : async Result.Result<(), Text> {
    if (not isGovernor(msg.caller.toText())) { return #err("Unauthorized") };
    fallbackChain := chain; #ok(())
  };

  public query func get_fallback_chain() : async [Provider] { fallbackChain };
}
