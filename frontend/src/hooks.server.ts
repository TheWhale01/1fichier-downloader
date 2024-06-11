import { redirect } from "@sveltejs/kit";
import env from "$lib/env";

export const handle = async ({ event, resolve }) => {
	const token: string | undefined = event.cookies.get('access_token');
	const type: string | undefined = event.cookies.get('token_type');
	const user = (await fetch(env.SERVER_BACKEND_URL + '/user')).status === 200;
	const valid_token = (await fetch(env.SERVER_BACKEND_URL + '/user/me', {
		headers: {'Authorization': `${type} ${token}`}
	})).status === 200;
	
	console.log(user);
	console.log(valid_token);
	if ((!user && !valid_token && !event.route.id?.startsWith('/setup'))
		|| (!user && valid_token && !event.route.id?.startsWith('/setup')))
		throw redirect(302, '/setup');
	else if (user && !valid_token && !event.route.id?.startsWith('/login'))
		throw redirect(302, '/login');
	else if (user && valid_token && !event.route.id?.startsWith('/(app)'))
		throw redirect(302, '/');
	const response = await resolve(event);
	return response;
}