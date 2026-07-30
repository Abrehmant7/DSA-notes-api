import { apiRequest, getFormData, saveToken, setMessage } from "./api.js";

const form = document.querySelector("#login-form");

form?.addEventListener("submit", async (event) => {
	event.preventDefault();

	try {
		const data = getFormData(event.currentTarget);
		const body = new URLSearchParams({
			username: data.email,
			password: data.password,
		});
		const token = await apiRequest("/auth/login", {
			method: "POST",
			headers: {
				"Content-Type": "application/x-www-form-urlencoded",
			},
			body,
		});

		saveToken(token.access_token);
		window.location.href = "/home";
	} catch (error) {
		setMessage(error.message, "error");
	}
});
