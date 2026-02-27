class ToolStore {
    state = $state({
        activeTool: null as any
    });

    activateTool(tool: any) {
        this.state.activeTool = tool;
    }

    deactivateTool() {
        this.state.activeTool = null;
    }
}

export const toolStore = new ToolStore();
