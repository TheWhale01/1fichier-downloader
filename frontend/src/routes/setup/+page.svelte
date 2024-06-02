<script lang="ts">
	import { goto } from "$app/navigation";

	let username: string = "";
	let password: string = "";
	let conf_password: string = "";
	
	$: display_error = (password || conf_password) && (password !== conf_password);
	
	async function create_admin(): Promise<void> {
		if (!password || password !== conf_password)
			return ;
		
		const response = await fetch('http://localhost:3000/user', {
			method: "POST",
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				'username': username,
				'password': password
			})});
		const response_json = await response.json();
		if (response_json['user'])
			goto('/');
	}
</script>

<input type="text" placeholder="Username" bind:value="{username}" />
<input type="password" placeholder="password" class="{display_error ? "error_input" : ""}" bind:value="{password}" />
<input type="password" placeholder="password confirmation" class="{display_error ? "error_input" : ""}" bind:value="{conf_password}" />
<button type="submit" on:click="{create_admin}">Create Admin</button>