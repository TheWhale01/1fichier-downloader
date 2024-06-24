<script lang="ts">
	import env from "$lib/env";
	import Loading from "../../components/Loading.svelte";
	import { goto } from "$app/navigation";
	export let data: any;

	let str_links: string = "";
	let show_loading: boolean = false;

	async function get_links(): Promise<void> {
		let links: string[] = [];
		show_loading = true;

		links = str_links.split("\n");
		const response = await fetch(env.BACKEND_URL + "/download", {
			method: "POST",
			headers: {
				Authorization: `${data["token_type"]} ${data["access_token"]}`,
				"Content-Type": "application/json",
			},
			body: JSON.stringify(links),
		});
		show_loading = false;
		switch (response.status) {
			case 401:
				goto("/login");
				break;
			case 200:
				str_links = "";
				console.log(await response.json());
				break;
			default:
				console.log(response.statusText);
				break;
		}
	}
</script>

<textarea
	name="links"
	id="links"
	bind:value={str_links}
	placeholder="Place your links here"
></textarea>
<button on:click={get_links} disabled={show_loading}>Download</button>

{#if show_loading}
	<Loading title="Getting file informations..." />
{/if}

<style>
	textarea {
		height: 70%;
		width: 60%;
	}
</style>
