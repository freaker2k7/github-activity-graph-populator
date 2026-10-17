import { EditorView, basicSetup } from 'codemirror';
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

let grid = Array.from({ length: gridRows }, () => Array.from({ length: gridCols }, () => 0));

const editor = new EditorView({
	doc: grid.map((row) => row.join('')).join('\n'),
	extensions: [basicSetup],
	parent: document.getElementById('editor')!,
});

async function encode() {
	editor.dispatch({
		changes: { from: 0, to: editor.state.doc.length, insert: grid.map((row) => row.join('')).join('\n') },
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

async function drawGrid(encodeGrid = true) {
	const cellWidth = canvas.width / gridCols;
	const cellHeight = canvas.height / gridRows;
	for (let row = 0; row < gridRows; row++) {
		for (let col = 0; col < gridCols; col++) {
			ctx.fillStyle = colors[grid[row][col]];
			ctx.fillRect(col * cellWidth, row * cellHeight, cellWidth, cellHeight);
		}
	}

	if (encodeGrid) {
		await encode();
	}
}

drawGrid();

(document.getElementById('copy-btn') as HTMLButtonElement).addEventListener('click', async (e) => {
	e.preventDefault();
	await navigator.clipboard.writeText(editor.state.doc.toString());

	(e.target as HTMLButtonElement).textContent = 'Copied!';

	setTimeout(() => {
		(e.target as HTMLButtonElement).textContent = 'Copy';
	}, 2000);
});

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

setInterval(() => {
	const new_code = editor.state.doc.toString();
	const old_code = grid.map((row) => row.join('')).join('\n');

	if (new_code !== old_code) {
		const new_grid = new_code.split('\n').map((row) => row.split('').map((cell) => parseInt(cell)));
		if (new_grid.length === gridRows && new_grid.every((row) => row.length === gridCols)) {
			grid = new_grid;
			drawGrid(false);
		}
	}
}, 1000);

window.addEventListener('resize', () => {
	canvas.style.width = Math.min(window.innerWidth * 0.9, width) + 'px';
	canvas.style.height = Math.min(window.innerHeight * 0.9, height) + 'px';
});
