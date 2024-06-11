<script lang="ts">
  import env from "$lib/env";
	import { goto } from '$app/navigation';
	export let data: any;

	let str_links: string = "";
	
	async function get_links(): Promise<void> {
		let links: string[] = [];
		
		links = str_links.split('\n');
		const response = await fetch(env.BACKEND_URL + '/download', {
			method: 'POST',
			headers: {
				'Authorization': `${data['token_type']} ${data['access_token']}`,
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(links),
		});
		switch (response.status) {
			case 401:
				goto('/login');
				break;
			case 200:
				break
			default:
				console.log('An error occured');
				break;
		}
	}
</script>
<textarea name="links" id="links" bind:value="{str_links}" placeholder="Place your links here"></textarea>
<button on:click="{get_links}">Download</button>

<style>
textarea {
	height: 70%;
	width: 60%;
}
</style>