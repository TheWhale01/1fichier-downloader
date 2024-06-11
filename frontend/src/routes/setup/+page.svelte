<script lang="ts">
	let username: string = '';
	let password: string = '';
	let password_conf: string = '';

	$: error = (!(username && password && (password === password_conf)));
</script>

<form method="post">
	<input type="text" placeholder="Username" name='username' bind:value={username}/>
	<input type="password" placeholder="password" name='password' bind:value={password}/>
	<input type="password" placeholder="password confirmation" name='password_conf' bind:value={password_conf}/>
	<button type="submit">Create Admin</button>
</form>
