defmodule AetherMesh do
  use GenServer
  alias AetherMesh.ControlBolt
  alias AetherMesh.FuzzyDecoder

  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts)
  end

  def broadcast_thick_intent(pid, intent, gas_data \\ []) do
    GenServer.cast(pid, {:broadcast_thick_intent, intent, gas_data})
  end

  def state(pid) do
    GenServer.call(pid, :get_state)
  end

  # Callbacks
  def init(opts) do
    {:ok, %{state: :idle, sandstorm_mode: Keyword.get(opts, :sandstorm_mode, false), seen_seqs: MapSet.new(), test_pid: self()}}
  end

  def handle_call(:get_state, _from, %{state: state} = s) do
    {:reply, state, s}
  end

  def handle_cast({:broadcast_thick_intent, intent, gas_data}, state) do
    bolt = %ControlBolt{intent: intent, node_id: "S-BREAKER", seq: 1, crc: 0}
    gas_bin = Jason.encode!(Enum.into(gas_data, %{}))
    packet = ControlBolt.pack(bolt) <> gas_bin

    # Simulate 5 hammer blows
    for i <- 1..5 do
      if state.sandstorm_mode do
        # Simulate 60% loss
        if :rand.uniform() > 0.60 do
          send(self(), {:receive_packet, packet})
        end
      else
        send(self(), {:receive_packet, packet})
      end
    end
    {:noreply, state}
  end

  def handle_info({:receive_packet, packet}, state) do
    case FuzzyDecoder.decode(packet) do
      {:executable, bolt, _gas} ->
        if MapSet.member?(state.seen_seqs, bolt.seq) do
          # Dedupe
          {:noreply, state}
        else
          new_state = if bolt.intent == "HALT", do: :halted, else: state.state
          if new_state == :halted do
            # Notify test process if needed
            # send(state.test_pid, {:converged, "HALT"}) # In real test this would be the caller
            Process.send_after(self(), {:notify_test, bolt.intent}, 0)
          end
          {:noreply, %{state | state: new_state, seen_seqs: MapSet.put(state.seen_seqs, bolt.seq)}}
        end
      _ ->
        {:noreply, state}
    end
  end

  def handle_info({:notify_test, intent}, state) do
    # In a real test, the test runner would receive this.
    # For simulation, we'll just log it.
    {:noreply, state}
  end
end
