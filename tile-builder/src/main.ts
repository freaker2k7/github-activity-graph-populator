import { transformerCopyButton } from '@selemondev/shiki-transformer-copy-button';
import { codeToHtml } from 'shiki';
import './main.scss';

const colors = ['#ffffff', '#00cc00', '#009900', '#006600', '#003300'];
const gridRows = 7;
let gridCols = 7;
const minGridCols = 1;
const size = 50;
const height = size * gridRows;
let width = size * gridCols;

const canvas = document.getElementById('canvas')! as HTMLCanvasElement;
const ctx = canvas.getContext('2d')! as CanvasRenderingContext2D;

canvas.width = width;
canvas.height = height;
canvas.style.border = '1px solid black';
canvas.style.borderRadius = '8px';
canvas.style.borderRadius = '8px';
canvas.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.1)';
ctx.fillStyle = 'lightgray';
ctx.fillRect(0, 0, canvas.width, canvas.height);

const grid = Array.from({ length: gridRows }, () => Array.from({ length: gridCols }, () => 0));
const code = document.getElementById('tile-code')! as HTMLElement;

async function encode() {
	code.innerHTML = await codeToHtml(grid.map((row) => row.join('')).join('\n'), {
		lang: 'txt',
		theme: 'everforest-light',
		transformers: [
			transformerCopyButton({
				duration: 1500,
				display: 'ready',
				successIcon: `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' stroke='rgba(128,128,128,1)' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' viewBox='0 0 24 24'%3E%3Crect width='8' height='4' x='8' y='2' rx='1' ry='1'/%3E%3Cpath d='M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2'/%3E%3Cpath d='m9 14 2 2 4-4'/%3E%3C/svg%3E`,
				copyIcon: `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' stroke='rgba(128,128,128,1)' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' viewBox='0 0 24 24'%3E%3Crect width='8' height='4' x='8' y='2' rx='1' ry='1'/%3E%3Cpath d='M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2'/%3E%3C/svg%3E`,
			}),
		],
	});
}

canvas.addEventListener('click', (e) => {
	const rect = canvas.getBoundingClientRect();
	const x = ((e.clientX - rect.left) / rect.width) * canvas.width;
	const y = ((e.clientY - rect.top) / rect.height) * canvas.height;
	const col = Math.floor(x / (canvas.width / gridCols));
	const row = Math.floor(y / (canvas.height / gridRows));
	console.log(`Clicked on row ${row}, col ${col}`);
	grid[row][col] = (grid[row][col] + 1) % colors.length;
	drawGrid();
});

async function drawGrid() {
	const cellWidth = canvas.width / gridCols;
	const cellHeight = canvas.height / gridRows;
	for (let row = 0; row < gridRows; row++) {
		for (let col = 0; col < gridCols; col++) {
			ctx.fillStyle = colors[grid[row][col]];
			ctx.fillRect(col * cellWidth, row * cellHeight, cellWidth, cellHeight);
		}
	}

	await encode();
}

drawGrid();

(document.getElementById('form') as HTMLFormElement).addEventListener('submit', async (e) => {
	e.preventDefault();
	await encode();
});

(document.getElementById('add-column') as HTMLButtonElement).addEventListener('click', async () => {
	gridCols++;
	for (let row = 0; row < gridRows; row++) {
		grid[row].push(0);
	}
	width = size * gridCols;
	canvas.width = width;
	canvas.style.width = Math.min(window.innerWidth * 0.9, width) + 'px';
	await drawGrid();

	(document.getElementById('matrix-size') as HTMLDivElement).textContent = `${gridRows}x${gridCols}`;
});

(document.getElementById('remove-column') as HTMLButtonElement).addEventListener('click', async () => {
	if (gridCols > minGridCols) {
		gridCols--;
		for (let row = 0; row < gridRows; row++) {
			grid[row].pop();
		}
		width = size * gridCols;
		canvas.width = width;
		canvas.style.width = Math.min(window.innerWidth * 0.9, width) + 'px';
		await drawGrid();

		(document.getElementById('matrix-size') as HTMLDivElement).textContent = `${gridRows}x${gridCols}`;
	}
});

window.addEventListener('resize', () => {
	canvas.style.width = Math.min(window.innerWidth * 0.9, width) + 'px';
	canvas.style.height = Math.min(window.innerHeight * 0.9, height) + 'px';
});
