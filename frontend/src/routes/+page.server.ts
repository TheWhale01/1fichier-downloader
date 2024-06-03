import { redirect } from "@sveltejs/kit";
import env from "$lib/env";

export async function load({ params }): Promise<void> {
	const response = await fetch(env.BACKEND_URL + '/user');
	const response_json = await response.json();

	if (!response_json['user'])
		throw redirect(302, '/setup');
	else
		throw redirect(302, '/login')
}