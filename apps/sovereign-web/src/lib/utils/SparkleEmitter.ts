export function spawnSparkles(x: number, y: number, color: string = '#fbbf24') {
    const container = document.body;
    const particleCount = 20;

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'sparkle-particle';

        const size = Math.random() * 4 + 2;
        const tx = (Math.random() - 0.5) * 200;
        const ty = (Math.random() - 0.5) * 200;
        const txFinal = tx * 1.5;
        const tyFinal = ty * 1.5;

        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.left = `${x}px`;
        particle.style.top = `${y}px`;
        particle.style.background = `radial-gradient(circle, ${color} 0%, transparent 70%)`;

        particle.style.setProperty('--tx', `${tx}px`);
        particle.style.setProperty('--ty', `${ty}px`);
        particle.style.setProperty('--tx-final', `${txFinal}px`);
        particle.style.setProperty('--ty-final', `${tyFinal}px`);

        particle.style.animation = `sparkle-fly ${Math.random() * 0.5 + 0.5}s cubic-bezier(0.16, 1, 0.3, 1) forwards`;

        container.appendChild(particle);

        setTimeout(() => {
            particle.remove();
        }, 1000);
    }
}
