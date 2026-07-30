import {
	apiRequest,
	clearToken,
	escapeHtml,
	getFormData,
	getToken,
	setMessage,
} from "./api.js";

const categoryForm = document.querySelector("#category-form");
const categoryList = document.querySelector("#category-list");
const clearSearch = document.querySelector("#clear-search");
const logoutButton = document.querySelector("#logout-button");
const noteCategory = document.querySelector("#note-category");
const noteForm = document.querySelector("#note-form");
const notesList = document.querySelector("#notes-list");
const refreshCategories = document.querySelector("#refresh-categories");
const refreshNotes = document.querySelector("#refresh-notes");
const searchForm = document.querySelector("#search-form");
const userLabel = document.querySelector("#user-label");

const state = {
	categories: [],
	notes: [],
};

function requireToken() {
	if (!getToken()) {
		window.location.href = "/login";
		return false;
	}

	return true;
}

function renderCategories() {
	if (!categoryList || !noteCategory) {
		return;
	}

	categoryList.innerHTML = state.categories.length
		? state.categories
				.map(
					(category) => `
						<span class="rounded-md bg-yellow-200 px-3 py-1 text-sm font-black text-zinc-950">
							${escapeHtml(category.name)}
						</span>
					`
				)
				.join("")
		: `<p class="text-sm text-zinc-500">No categories yet.</p>`;

	noteCategory.innerHTML = `
		<option value="">Choose category</option>
		${state.categories
			.map((category) => `<option value="${category.id}">${escapeHtml(category.name)}</option>`)
			.join("")}
	`;
}

function renderNotes() {
	if (!notesList) {
		return;
	}

	if (state.notes.length === 0) {
		notesList.innerHTML = `
			<p class="rounded-md border border-dashed border-zinc-400 bg-yellow-50 p-4 text-sm font-medium text-zinc-600">
				No notes found.
			</p>
		`;
		return;
	}

	notesList.innerHTML = state.notes
		.map(
			(note) => `
				<article class="rounded-lg border-2 border-zinc-950 bg-yellow-50 p-4">
					<div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
						<div>
							<h3 class="text-base font-black text-zinc-950">${escapeHtml(note.question)}</h3>
							<p class="mt-1 text-sm font-bold text-zinc-700">${escapeHtml(note.pattern)}</p>
						</div>
						<button data-delete-note="${note.id}" class="rounded-md bg-zinc-950 px-3 py-2 text-sm font-black text-yellow-50 hover:bg-zinc-800">
							Delete
						</button>
					</div>
					<div class="mt-4 grid gap-3 text-sm text-zinc-700">
						<p><span class="font-black text-zinc-950">Signal:</span> ${escapeHtml(note.signal)}</p>
						<p><span class="font-black text-zinc-950">Approach:</span> ${escapeHtml(note.solution_approach)}</p>
						<p><span class="font-black text-zinc-950">Memory:</span> ${escapeHtml(note.useful_memory)}</p>
						<p class="font-semibold text-zinc-600">${escapeHtml(note.time_complexity)} time, ${escapeHtml(note.space_complexity)} space</p>
					</div>
				</article>
			`
		)
		.join("");
}

async function loadUser() {
	const user = await apiRequest("/auth/me");

	if (userLabel) {
		userLabel.textContent = `Signed in as ${user.email}`;
	}
}

async function loadCategories() {
	state.categories = await apiRequest("/categories/");
	renderCategories();
}

async function loadNotes() {
	state.notes = await apiRequest("/notes/");
	renderNotes();
}

async function loadDashboard() {
	if (!requireToken()) {
		return;
	}

	try {
		await loadUser();
		await Promise.all([loadCategories(), loadNotes()]);
	} catch (error) {
		clearToken();
		setMessage(error.message, "error");
		window.location.href = "/login";
	}
}

categoryForm?.addEventListener("submit", async (event) => {
	event.preventDefault();

	try {
		const data = getFormData(event.currentTarget);

		await apiRequest("/categories/", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(data),
		});

		event.currentTarget.reset();
		await loadCategories();
		setMessage("Category saved.");
	} catch (error) {
		setMessage(error.message, "error");
	}
});

noteForm?.addEventListener("submit", async (event) => {
	event.preventDefault();

	try {
		const data = getFormData(event.currentTarget);
		data.category_id = Number(data.category_id);

		await apiRequest("/notes/", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(data),
		});

		event.currentTarget.reset();
		await loadNotes();
		setMessage("Note saved.");
	} catch (error) {
		setMessage(error.message, "error");
	}
});

searchForm?.addEventListener("submit", async (event) => {
	event.preventDefault();

	try {
		const data = getFormData(event.currentTarget);
		const query = new URLSearchParams({
			question: data.question,
		});

		state.notes = await apiRequest(`/notes/search?${query}`);
		renderNotes();
	} catch (error) {
		setMessage(error.message, "error");
	}
});

notesList?.addEventListener("click", async (event) => {
	const target = event.target;

	if (!(target instanceof Element)) {
		return;
	}

	const button = target.closest("[data-delete-note]");

	if (!button) {
		return;
	}

	try {
		await apiRequest(`/notes/${button.dataset.deleteNote}`, {
			method: "DELETE",
		});
		await loadNotes();
		setMessage("Note deleted.");
	} catch (error) {
		setMessage(error.message, "error");
	}
});

refreshCategories?.addEventListener("click", async () => {
	try {
		await loadCategories();
	} catch (error) {
		setMessage(error.message, "error");
	}
});

refreshNotes?.addEventListener("click", async () => {
	try {
		await loadNotes();
	} catch (error) {
		setMessage(error.message, "error");
	}
});

clearSearch?.addEventListener("click", async () => {
	searchForm?.reset();

	try {
		await loadNotes();
	} catch (error) {
		setMessage(error.message, "error");
	}
});

logoutButton?.addEventListener("click", () => {
	clearToken();
	window.location.href = "/login";
});

loadDashboard();
