
class env {
	// static BACKEND_HOST: string = process.env.BACKEND_HOST
	// static BACKEND_PORT: string = process.env.BACKEND_PORT

	// Setup vite proxy
	static BACKEND_URL: string = `http://localhost:3000`;
	static SERVER_BACKEND_URL: string = `http://1fichier-downloader-backend:3000`;
}

export default env;