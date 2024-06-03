<script lang="ts">
	import { goto } from "$app/navigation";

	let username: string = "";
	let password: string = "";
	
	async function login(): Promise<void> {
		const response = await fetch(`http://localhost:3000/login`, {
			method: "POST",
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				'username': username,
				'password': password
			})
		});
		const response_json = await response.json();

		if (response_json['isLoggedIn']) {
			// store token in localStorage
			goto('/');
		}
	}
</script>

<input type="text" placeholder="username" bind:value="{username}" />
<input type="password" placeholder="password" bind:value="{password}" />
<button type="submit" on:click="{login}">Login</button>
