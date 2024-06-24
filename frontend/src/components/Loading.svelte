<script lang="ts">
	export let title: string = "";
</script>

<div class="load_page">
	<div>
		<div class="spinner_container">
			<div class="spinner" />
		</div>
		<span>{title}</span>
	</div>
</div>

<style>
	.load_page {
		position:absolute;
		top: 0;
		left: 0;
		height: 100vh;
		width: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background-color: rgba(0, 0, 0, 0.4);
	}

	.spinner {
		border: 10px solid #f3f3f3;
		border-top: 10px solid #3498db;
		border-radius: 50%;
		width: 120px;
		height: 120px;
		margin-bottom: 20px;
		animation: spin 2s linear infinite;
	}

	.spinner_container {
		display: flex;
		justify-content: center;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	span {
		font-size: 1.5em;
		color: black;
		padding: 10px;
		background-color: white;
		border-radius: 10px;
	}
</style>
