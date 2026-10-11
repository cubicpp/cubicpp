// Official renderer at abozanona/pacman-contribution-graph commit
// 7332e1de7903ab780c3692a4127a59cc13872daa (5.3.2), without Action analytics.
import { ArcadeRenderer } from './vendor/pacman.mjs';
import { writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

if (!process.env.GITHUB_TOKEN) throw new Error('GITHUB_TOKEN is required');
for (const game of ['pacman', 'breakout']) {
  for (const [suffix, theme] of [['light', 'github'], ['dark', 'github-dark']]) {
    let svg = '';
    const renderer = new ArcadeRenderer({
      game, platform: 'github', username: 'cubicpp', gameTheme: theme,
      playerStyle: 'opportunistic', showMonthLabels: true,
      githubSettings: { accessToken: process.env.GITHUB_TOKEN },
      svgCallback: result => { svg = result; },
      gameOverCallback: () => {}, pointsIncreasedCallback: () => {},
    });
    await renderer.start();
    if (!svg.startsWith('<svg') || /<(script|foreignObject)\b/i.test(svg)) throw new Error('Invalid arcade SVG');
    const target = fileURLToPath(new URL(`../assets/arcade-${game}-${suffix}.svg`, import.meta.url));
    await writeFile(target, svg);
    console.log(`Generated ${game} ${suffix}`);
  }
}
