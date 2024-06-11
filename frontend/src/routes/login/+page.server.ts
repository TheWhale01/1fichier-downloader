import env from '$lib/env';
import { redirect } from '@sveltejs/kit';

export const actions = {
	default: async ({ cookies, request }) => {
		const data = await request.formData();
		const username = data.get('username');
		const password = data.get('password');
		
		const response = await fetch(env.SERVER_BACKEND_URL + '/token', {
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
		const response_json = await response.json();
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
		throw redirect(302, '/');
	}
}