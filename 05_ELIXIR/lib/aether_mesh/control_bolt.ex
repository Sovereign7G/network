defmodule AetherMesh.ControlBolt do
  @moduledoc """
  Fixed-width binary prefix (64 bytes) — the AK's tapered cartridge tip.
  [16B INTENT | 32B NODE_ID | 8B SEQ | 8B CRC]
  """
  @bolt_width 64
  
  defstruct [:intent, :node_id, :seq, :crc]
  
  def pack(%__MODULE__{intent: i, node_id: n, seq: s, crc: c}) do
    intent_bin = String.pad_trailing(i, 16) |> binary_part(0, 16)
    node_bin = String.pad_trailing(n, 32) |> binary_part(0, 32)
    <<intent_bin::binary-16, node_bin::binary-32, s::unsigned-64, c::unsigned-64>>
  end
  
  def unpack(<<i::binary-16, n::binary-32, s::unsigned-64, c::unsigned-64>>) do
    bolt = %__MODULE__{
      intent: String.trim(i, <<0>>),
      node_id: String.trim(n, <<0>>),
      seq: s,
      crc: c
    }
    # In production, verify crc64(bolt) == c
    {:ok, bolt}
  end
  def unpack(_), do: {:error, :malformed}
end
