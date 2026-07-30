import { apiRequest, getFormData, setMessage } from "./api.js";

const form = document.querySelector("#register-form");

form?.addEventListener("submit", async (event) => {
	event.preventDefault();

	try {
		const data = getFormData(event.currentTarget);

		await apiRequest("/auth/register", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(data),
		});

		event.currentTarget.reset();
		setMessage("Account created. Go to login when you are ready.");
	} catch (error) {
		setMessage(error.message, "error");
	}
});
