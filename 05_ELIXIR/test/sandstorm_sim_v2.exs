defmodule SandstormSimulationTest do
  use ExUnit.Case
  
  test "60% loss + corruption still converges" do
    # Start the mesh in sandstorm mode
    {:ok, mesh} = AetherMesh.start_link(sandstorm_mode: true)
    
    # Broadcast a thick intent (5 hammer blows)
    AetherMesh.broadcast_thick_intent(mesh, "HALT", region: "GRID_01")
    
    # Wait for convergence (check state periodically or use a loop)
    # Since we can't easily wait for a message in this mock, we'll poll
    check_convergence(mesh, 10)
  end

  defp check_convergence(mesh, 0), do: flunk("Mesh failed to converge in time")
  defp check_convergence(mesh, attempts) do
    if AetherMesh.state(mesh) == :halted do
      IO.puts("✅ CONVERGED: Intent 'HALT' executed despite sandstorm.")
      assert true
    else
      Process.sleep(100)
      check_convergence(mesh, attempts - 1)
    end
  end
end
