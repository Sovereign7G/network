defmodule AetherMesh.FuzzyDecoder do
  alias AetherMesh.ControlBolt

  def decode(packet) do
    case packet do
      <<bolt_bin::binary-64, gas::binary>> ->
        case ControlBolt.unpack(bolt_bin) do
          {:ok, bolt_struct} ->
            # Bolt is intact — execute regardless of gas
            gas_result = try_decode_gas(gas)
            {:executable, bolt_struct, gas_result}
          error ->
            error
        end
      _ ->
        {:error, :malformed}
    end
  end
  
  defp try_decode_gas(gas) do
    case Jason.decode(gas) do
      {:ok, data} -> {:clean, data}
      _ -> {:vented, :corruption_ignored}
    end
  end
end
