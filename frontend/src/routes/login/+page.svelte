<script lang="ts">
	import { access_token } from '$lib/stores';
	import { goto } from '$app/navigation';

	let username: string = "";
	let password: string = "";
	
	async function login(): Promise<void> {
		const response = await fetch(`http://localhost:3000/token`, {
			method: "POST",
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded'
			},
			body: new URLSearchParams({
				'username': username,
				'password': password
			})
		});
		if (response.status != 200)
			return ;
		const response_json = await response.json();
		access_token.set(response_json);
		goto('/');
	}
</script>

<input type="text" placeholder="username" bind:value="{username}" />
<input type="password" placeholder="password" bind:value="{password}" />
<button type="submit" on:click="{login}">Login</button>
