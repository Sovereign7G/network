interface IntersectParams {
    rootMargin?: string;
    threshold?: number | number[];
    class?: string;
    once?: boolean;
}

function intersect(node: HTMLElement, params: IntersectParams = {}) {
    let observer: IntersectionObserver;

    const {
        rootMargin = "0px",
        threshold = 0.1,
        class: activeClass = "intersected",
        once = true
    } = params;

    const init = () => {
        observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        node.classList.add(activeClass);
                        if (once) {
                            observer.unobserve(node);
                        }
                    } else if (!once) {
                        node.classList.remove(activeClass);
                    }
                });
            },
            { rootMargin, threshold }
        );

        observer.observe(node);
    };

    init();

    return {
        destroy() {
            if (observer) {
                observer.disconnect();
            }
        }
    };
}
