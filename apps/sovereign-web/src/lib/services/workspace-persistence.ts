export interface WorkspaceTemplate {
    id: string;
    name: string;
    description: string;
    columns: any[];
    createdAt: number;
    lastUsed: number;
    useCount: number;
}

class WorkspacePersistence {
    private readonly STORAGE_KEY = 'sovereign-workspace';
    private readonly TEMPLATES_KEY = 'workspace-templates';

    // Save current workspace
    saveWorkspace(columns: any[]) {
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(columns));
    }

    // Load current workspace
    loadWorkspace(): any[] | null {
        const saved = localStorage.getItem(this.STORAGE_KEY);
        return saved ? JSON.parse(saved) : null;
    }

    // Save as template
    saveTemplate(name: string, description: string, columns: any[]): WorkspaceTemplate {
        const templates = this.listTemplates();

        const template: WorkspaceTemplate = {
            id: `template-${Date.now()}`,
            name,
            description,
            columns,
            createdAt: Date.now(),
            lastUsed: Date.now(),
            useCount: 1
        };

        templates.push(template);
        localStorage.setItem(this.TEMPLATES_KEY, JSON.stringify(templates));

        return template;
    }

    // List all templates
    listTemplates(): WorkspaceTemplate[] {
        const saved = localStorage.getItem(this.TEMPLATES_KEY);
        return saved ? JSON.parse(saved) : [];
    }

    // Load a template
    loadTemplate(templateId: string): any[] | null {
        const templates = this.listTemplates();
        const template = templates.find(t => t.id === templateId);

        if (template) {
            template.lastUsed = Date.now();
            template.useCount++;
            localStorage.setItem(this.TEMPLATES_KEY, JSON.stringify(templates));
            return template.columns;
        }

        return null;
    }

    // Delete template
    deleteTemplate(templateId: string) {
        const templates = this.listTemplates();
        const filtered = templates.filter(t => t.id !== templateId);
        localStorage.setItem(this.TEMPLATES_KEY, JSON.stringify(filtered));
    }
}

export const workspacePersistence = new WorkspacePersistence();
