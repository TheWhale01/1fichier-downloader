<script lang="ts">
	let str_links: string = "";
	
	function get_links(): void {
		let links: string[] = [];
		
		links = str_links.split('\n');
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