import env from '$lib/env';
import { redirect } from '@sveltejs/kit';

export const actions = {
	default: async ({ cookies, request }) => {
		const data = await request.formData();
		const username = data.get('username');
		const password = data.get('password');
		const password_conf = data.get('password_conf');
		
		if (!(username && password && (password === password_conf)))
			return ;
		const response = await fetch(env.SERVER_BACKEND_URL + '/user', {
			method: 'POST',
			headers: {
				'Content-type': 'application/json',
			},
			body: JSON.stringify({
				username: username,
				password: password
			})
		});
		if (response.status !== 200)
			return ;
		const response_token =  await fetch(env.SERVER_BACKEND_URL + '/token', {
			method: 'POST',
			headers: {
				'Content-type': 'application/x-www-form-urlencoded',
			},
			body: new URLSearchParams({
				'username': username,
				'password': password
			})
		});
		if (response.status !== 200)
			return ;
		const response_json = await response_token.json();
		cookies.set('access_token', response_json['access_token'], {
			path: '/',
			httpOnly: true,
			sameSite: 'lax',
			maxAge: 60 * 60
		});
		cookies.set('token_type', response_json['token_type'], {
			path: '/',
			httpOnly: true,
			sameSite: 'lax',
			maxAge: 60 * 60
		});
		if (response.status !== 200)
			return ;
		throw redirect(302, "/");
	}
}