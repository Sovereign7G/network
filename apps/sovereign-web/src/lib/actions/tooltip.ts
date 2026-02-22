import Tooltip from '../components/ui/Tooltip.svelte';

let tooltipComponent: Tooltip | null = null;

export function tooltip(node: HTMLElement, text: string) {
    if (!text) return;

    const handleMouseEnter = (event: MouseEvent) => {
        if (!tooltipComponent) {
            tooltipComponent = new Tooltip({
                target: document.body,
                props: {
                    text: text,
                    x: event.clientX,
                    y: event.clientY,
                    visible: true
                }
            });
        } else {
            tooltipComponent.$set({
                text: text,
                x: event.clientX,
                y: event.clientY,
                visible: true
            });
        }
    };

    const handleMouseMove = (event: MouseEvent) => {
        if (tooltipComponent) {
            tooltipComponent.$set({
                x: event.clientX,
                y: event.clientY
            });
        }
    };

    const handleMouseLeave = () => {
        if (tooltipComponent) {
            tooltipComponent.$set({ visible: false });
        }
    };

    node.addEventListener('mouseenter', handleMouseEnter);
    node.addEventListener('mousemove', handleMouseMove);
    node.addEventListener('mouseleave', handleMouseLeave);

    return {
        update(newText: string) {
            text = newText;
        },
        destroy() {
            node.removeEventListener('mouseenter', handleMouseEnter);
            node.removeEventListener('mousemove', handleMouseMove);
            node.removeEventListener('mouseleave', handleMouseLeave);
            if (tooltipComponent) {
                tooltipComponent.$set({ visible: false });
            }
        }
    };
}
