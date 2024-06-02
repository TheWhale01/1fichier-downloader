<script lang="ts">
	let username: string = "";
	let password: string = "";
	
	function login(): void {
		console.log(username);
		console.log(password);
	}
</script>

<input type="text" placeholder="username" bind:value="{username}" />
<input type="password" placeholder="password" bind:value="{password}" />
<button type="submit" on:click="{login}">Login</button>
