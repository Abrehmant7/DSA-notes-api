const API_BASE_URL = "http://127.0.0.1:8000";
export const TOKEN_KEY = "dsa_notes_token";

export function getToken() {
	return localStorage.getItem(TOKEN_KEY);
}

export function saveToken(token) {
	localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
	localStorage.removeItem(TOKEN_KEY);
}

export async function apiRequest(path, options = {}) {
	const token = getToken();
	const headers = {
		...(token ? { Authorization: `Bearer ${token}` } : {}),
		...(options.headers ?? {}),
	};

	const response = await fetch(`${API_BASE_URL}${path}`, {
		...options,
		headers,
	});

	if (response.status === 204) {
		return null;
	}

	const data = await response.json().catch(() => null);

	if (!response.ok) {
		const detail = data?.detail ?? "Request failed";
		throw new Error(typeof detail === "string" ? detail : "Request failed");
	}

	return data;
}

export function getFormData(form) {
	return Object.fromEntries(new FormData(form).entries());
}

export function setMessage(message, type = "success") {
	const box = document.querySelector("#message-box");

	if (!box) {
		return;
	}

	box.textContent = message;
	box.className =
		type === "error"
			? "mb-5 rounded-md border border-red-300 bg-red-50 px-4 py-3 text-sm font-semibold text-red-700"
			: "mb-5 rounded-md border border-zinc-950 bg-yellow-200 px-4 py-3 text-sm font-semibold text-zinc-950";
}

export function escapeHtml(value) {
	return String(value)
		.replaceAll("&", "&amp;")
		.replaceAll("<", "&lt;")
		.replaceAll(">", "&gt;")
		.replaceAll('"', "&quot;")
		.replaceAll("'", "&#039;");
}
